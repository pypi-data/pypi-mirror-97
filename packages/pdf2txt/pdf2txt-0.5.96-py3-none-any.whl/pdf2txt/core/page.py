from pdf2txt import utils
from pdf2txt.utils import BoundingBox, cluster_objects, collate_line
from pdf2txt.utils import resolve_all
from pdf2txt.core import Component
from pdf2txt.settings import ALL_ATTRS
from pdf2txt.core.word import WordExtractor
from pdf2txt.core.token import TokenExtractor, Token
from pdf2txt.graph import extract_graphs
from pdf2txt.core.region import RegionExtractor
from pdf2txt.core.paragraph import extract
from pdf2txt.table import TableFinder, Table, guess_table_from_token_lines
from pdf2txt.core.paragraph import ContentType
from pandas import DataFrame
import re
from statistics import mean
from pdf2txt.utils import cluster_objects

from pdf2txt.settings import DEFAULT_WORD_EXTRACTION_SETTINGS, DEFAULT_Y_TOLERANCE, DEFAULT_TOKEN_EXTRACTION_SETTINGS
lt_pat = re.compile(r"^LT")




class Page(Component):
    cached_properties = Component.cached_properties + ["_layout"]
    is_original = True
    __text_lines=None

    def __init__(self, parent, page_obj, page_number=None, bbox=None):
        self.document = parent
        self.page_obj = page_obj
        self.page_number = page_number
        self.title=[]
        self._words=None
        self.token_start=None
        self.token_end=None
        self.page_image=None
#        self._tokens=None
        self._region_extractor=RegionExtractor()

        mediabox = page_obj.attrs.get("MediaBox")

        self.mediabox = resolve_all(mediabox)
        m = self.mediabox

        if bbox is None:
            self.bbox = BoundingBox(
                        min(m[0], m[2]),
                        min(m[1], m[3]),
                        max(m[0], m[2]),
                        max(m[1], m[3]),
                )
        self._left_margin=None
        self._right_margin=None
        self._top_margin=None
        self._bottom_margin=None
        self.table_finder=TableFinder(self)
        self.root_page=self


    def detect_semantic_structure(self):

        self.regions.sort(key=lambda re: ( re.left, re.top))

        paragraph_number=0
        font_body={}
        page_font_statistics=self.font_statistics
        for region_number, region in enumerate(self.regions):
            font_statistics = region.font_statistics
            if self.page_number==0 and region_number <=1:
                if region_number==0 and region.height<self.bbox.height/8:
                    self.find_header(region, region_number==1)
            elif self.page_number>0 and region_number==0 and region.height<self.bbox.height/8:
                self.find_header(region, region_number == 1)

            title_font={}
            paragraphs=[]
            if len(region.text_lines)>0:
                paragraphs = self.extract_paragraph(region)
            for p in paragraphs:
                check_title=True
                paragraph_number+=1
                paragraph = self.document.paragraphs.get_last_paragraph()

                for n, tl in enumerate(p):
                    if isinstance(tl, DataFrame):
                        if paragraph is not None and len(paragraph.content)>0:
                            t=paragraph.content[-1]["content"]
                            if not isinstance(t, DataFrame) and check_title and t is not None and self.is_title2(t, font_statistics,
                                                                                page_font_statistics, title_font={}):
                                del paragraph.content[-1]
                                paragraph = self.document.paragraphs.create_paragraph()
                                paragraph.title = t
                                check_title = False
                            else:
                                columns = tl.columns.tolist()
                                if len(columns)>0:

                                    if paragraph is not None and len(paragraph.content)>0 and len(columns)>0:
                                        first=columns[0]
                                        t=self.get_token_with_value(first)
                                        if check_title and t is not None and self.is_title2([t], page_font_statistics, page_font_statistics,title_font):
                                            paragraph = self.document.paragraphs.create_paragraph()
                                            paragraph.title = [t]
                                        if paragraph is None:
                                            paragraph = self.document.paragraphs.create_paragraph()
                        elif paragraph is None:
                            paragraph = self.document.paragraphs.create_paragraph()
                        paragraph.add_content(tl, ContentType.Table)

                    elif check_title and (paragraph is None or self.is_title2(tl, font_statistics, page_font_statistics,title_font, font_body)):
