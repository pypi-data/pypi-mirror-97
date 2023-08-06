# from pdf2txt.colors import get_color_name
from pdfminer.pdftypes import PDFObjRef
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.psparser import PSLiteral
from pdfminer.pdfdocument import PDFDocument
from math import floor
import re
import numpy as np

from operator import itemgetter
from statistics import mean
import itertools
from pdf2txt.settings import DEFAULT_MIN_WORDS_VERTICAL, DEFAULT_X_TOLERANCE, DEFAULT_Y_TOLERANCE
from copy import copy
import ast
import tempfile, shutil
import numpy as np
import pdf2image
import cv2

class BoundingBox():
    """Contains coordinate of object on the page bottom left of the page correspond to 0,0"""

    def __init__(self, left=None, top=None, right=None, bottom=None,  **kwargs):
        self.left = left  #
        self.bottom = bottom
        self.right = right
        self.top = top
        self.space_above=None
        self.space_bellow=None
        self._height=self.bottom - self.top

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def height(self):
        return self.bottom - self.top

    @height.setter
    def height(self, value):
        self._height=value

    def __repr__(self):
        return '(' + str(self.left) + " " + str(self.top) + " " + str(self.right) + " " + str(self.bottom) + " " + ")"

# https://stackoverflow.com/a/22726782
class TemporaryDirectory(object):
    def __enter__(self):
        self.name = tempfile.mkdtemp()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)


def bbox_to_rect(bbox):
    return {"left": bbox[0], "top": bbox[1], "right": bbox[2], "bottom": bbox[3]}




def convert_pdf_to_image(document, dpi):
    images = []
    images.extend(
                    list(
                        map(
                            lambda image: cv2.cvtColor(
                                np.asarray(image), code=cv2.COLOR_RGB2BGR
                            ),
                            pdf2image.convert_from_path(document, dpi=dpi),
                        )
                    )
                )
    return images