#                        existing_title=self.document.paragraphs.filter_by_title_equal(tl)
                        paragraph=self.document.paragraphs.create_paragraph()
                        paragraph.title=tl
                        title_font['name'] = tl[0].font + str(tl[0].Text.isupper() or tl[0].is_bold)
                        title_font['size'] = tl[0].font_size
                        check_title=False
                    else:
                        paragraph.add_content(tl, ContentType.Text)
                        if tl[0].font_size<=self.font_statistics['average']:
                            font_body['name']= tl[0].font+str(tl[0].is_bold)
                            font_body['size'] = tl[0].font_size

                        check_title=True


    def extract_paragraph2(self, region):

        if len(region.graphs):
            top = region.top
            paragraphs = []
            for graph in sorted(region.graphs, key=lambda g: g.top):
                top_paragraph = extract([tl for tl in region.text_lines if top<tl[0].top <= graph.top ])
                if len(top_paragraph[0]) > 0:
                    paragraphs.extend(top_paragraph)
                graph_paragraph=[]
                graph_data = graph.extract_chart_data()
                if 'text' in graph_data and len(graph_data['text']) > 0:
                    graph_paragraph.append(graph_data['text'])
                if 'dataframe' in graph_data and graph_data['dataframe'] is not None:
                    graph_paragraph.append(graph_data['dataframe'])
                paragraphs.append(graph_paragraph)


                top = graph.bottom
            last_paragraph = extract([tl for tl in region.text_lines if tl[0].top > top])
            if len(last_paragraph[0]) > 0:
                paragraphs.extend(last_paragraph)
        else:
            paragraphs = extract(region.text_lines)
        paragraphs2=[]
        for p in paragraphs:
            if isinstance(p, DataFrame) or len(p)<=2:
                paragraphs2.append(p)
                continue
            lines_for_table = []
            pp=[]
            tables= utils.get_partially_overlapping_objects(utils.get_BoundingBox_from_objects([t for l in p for t in l]), region.tables)
            if not tables: #try another method to guess tables. The presence of lines with the same number of tokens with emty space in between can signbal the presence of a table
                tables=guess_table_from_token_lines(region, p)
                if tables:
                    for l in p:
                        if l not in tables.textlines:
                            pp.append(l)
                    pp.append(tables.to_pandas())
                    paragraphs2.append(pp)
                    continue
            if tables:
                i=-1
                while i < len(p)-1:
                    i+=1
                    l=p[i]
                    if len(l)>=2 or (len(l)==1 and utils.get_type(l[0].Text.strip('%'))=="Numeric"):
                        lines_for_table.append(l)
                    elif len(lines_for_table) > 2:
                        table = Table(region, textlines=lines_for_table, rect=utils.get_BoundingBox_from_objects(tables), paragraph=p).extract()
#                       print(table.to_string())
                        pp.append(table.to_pandas())
#                       pp.extend([p for p in pp if not isinstance(p, DataFrame) and p not in table.textlines and p not in pp])
                        i+=len(table.textlines)-len(lines_for_table)-1
                        lines_for_table = []
                    elif len(lines_for_table)==1:
                        pp.extend(lines_for_table)
                        lines_for_table=[]
                    else:
                        pp.append(l)
                if len(lines_for_table)>1:
                    table = Table(region, textlines=lines_for_table,rect=utils.get_BoundingBox_from_objects(tables), paragraph=p).extract()
#                    print(table.to_string())
#                    pp=[p for p in pp if p not in table.textlines]
                    pp.append(table.to_pandas())
                else:
                    pp.extend(lines_for_table)
            else:
                pp=p
            paragraphs2.append(pp)
        return paragraphs2


    def extract_paragraph(self, region):
        returned_paragraphs= []

        g_paragraph=self.extract_paragaph_from_graph(region)

        if g_paragraph:
            returned_paragraphs=g_paragraph
        else:
            txt_paragraphs = extract(region.text_lines)


            for p in txt_paragraphs:
                paragraph = []
                table_region=None
                text_lines = Table.extract_table_lines_from_paragaraph(p)
                table_regions = utils.get_partially_overlapping_objects(
                    utils.get_BoundingBox_from_objects([t for l in p for t in l]), region.tables)
                if table_regions:
                    table_region=utils.get_BoundingBox_from_objects(table_regions)

                if text_lines or table_region:
                    i=0
                    table = Table(region, textlines=text_lines if text_lines else p, rect=table_region, paragraph=p).extract()
                    while i < len(p):
                        line=p[i]
                        if table is None or line not in table.textlines:
                            paragraph.append(line)
                            i+=1
                        else:
                            paragraph.append(table.to_pandas())
                            i += len(table.textlines)
                else:
                    paragraph=p

                returned_paragraphs.append(paragraph)
        return returned_paragraphs


    def extract_paragaph_from_graph(self, region):


        if len(region.graphs)==0:
            return []
        else:
            top = region.top
            paragraphs = []
            for graph in sorted(region.graphs, key=lambda g: g.top):
                top_paragraph = extract([tl for tl in region.text_lines if top < tl[0].top <= graph.top])
                if len(top_paragraph[0]) > 0:
                    paragraphs.extend(top_paragraph)
                graph_paragraph = []
                graph_data = graph.extract_chart_data()
                if 'text' in graph_data and len(graph_data['text']) > 0:
                    graph_paragraph.append(graph_data['text'])
                if 'dataframe' in graph_data and graph_data['dataframe'] is not None:
                    graph_paragraph.append(graph_data['dataframe'])
                paragraphs.append(graph_paragraph)

                top = graph.bottom
            last_paragraph = extract([tl for tl in region.text_lines if tl[0].top > top])
            if len(last_paragraph[0]) > 0:
                paragraphs.extend(last_paragraph)

        return paragraphs

    def is_title2(self, textline, font_stat, page_font_stat, title_font={}, font_body={}):

        if len(textline)==0:
            return False
        if font_body and textline[0].font+str(textline[0].Text.isupper() or textline[0].is_bold)==font_body['name'] and textline[0].font_size==font_body['size']:
            return False

        if utils.get_type(textline[0].Text.replace('M€', '').replace('€', '').replace('/', '').strip())== "Numeric":
            return False
        if title_font and textline[0].font+str(textline[0].Text.isupper() or textline[0].is_bold)==title_font['name']:
            return True
        elif title_font and textline[0].font_size>title_font['size']:
            return True
        elif title_font:
            return False
        if (len(font_stat["name_by_frequency"]) > 1 or len(font_stat["size_by_frequency"]) > 1) and (textline[0].font_size >= font_stat['second_largest'] and font_stat['second_largest']>-1):
            title_font['name']= textline[0].font+str(textline[0].Text.isupper() or textline[0].is_bold)
            title_font['size']=textline[0].font_size
            return True
        elif len(font_stat["name_by_frequency"]) == 1 and len(font_stat["size_by_frequency"]) == 1:
            if font_stat['most_frequent']< page_font_stat["largest"]:
                return False
            elif font_stat['most_frequent']== page_font_stat["largest"] and (textline[0].Text.isupper() or textline[0].is_bold):
                title_font['name']=textline[0].font+str(textline[0].Text.isupper() or textline[0].is_bold)
                title_font['size']=textline[0].font_size
                return True
            elif font_stat['most_frequent']== page_font_stat["largest"]:
                return False
        return False

    def find_header(self, region, largest_only=False):
        font_stat= region.parent_page.font_statistics
        first_horizontal_separator = None
        horizontal_separators = [line for line in region.horizontal_lines+region.horizontal_edges if line.width > self.width * 0.7 and line.top>10]
        if len(horizontal_separators) > 0:
            first_horizontal_separator = horizontal_separators[0]
        for l in region.text_lines[:5]:
            if first_horizontal_separator and l[0].top > first_horizontal_separator.top and len(self.title)>0:
                return

            if not largest_only and (l[0].font_size == font_stat["largest"] or l[0].font_size > font_stat["most_frequent"]):
                self.title.append(l)
                region.text_lines.remove(l)
            elif largest_only and l[0].font_size == font_stat["largest"]:
                self.title.append(l)
                region.text_lines.remove(l)
        return False

    def is_title(self, id, region_number, line, font_stat, title_font={}):

        if len(line)>1:
            return False

        if line[0].font_size >= font_stat["most_frequent"] and region_number == 0 and id<3:
            title_font['font']=line[0].font
            return True

        if title_font:
            if line[0].font == title_font['font']:
                return True
            else:
                return False

        if len(line)==1 and utils.get_type(line[0].Text)=="Numeric":
            return False

        if line[0].font_size > font_stat["most_frequent"]:
            title_font['font']=line[0].font
            return True



        if len(font_stat["size_by_frequency"])==1 and line[0].is_bold:
            title_font['font']=line[0].font
            return True

        if len(font_stat["size_by_frequency"])==1 and len(font_stat["name_by_frequency"])==1:
            return False

        if id==0:
            title_font['font'] = line[0].font
            return True

        return False


    def set_page_layout(self):

        self.image_width = self.page_image.shape[1]
        self.image_height = self.page_image.shape[0]
        self.image_width_scaler = self.image_width / float(self.width)
        self.image_height_scaler = self.image_height / float(self.height)
        self.pdf_width_scaler = self.width / float(self.image_width)
        self.pdf_height_scaler = self.height / float(self.image_height)
        self.image_scalers = (self.image_width_scaler, self.image_height_scaler, self.height)
        self.pdf_scalers = (self.pdf_width_scaler, self.pdf_height_scaler, self.image_height)


    def get_token_with_value(self, val):
        for t in self.tokens:
            if t.Text==val:
                return t

    @property
    def regions(self):
        if hasattr(self, "_regions"):
            return self._regions

        self._regions=[r for r in self._region_extractor.extract_regions(self) if len(r.text_lines)>0]
        return self._regions


    @property
    def width(self):
        return self.bbox.right - self.bbox.left

    @property
    def height(self):
        return self.bbox.bottom - self.bbox.top

    @property
    def layout(self):
        if hasattr(self, "_layout"):
            return self._layout
        self._layout = self.document.get_page(self.page_obj)
        return self._layout

    @property
    def font_statistics(self):
        if hasattr(self, "_font_statistics"):
            return self._font_statistics

        self._font_statistics = utils.get_fonts_statistics(self.text_lines)
        return self._font_statistics

    @property
    def objects(self):
        if hasattr(self, "_objects"):
            return self._objects
        self._objects = self.parse_objects()
        return self._objects

    def process_object(self, obj):
        kind = re.sub(lt_pat, "", obj.__class__.__name__).lower()

        def process_attr(item):
            k, v = item
            if k in ALL_ATTRS:
                res = resolve_all(v)
                return (k, res)
            else:
                return None

        attr = dict(filter(None, map(process_attr, obj.__dict__.items())))

        attr["object_type"] = kind
        attr["page_number"] = self.page_number

        if hasattr(obj, "graphicstate"):
            gs = obj.graphicstate
            attr["stroking_color"] = gs.scolor
            attr["non_stroking_color"] = gs.ncolor
            attr["linewidth"] = gs.linewidth

        if hasattr(obj, "get_text"):
            attr["text"] = obj.get_text()

        if kind == "curve":

            def point2coord(pt):
                x, y = pt
                return (x, self.height - y)

            attr["points"] = list(map(point2coord, obj.pts))

        if attr.get("y0") is not None:
            attr["top"] = self.height - attr["y1"]
            attr["bottom"] = self.height - attr["y0"]
        if attr.get("x0") is not None:
            attr["left"] =  attr["x0"]
        if attr.get("x1") is not None:
            attr["right"] = attr["x1"]

        return attr

    def iter_layout_objects(self, layout_objects):
        for obj in layout_objects:
            # If object is, like LTFigure, a higher-level object
            # then iterate through it's children
            if hasattr(obj, "_objs"):
                yield from self.iter_layout_objects(obj._objs)
            else:
                yield self.process_object(obj)

    def parse_objects(self):
        objects = {}
        for obj in self.iter_layout_objects(self.layout._objs):
            kind = obj["object_type"]

            if objects.get(kind) is None:
                objects[kind] = []
            objects[kind].append(obj)
        return objects

    def within_bbox(self, bbox, relative=False):
        """
        Same as .crop, except only includes objects fully within the bbox
        """
        return Region(self, bbox)

    @property
    def tables(self):
        if hasattr(self, "_tables"):
            return self._tables

        self._tables = self.table_finder.guess_tables()
        return self._tables

    @property
    def graphs(self):
        if hasattr(self, "_graphs"):
            return self._graphs


        self._graphs=extract_graphs(page=self, rect_threshold=2)
        return self._graphs


    @property
    def words(self):
        settings = dict(DEFAULT_WORD_EXTRACTION_SETTINGS)
        if self._words:
            return self._words
        if not self.chars:
            return []
        chars=self.chars

        if "linewidth" in self.chars[0]:
            chars=[char for char in self.chars if (char["upright"] and (char["left"] > 0 and char["linewidth"] > 0) or (
                        char["linewidth"] == 0 and char["non_stroking_color"] not in [(1, 0, 1)]))]
        self._words= WordExtractor(self, **settings).extract(chars)
        return self._words

    def to_image(self, **conversion_kwargs):
        """
        For conversion_kwargs, see:
        http://docs.wand-py.org/en/latest/wand/image.html#wand.image.Image
        """
        from pdf2txt.visualize import PageImage, DEFAULT_RESOLUTION

        kwargs = dict(conversion_kwargs)
        if "resolution" not in conversion_kwargs:
            kwargs["resolution"] = DEFAULT_RESOLUTION
        return PageImage(self, **kwargs)

    @property
    def tokens(self):
        if self.token_start is not None and self.token_end is not None:
            return self.document._token_list[self.token_start:self.token_end]

        settings = dict(DEFAULT_TOKEN_EXTRACTION_SETTINGS)

        self.token_start=len(self.document._token_list)

        _tokens=TokenExtractor(self, **settings).extract(self.words)

        for i, token in enumerate(_tokens):
            token.index=self.token_start+i
            self.document._token_list.append(token)

        self.token_end=len(self.document._token_list)
        return self.document._token_list[self.token_start:self.token_end]

    @property
    def text_lines(self):

        if self.__text_lines is not None:
            return self.__text_lines
        if len(self.tokens)==0:
            return []
 #       doctop_clusters = cluster_objects(self.tokens, "bottom", self.tokens[0].font_size/3)