def get_page_layout( filename,  char_margin=2.0, line_margin=0.5, word_margin=0.1, detect_vertical=False, all_texts=True):
    """Returns a PDFMiner LTPage object and page dimension of a single
    page pdf. See https://euske.github.io/pdfminer/ to get definitions
    of kwargs.
    Parameters
    ----------
    filename : string
        Path to pdf file.
    char_margin : float
    line_margin : float
    word_margin : float
    detect_vertical : bool
    all_texts : bool
    Returns
    -------
    layout : object
        PDFMiner LTPage object.
    dim : tuple
        Dimension of pdf page in the form (width, height).
    """
    with open(filename, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed(f"Text extraction is not allowed: {filename}")
        laparams = LAParams(
            char_margin=char_margin,
            line_margin=line_margin,
            word_margin=word_margin,
            detect_vertical=detect_vertical,
            all_texts=all_texts,
            boxes_flow=None
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            width = layout.bbox[2]
            height = layout.bbox[3]
            dim = (width, height)
            return layout, dim




def are_in_same_Line(word1, word2, tol=2.3):
    return np.isclose(word1.top, word2.top, atol=tol) and np.isclose(word1.bottom, word2.bottom, atol=tol)

def are_in_same_line2(word1, word2, tolerance='auto'):
    if tolerance=='auto':
        tolerance=(word1.bottom-word1.top)/3
    return max(0, min(word1.bottom, word2.bottom) - max(word1.top, word2.top))>tolerance

def extract_text(
        chars, x_tolerance=DEFAULT_X_TOLERANCE, y_tolerance=DEFAULT_Y_TOLERANCE
    ):

        if len(chars) == 0:
            return None

        chars = list(chars)
        doctop_clusters = cluster_objects(chars, "doctop", y_tolerance)

        lines = (collate_line(line_chars, x_tolerance) for line_chars in doctop_clusters)

        coll = "\n".join(lines)
        return coll


def join_collated_h_edges(edges):
    clustered=cluster_objects(edges, "bottom", 1)

    if clustered is None:
        return []

    returned_edges=[]
    for c in clustered:
        if len(c)==1:
            returned_edges.append(c[0])
        else:
            c=sorted(c, key=lambda x: x.left)
            returned_edges.append(c[0])
            for i in  range(1, len(c)):
                if np.isclose(returned_edges[-1].right, c[i].left, atol=3) or returned_edges[-1].right> c[i].left:
                    returned_edges[-1].right=max(returned_edges[-1].right, c[i].right)
                    returned_edges[-1].width=returned_edges[-1].right-returned_edges[-1].left
                else:
                    returned_edges.append(c[i])

    #combine lines that have less than 2 pixels separation
    returned_edges=sorted(returned_edges, key=lambda e:(e.top, e.left))
    edges2=[returned_edges[0]]
    for i in range(1, len(returned_edges)):
        if not np.isclose(edges2[-1].top, returned_edges[i].top, atol=4) or horizontal_overlap(edges2[-1], returned_edges[i])==0 :
            edges2.append(returned_edges[i])

        elif edges2[-1].width<returned_edges[i].width:
            del edges2[-1]
            edges2.append(returned_edges[i])

    return edges2

def join_collated_v_edges(edges):
    clustered=cluster_objects(edges, "left", 1)

    if clustered is None:
        return []

    returned_edges=[]
    for c in clustered:
        if len(c)==1:
            returned_edges.append(c[0])
        else:
            c=sorted(c, key=lambda x: x.top)
            returned_edges.append(c[0])
            for i in  range(1, len(c)):
                if np.isclose(returned_edges[-1].bottom, c[i].top, atol=1) or returned_edges[-1].bottom> c[i].top:
                    returned_edges[-1].bottom=c[i].bottom
                else:
                    returned_edges.append(c[i])

    return returned_edges


def rect_to_edges(rect):
    top, bottom, left, right = [copy(rect) for x in range(4)]

    top.object_type="rect_edge"
    top.height= 0.0
    top.bottom=rect.top
    top.orientation="h"


    bottom.object_type="rect_edge"
    bottom.height= 0.0
    bottom.top=rect.bottom
    bottom.orientation="h"

    left.object_type = "rect_edge"
    left.width = 0.0
    left.right = rect.left
    left.orientation = "v"

    right.object_type = "rect_edge"
    right.width = 0.0
    right.left = rect.right
    right.orientation = "v"

    return [top, bottom, left, right]


def line_to_edge(line):
    edge = line
    edge.orientation = "h" if (line.width > line.height) else "v"
    return edge


def curve_to_edges(curve):
    point_pairs = zip(curve["points"], curve["points"][1:])
    return [
        {
            "left": min(p0[0], p1[0]),
            "right": max(p0[0], p1[0]),
            "top": min(p0[1], p1[1]),
            "bottom": max(p0[1], p1[1]),
            "width": abs(p0[0] - p1[0]),
            "height": abs(p0[1] - p1[1]),
            "orientation": "v" if p0[0] == p1[0] else ("h" if p0[1] == p1[1] else None),
        }
        for p0, p1 in point_pairs
    ]


def filter_edges(edges, orientation=None, edge_type=None, min_length=1):
    if orientation not in ("v", "h", None):
        raise ValueError("Orientation must be 'v' or 'h'")

    def test(e):
        dim = "height" if e.orientation == "v" else "width"
        et_correct = e.object_type == edge_type if edge_type is not None else True
        orient_correct = orientation is None or e.orientation == orientation
        return et_correct and orient_correct and (getattr(e, dim) >= min_length)

    edges = filter(test, edges)
    return list(edges)


def resolve(x):
    if type(x) == PDFObjRef:
        return x.resolve()
    else:
        return x

def dedupe_chars(chars, tolerance=1):
    """
    Removes duplicate chars.
    """
    key = itemgetter("fontname", "size", "upright", "text")
    pos_key = itemgetter("top", "x0")
    t = tolerance

    def yield_unique_chars(chars):
        sorted_chars = sorted(chars, key=key)
        for grp, grp_chars in itertools.groupby(sorted_chars, key=key):
            for y_cluster in cluster_objects(grp_chars, "top", t):
                for x_cluster in cluster_objects(y_cluster, "left", t):
                    yield sorted(x_cluster, key=pos_key)[0]

    deduped = yield_unique_chars(chars)
    return sorted(deduped, key=chars.index)


def collate_line(line_tokens, tolerance=DEFAULT_X_TOLERANCE):
    tolerance = tolerance
    coll = ""
    last_x1 = None
    for token in sorted(line_tokens, key=lambda x: x["top"]):
        if (last_x1 is not None) and (token["top"] > (last_x1 + tolerance)):
            coll += " "
        last_x1 = token["right"]
        coll += token["text"]
    return coll


def get_dict_type(d):
    if type(d) is not dict:
        return None
    t = d.get("Type")
    if type(t) is PSLiteral:
        return t.name
    else:
        return t


def resolve_all(x):
    """
    Recursively resolves the given object and all the internals.
    """
    t = type(x)
    if t == PDFObjRef:
        resolved = x.resolve()

        # Avoid infinite recursion
        if get_dict_type(resolved) == "Page":
            return x

        return resolve_all(resolved)
    elif t in (list, tuple):
        return t(resolve_all(v) for v in x)
    elif t == dict:
        if get_dict_type(x) == "Annot":
            exceptions = ["Parent"]
        else:
            exceptions = []
        return dict((k, v if k in exceptions else resolve_all(v)) for k, v in x.items())
    else:
        return x




def object_to_bbox(object):
    return (
        object.left,
        object.top,
        object.right,
        object.bottom
    )


def get_type(value):

    if isinstance(value, int) or isinstance(value, float):
        return "Numeric"

    if isinstance(value, str):
        value = value.strip('%')
    try:
        float(value)
        return "Numeric"
    except:
        return "Literal"


def get_overlap_with_bbox(a, b):
    a_left, a_top, a_right, a_bottom = a.left, a.top, a.right, a.bottom
    b_left, b_top, b_right, b_bottom = b.left, b.top, b.right, b.bottom
    o_left = max(a_left, b_left)
    o_right = min(a_right, b_right)
    o_bottom = min(a_bottom, b_bottom)
    o_top = max(a_top, b_top)
    o_width = o_right - o_left
    o_height = o_bottom - o_top
    if o_height >= 0 and o_width >= 0 and o_height + o_width > 0:
        return {"left": o_left, "top": o_top, "right": o_right, "bottom": o_bottom}
    else:
        return None


def get_partially_overlapping_objects(bbox, objects):
    objs = []
    for o in objects:
        if isinstance(o, dict):
            o = BoundingBox(left=o["left"], top=o["top"], right=o["right"], bottom=o["bottom"])
        if has_overlap_with_bbox(o, bbox):
            objs.append(o)

    return objs

def get_partially_touching_objects(bbox, objects):
    objs = []
    for o in objects:
        if isinstance(o, dict):
            o = BoundingBox(left=o["left"], top=o["top"], right=o["right"], bottom=o["bottom"])
        if is_touching_with_bbox(bbox, o):
            objs.append(o)

    return objs

def has_overlap_with_bbox(a, b, allow_touching=False):
    if isinstance(a, tuple):
        a=BoundingBox(a[0],a[1],a[2],a[3])
    if isinstance(b, tuple):
        b=BoundingBox(b[0],b[1],b[2],b[3])
    if allow_touching:
        return not (round(a.right, 2) <= round(b.left,2) or round(a.left,2) >= round(b.right,2) or round(a.bottom,2) <= round(b.top,2) or round(a.top,2) >= round(b.bottom,2))
    return not (a.right < b.left or a.left > b.right or a.bottom < b.top or a.top > b.bottom)

def is_touching_with_bbox(line, bbox):
    if isinstance(line, tuple):
        line=BoundingBox(line[0], line[1], line[2], line[3])
    if isinstance(bbox, tuple):
        bbox=BoundingBox(bbox[0], bbox[1], bbox[2], bbox[3])

    x1, y1, x2, y2=floor(line.left), floor(line.top), floor(line.right), floor(line.bottom)

    x3, y3=floor(bbox.left), floor(bbox.top)

    if x1==x2:
        pt3_on = x3==x1

    elif y1==y2:
        pt3_on = y3==y1
    else:
        slope = (y2 - y1) / (x2 - x1)
        pt3_on = (y3 - y1) == slope * (x3 - x1)


    if not pt3_on:
        x3, y3 = floor(bbox.right), floor(bbox.bottom)

        if x1 == x2:
            pt3_on = x3 == x1

        elif y1 == y2:
            pt3_on = y3 == y1
        else:
            slope = (y2 - y1) / (x2 - x1)
            pt3_on = (y3 - y1) == slope * (x3 - x1)

    pt3_between = (min(x1, x2) <= x3 <= max(x1, x2)) and (min(y1, y2) <= y3 <= max(y1, y2))
    on_and_between = pt3_on and pt3_between

    return on_and_between

def is_ovarlaping_with_objects(bbox, objects, allow_touching=False):
    for o in objects:
        if isinstance(o, dict):
            o = BoundingBox(left=o["left"], top=o["top"], right=o["right"], bottom=o["bottom"])
        if has_overlap_with_bbox(o, bbox, allow_touching):
            return True
    return False

def get_max_non_overlap_zone(line, objects):
    tops=[]
    bottoms=[]

    for o in sorted(objects, key=lambda x: x.top):
        if has_overlap_with_bbox(o, line):
            tops.append(o.top)
            bottoms.append(o.bottom)
    diffs=[]
    for i in range(1, len(tops)):
        diffs.append(tops[i]-bottoms[i-1])

    if diffs:
        i=diffs.index(max(diffs))
        if i == 0:
            i = 1
        return (tops[i-1], bottoms[i])
    return False


def get_widthin_bbox(objs, bbox):
    """
    Filters objs to only those intersecting the bbox,
    and crops the extent of the objects to the bbox.
    """
    if isinstance(objs, dict):
        return dict((k, get_widthin_bbox(v, bbox)) for k, v in objs.items())

    else:

        sub_obj= [o for o in objs if get_overlap_with_bbox(BoundingBox(left=o["left"], top=o["top"], right=o["right"], bottom=o["bottom"]), bbox)]
        return sub_obj

def get_widthin_BoundingBox(objs, bbox):
    """
    Filters objs to only those intersecting the bbox,
    and crops the extent of the objects to the bbox.
    """

    if len(objs)==0:
        return []
    if isinstance(objs, dict):
        return dict((k, get_widthin_bbox(v, bbox)) for k, v in objs.items())


    else:
        if isinstance(objs[0], list):
            sub_obj = [o for o in objs if get_overlap_with_bbox(get_BoundingBox_from_objects(o), bbox)]
        else:
            sub_obj= [o for o in objs if get_overlap_with_bbox(o, bbox)]
        return sub_obj

def cluster_list(xs, tolerance=0):
    if tolerance == 0:
        return [[x] for x in sorted(xs)]
    if len(xs) < 2:
        return [[x] for x in sorted(xs)]
    groups = []
    xs = list(sorted(xs))
    current_group = [xs[0]]
    last = xs[0]
    for x in xs[1:]:
        if x <= (last + tolerance):
            current_group.append(x)
        else:
            groups.append(current_group)
            current_group = [x]
        last = x
    groups.append(current_group)
    return groups

def cluster_list_multi(xs, tolerance=0):
    if tolerance == 0:
        return [[x] for x in sorted(xs)]
    if len(xs) < 2:
        return [[x] for x in sorted(xs)]
    groups = []
    xs = list(sorted(xs))
    current_group = [xs[0]]
    last = xs[0]
    for x in xs[1:]:
        if np.isclose(x[0], last[0], atol= tolerance) and np.isclose(x[1],  last[1], atol= tolerance):
            current_group.append(x)
        else:
            groups.append(current_group)
            current_group = [x]
        last = x
    groups.append(current_group)
    return groups


def make_cluster_dict(values, tolerance, multi=False):
    if multi:
        clusters = cluster_list_multi(set(values), tolerance)
    else:
        clusters = cluster_list(set(values), tolerance)

    nested_tuples = [
        [(val, i) for val in value_cluster] for i, value_cluster in enumerate(clusters)
    ]

    cluster_dict = dict(itertools.chain(*nested_tuples))
    return cluster_dict


def cluster_objects(objs, attr, tolerance):
    if not objs:
        return None
    if isinstance(attr, (str, int)):
        attr_getter = itemgetter(attr)
    else:
        attr_getter = attr

    objs = list(objs)

    values = map(attr_getter, objs)

    if not isinstance(objs[0], dict) and isinstance(attr, (str, int)):
        values = map(lambda p: getattr(p, attr), objs)

    cluster_dict = make_cluster_dict(values, tolerance)

    get_0, get_1 = itemgetter(0), itemgetter(1)

    if not isinstance(objs[0], dict) and isinstance(attr, (str, int)):
        cluster_tuples = sorted(
            ((obj, cluster_dict.get(getattr(obj, attr))) for obj in objs), key=get_1
        )
    else:
        cluster_tuples = sorted(
            ((obj, cluster_dict.get(attr_getter(obj))) for obj in objs), key=get_1
        )

    grouped = itertools.groupby(cluster_tuples, key=get_1)

    clusters = [list(map(get_0, v)) for k, v in grouped]

    return clusters


def cluster_objects_multi(objs, attr1, attr2, tolerance):
    if not objs:
        return None

    objs = list(objs)


    values = list(map(lambda p: (getattr(p, attr1), getattr(p, attr2)), objs))

    cluster_dict = make_cluster_dict(values, tolerance, multi=True)

    get_0, get_1 = itemgetter(0), itemgetter(1)

    cluster_tuples = sorted(
        ((obj, cluster_dict.get( (getattr(obj, attr1), getattr(obj, attr2)))) for obj in objs), key=get_1
    )

    grouped = itertools.groupby(cluster_tuples, key=get_1)

    clusters = [list(map(get_0, v)) for k, v in grouped]

    return clusters

def get_bbox_from_objects(objects):
    is_dict = False
    if len(objects) > 0 and isinstance(objects[0], dict):
        is_dict=True

    if is_dict:
        return (
            min(map(itemgetter("left"), objects)),
            min(map(itemgetter("top"), objects)),
            max(map(itemgetter("right"), objects)),
            max(map(itemgetter("bottom"), objects)),
        )
    else:
        return (
            min([o.left for o in objects]),
            min([o.top for o in objects]),
            max([o.right for o in objects]),
            max([o.bottom for o in objects])
        )

def calculate_area(bbox):
    left, top, right, bottom = bbox.left, bbox.top, bbox.right, bbox.bottom

    if left > right or top > bottom:
        raise ValueError(f"{bbox} has a negative width or height.")
    return (right - left) * (bottom - top)

def are_equal(bbox1, bbox2):
    return int(bbox1.top)==int(bbox2.top) and int(bbox1.left)==int(bbox2.left)and int(bbox1.bottom)==int(bbox2.bottom) and int(bbox1.right)==int(bbox2.right)

def contains_objects(object, objects):

    for o in objects:
        if are_equal(o, object):
            return True
    return False


def get_BoundingBox_from_objects(objects):
    is_dict = False
    if objects is None:
        return None
    if len(objects) > 0 and isinstance(objects[0], dict):
        is_dict=True

    if is_dict:
        return BoundingBox(
            min(map(itemgetter("left"), objects)),
            min(map(itemgetter("top"), objects)),
            max(map(itemgetter("right"), objects)),
            max(map(itemgetter("bottom"), objects)),
        )
    else:
        return BoundingBox(
            min([o.left for o in objects]),
            min([o.top for o in objects]),
            max([o.right for o in objects]),
            max([o.bottom for o in objects])
        )

def parse_value(val):
    val=val.strip().replace(',', '.').replace(' ', '_').replace('/', '_')
    try:
        val = ast.literal_eval(val)
    except (ValueError, SyntaxError):
        pass
    return val


def words_to_left_edges(words, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
    """
    Find (imaginary) vertical lines that connect the left, right, or
    center of at least `word_threshold` words.
    """
    # Find words that share the same left, right, or centerpoints

    by_left = cluster_objects(words, "left", 2)
    by_right = cluster_objects(words, "right", 2)

    # Find the points that align with the most words
    by_left = list(filter(lambda x: len(x) >= word_threshold, by_left))
    by_right = list(filter(lambda x: len(x) >= word_threshold, by_right))

    #select the most aligned left an right separators. This is possible because separator edges share words.
    #the one that is aligned with most words is retained
    by_left2 = copy(by_left)
    by_right2=[]
    for left in by_left:
        for right in by_right:
            inetersection = set(left).intersection(set(right))
            if len(inetersection) > 2 and len(set(right)) >= len(set(left)):
                if left in by_left2:
                    by_left2.remove(left)
                    if right not in by_right2:
                        by_right2.append(right)

    edges = [
        BoundingBox(left=min(w.left for w in words), right=min(w.left for w in words), top=min(w.top for w in words),
                    bottom=max(w.bottom for w in words)) for words in by_left2]+[
        BoundingBox(left=max(w.right for w in words), right=max(w.right for w in words), top=min(w.top for w in words),
                    bottom=max(w.bottom for w in words)) for words in by_right2]

    return edges


def vertical_overlap(a, b):
    return max(0, min(a.bottom, b.bottom) - max(a.top, b.top))


def horizontal_overlap(a, b):
    return max(0, min(a.right, b.right) - max(a.left, b.left))


def intersecting_edges(v_edges, h_edges, x_tolerance=1, y_tolerance=1):
    """
    Given a list of edges, return the points at which they intersect
    within `tolerance` pixels.
    """
    intersections = {}

    for v in sorted(v_edges, key=lambda e: (e.left, e.top)):
        for h in sorted(h_edges, key=lambda e: (e.top, e.left)):
            if (
                    (v.top <= (h.top + y_tolerance))
                    and (v.bottom >= (h.top - y_tolerance))
                    and (v.left >= (h.left - x_tolerance))
                    and (v.left <= (h.right + x_tolerance))
            ):
                vertex = (v.left, h.top)
                if vertex not in intersections:
                    intersections[vertex] = {"v": [], "h": []}
                intersections[vertex]["v"].append(v)
                intersections[vertex]["h"].append(h)
    return intersections

def move_object(obj, axis, value):
    assert axis in ("h", "v")
    if axis == "h":
        obj.left+=value
        obj.right+=value
    if axis == "v":
        obj.top += value
        obj.bottom += value

        if hasattr(obj, "todtop"):
            obj.doctop += value

        if hasattr(obj, "y0"):
            obj.y0 -= value
            obj.y1 -= value

    return obj

def resize_object(obj, key, value):
    assert key in ("left", "right", "top", "bottom")
    old_value = getattr(obj, key)
    diff = value - old_value

    if key == "left":
        assert value <= obj.left
        obj.width= obj.right - value
    elif key == "right":
        assert value >= obj.left
        obj.width= value - obj.left
    elif key == "top":
        assert value <= obj.bottom
        obj.doctop=obj.doctop + diff
        obj.height= obj.height - diff
        if hasattr(obj, "y1"):
            obj.y1= obj.y1 - diff
    elif key == "bottom":
        assert value >= obj.top
        obj.height= obj.height + diff
        if hasattr(obj, "y0"):
            obj.y0=obj.y0 - diff
    return obj

#obj_to_bbox = getattr("left", "top", "right", "bottom")



def extract_text(
    chars, x_tolerance=DEFAULT_X_TOLERANCE, y_tolerance=DEFAULT_Y_TOLERANCE
):

    if len(chars) == 0:
        return None

    chars = list(chars)
    doctop_clusters = cluster_objects(chars, "bottom", y_tolerance)

    lines = (collate_line(line_chars, x_tolerance) for line_chars in doctop_clusters)

    coll = "\n".join(lines)
    return coll


collate_chars = extract_text


def snap_objects(objs, attr, tolerance):
    if objs ==[]:
        return []
    axis = {"left": "h", "right": "h", "top": "v", "bottom": "v"}[attr]
    clusters = cluster_objects(objs, attr, tolerance)

    avgs = [sum(map(getattr, objs, (attr,)*len(objs))) / len(objs) for objs in clusters]

    snapped_clusters = [
        [move_object(obj, axis, avg - getattr(obj, attr)) for obj in cluster]
        for cluster, avg in zip(clusters, avgs)
    ]
    return list(itertools.chain(*snapped_clusters))


def obj_to_edges(obj):
    return {
        "line": lambda x: [line_to_edge(x)],
        "rect": rect_to_edges,
        "rect_edge": rect_to_edges,
        "curve": curve_to_edges,
    }[obj["object_type"]](obj)

def rects_to_edges(rectangles, lines, words, rect_threshold=DEFAULT_MIN_WORDS_VERTICAL):
    """
    Find (imaginary) vertical lines that connect the left, right, or
    center of at least `word_threshold` words.
    """
    # Find words that share the same left, right, or centerpoints
    by_left = cluster_objects(rectangles, "left", 2)
    by_bottom = cluster_objects(rectangles, "bottom", 2)
    edges = {}
    # Find the points that align with the most words
    if by_left is None:
        by_left = []
    if by_bottom is None:
        by_bottom = []

    by_left = list(filter(lambda x: len(x) >= rect_threshold, by_left))
    by_bottom = list(filter(lambda x: len(x) >= rect_threshold, by_bottom))
    edge = {}
    edges['h'] = []
    for rects in by_bottom:
        edge = {}

        edge['axis'] = BoundingBox(left=min(rect.left for rect in rects), right=max(rect.right for rect in rects),
                                   top=min(rect.bottom for rect in rects),
                                   bottom=min(rect.bottom for rect in rects))
        edge['components'] = get_partially_overlapping_objects(edge['axis'], rectangles)
        edge['bbox'] = BoundingBox(left=min(rect.left for rect in edge['components']),
                                   right=max(rect.right for rect in edge['components']) + 5,
                                   top=min(rect.top for rect in edge['components']) - 10,
                                   bottom=max(rect.bottom for rect in edge['components']))

        edge['lines'] = get_partially_overlapping_objects(edge['bbox'], lines)
        if len(edge['lines']) > 0:
            edge['bbox'].left = min(edge['bbox'].left, min([l.left for l in edge['lines']]))
            edge['bbox'].right = max(edge['bbox'].left, max([l.right for l in edge['lines']]))
        sizes=set([int(r.bottom - r.top) for r in edge['components']])
        if len(sizes)>2:
            edges['h'].append(edge)

    edges['v'] = []
    for rects in by_left:
        edge = {}
        edge['axis'] = BoundingBox(left=min(rect.left for rect in rects), right=min(rect.left for rect in rects),
                                   top=min(rect.top for rect in rects),
                                   bottom=max(rect.bottom for rect in rects))
        edge['components'] = get_partially_overlapping_objects(edge['axis'], rectangles)
        edge['bbox'] = BoundingBox(left=min(rect.left for rect in edge['components']),
                                   right=max(rect.right for rect in edge['components']),
                                   top=min(rect.bottom for rect in edge['components']),
                                   bottom=max(rect.bottom for rect in edge['components']))
        edge['lines'] = get_partially_overlapping_objects(edge['bbox'], lines)
        if len(edge['lines']) > 0:
            edge['bbox'].left = min(edge['bbox'].left, min([l.left for l in edge['lines']]))
            edge['bbox'].right = max(edge['bbox'].left, max([l.right for l in edge['lines']]))

        edges['v'].append(edge)

    intersection_text = intersecting_edges([e['axis'] for e in edges['v']], words, x_tolerance=-1, y_tolerance=1)

    # if the edge intersect text we typically crossed to an other chart or rectangle. We split and recompute
    for k, v in intersection_text.items():
        vertical = v['v'][0]
        top = k[1]
        for edge in edges['v']:
            if edge['axis'] == vertical:
                top_components = [c for c in edge['components'] if c.bottom < top]
                remaining_components = edge['components'] = [c for c in edge['components'] if c.top > top]
                if len(top_components) >= 3:
                    edge['components'] = top_components
                    edge['axis'] = BoundingBox(left=min(rect.left for rect in edge['components']),
                                               right=min(rect.left for rect in edge['components']),
                                               top=min(rect.top for rect in edge['components']),
                                               bottom=max(rect.bottom for rect in edge['components']))

                if len(remaining_components) >= 3:  # create new edge
                    edge2 = {}
                    edge2['axis'] = BoundingBox(left=min(rect.left for rect in remaining_components),
                                                right=min(rect.left for rect in remaining_components),
                                                top=min(rect.top for rect in remaining_components),
                                                bottom=max(rect.bottom for rect in remaining_components))
                    edge2['components'] = remaining_components
                    edge2['bbox'] = BoundingBox(left=min(rect.left for rect in edge2['components']),
                                                right=max(rect.right for rect in edge2['components']),
                                                top=min(rect.bottom for rect in edge2['components']),
                                                bottom=max(rect.bottom for rect in edge2['components']))
                    edge2['lines'] = get_partially_overlapping_objects(edge2['bbox'], lines)
                    if len(edge2['lines']) > 0:
                        edge2['bbox'].left = min(edge2['bbox'].left, min([l.left for l in edge2['lines']]))
                        edge2['bbox'].right = max(edge2['bbox'].left, max([l.right for l in edge2['lines']]))
                    edges['v'].append(edge2)


    #Do the same on the horisental graphs

    intersection_text = intersecting_edges(words, [e['axis'] for e in edges['h']], x_tolerance=-1, y_tolerance=1)

    # if the edge intersect text we typically crossed to an other chart or rectangle. We split and recompute
    for k, v in intersection_text.items():
        vertical = v['h'][0]
        left = k[0]
        for edge in edges['h']:
            if edge['axis'] == vertical:
                top_components = [c for c in edge['components'] if c.left < left]
                remaining_components = edge['components'] = [c for c in edge['components'] if c.left > left]
                if len(top_components) >= 3:
                    edge['components'] = top_components
                    edge['axis'] = BoundingBox(left=min(rect.left for rect in edge['components']),
                                               right=max(rect.right for rect in edge['components']),
                                               top=min(rect.bottom for rect in edge['components']),
                                               bottom=min(rect.bottom for rect in edge['components']))

                if len(remaining_components) >= 3:  # create new edge
                    edge2 = {}
                    edge2['axis'] = BoundingBox(left=min(rect.left for rect in remaining_components),
                                                right=max(rect.right for rect in remaining_components),
                                                top=min(rect.bottom for rect in remaining_components),
                                                bottom=min(rect.bottom for rect in remaining_components))
                    edge2['components'] = remaining_components
                    edge2['bbox'] = BoundingBox(left=min(rect.left for rect in edge2['components']),
                                                right=max(rect.right for rect in edge2['components']),
                                                top=min(rect.bottom for rect in edge2['components']),
                                                bottom=max(rect.bottom for rect in edge2['components']))
                    edge2['lines'] = get_partially_overlapping_objects(edge2['bbox'], lines)
                    if len(edge2['lines']) > 0:
                        edge2['bbox'].left = min(edge2['bbox'].left, min([l.left for l in edge2['lines']]))
                        edge2['bbox'].right = max(edge2['bbox'].left, max([l.right for l in edge2['lines']]))
                    edges['h'].append(edge2)



    intersection_data = intersecting_edges([e['axis'] for e in edges['v']], [e['axis'] for e in edges['h']],
                                           x_tolerance=-1, y_tolerance=1)
    intersections = set(
        [v['v'][0] for k, v in intersection_data.items()] + [v['h'][0] for k, v in intersection_data.items()])

    edges['v'] = [e for e in edges['v'] if e['axis'] not in intersections]
    edges['h'] = [e for e in edges['h'] if e['axis'] not in intersections]

    return edges

def get_fonts_statistics(texlines):
    if len(texlines)==0:
        return {}

    sizes = [word.font_size for line in texlines for token in line for word in token.original_words]
    font_names = [word.font_name for line in texlines for token in line for word in token.original_words]
    interlines = [int(i[0].top-j[0].bottom) for i, j in zip(texlines[1:], texlines[:-1])]
#    ncolors = [word.font_ncolor for line in texlines for token in line for word in token.original_words]
    font_sizes_by_frequency=sorted(set(sizes), key = lambda ele: -sizes.count(ele))
    font_names_by_frequency=sorted(set(font_names), key = lambda ele: -sizes.count(ele))

    return {
        'most_frequent': max(set(sizes), key=sizes.count),
        'largest': max(sizes),
        'average': mean(sizes),
        'size_by_frequency': font_sizes_by_frequency,
        'name_by_frequency': font_names_by_frequency,
        'second_largest': sorted(font_sizes_by_frequency)[-2] if len(font_sizes_by_frequency)>1 else -1,
        'interline': max(set(interlines), key=interlines.count)  if len(interlines)>1 else -1,
#        'scolors': max(set(scolors), key=scolors.count),
        'name': max(set(font_names), key=font_names.count)
    }

def find_line_structure(tokens):
        lines = []

        i = 0
        while i < len(tokens):

            token=tokens[i]
            next_token=None
            if i+1<len(tokens):
                next_token = tokens[i + 1]



            line = [token]

            while next_token and  are_in_same_line2(token, next_token):
                line.append(next_token)
                i+=1
                if i >= len(tokens)-1:
                    break

                token=next_token
                next_token = tokens[i + 1]


            line=sorted(line, key=lambda elem: elem.left)
            lines.append(line)
            i+=1

        return lines