#        if doctop_clusters is not None:
        self.__text_lines = utils.find_line_structure(self.tokens) #[sorted(line, key=lambda x: x.left) for line in doctop_clusters]

        return self.__text_lines


    def __repr__(self):
        return f"<Page:{self.page_number}>"

    @property
    def top(self):
        return self.bbox.top

    @property
    def bottom(self):
        return self.bbox.bottom

    @property
    def left(self):
        return self.bbox.left

    @property
    def right(self):
        return self.bbox.right


    @property
    def left_margin(self):
        if self._left_margin is None:
            if len(self.tokens)==0:
                self._left_margin=0
            else:
                self._left_margin = min([t.left for t in self.tokens])

        return self._left_margin

    @property
    def content_width(self):
        return self.right_margin-self.left_margin


    @property
    def right_margin(self):
        if self._right_margin is None:
            if len(self.tokens)==0:
                self._right_margin=self.width
            else:
                self._right_margin = max([t.right for t in self.tokens])
            if self._right_margin>=self.bbox.right:
                self._right_margin=self.bbox.right-self.left_margin/2
        return self._right_margin

    @property
    def top_margin(self):
        if self._top_margin is None:
            if len(self.tokens)==0:
                self._top_margin=0
            else:
                self._top_margin = min([t.top for t in self.tokens])
        return self._top_margin

    @property
    def bottom_margin(self):
        if self._bottom_margin is None:
            if len(self.tokens)==0:
                self._bottom_margin=self.height
            else:
                self._bottom_margin = max([t.bottom for t in self.tokens])
        return self._bottom_margin

class Region(Page):
    is_original = False

    def __init__(self, parent_page, bbox):

        self.parent_page = parent_page
        self.page_number = parent_page.page_number
        self.bbox=BoundingBox(top=int(bbox.top*parent_page.pdf_height_scaler), left=int(bbox.left*parent_page.pdf_width_scaler), right=int(bbox.right*parent_page.pdf_width_scaler), bottom=int(bbox.bottom*parent_page.pdf_height_scaler)-1)
        super().__init__(parent_page.document, parent_page.page_obj, bbox=bbox)
        self.flush_cache(Component.cached_properties)



        if type(parent_page) == Page:
            self.root_page = parent_page
        else:
            self.root_page = parent_page.root_page
        self.sections=[]

    def __repr__(self):
        return f"<Region:{self.page_number}>"

    @property
    def objects(self):
        if hasattr(self, "_objects"):
            return self._objects
        self._objects = utils.get_widthin_bbox(self.parent_page.objects, self.bbox)
        return self._objects

    @property
    def tokens(self):
        return utils.get_widthin_BoundingBox(self.parent_page.tokens, self.bbox)