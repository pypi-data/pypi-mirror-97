from typing import Dict, Generator, ValuesView, TYPE_CHECKING

from collections import defaultdict
import statistics
from pdf2txt.exceptions import ParagraphNotFoundError
import numpy as np
from enum import Enum
from itertools import chain
from string import digits
from pdf2txt.core.indexer import *
if TYPE_CHECKING:
    from pdf2txt.core import Document, Token




def extract(textlines):

        if len(textlines)<=2:
            return [textlines]

        # normalizing the line gaps to get an average gap for detetcting the paraagarphs
        line_gap_list=[j[0].bottom-i[0].bottom+(1+j[0].is_bold)*j[0].font_size for i, j in zip(textlines[:-1], textlines[1:])]
#        line_gap_list = [line.space_above+line.tokens[0].font_size for line in textlines if line.space_above != -1]
        if len(line_gap_list)<len(textlines):
            line_gap_list.insert(0,max(line_gap_list) if len(line_gap_list) else 0)
        #	curr_line=[line.Text for line in textlines]

        if len(line_gap_list) <= 3:
            return [textlines]

        # Now we need the 2nd order derivative so that we can  get the
        # global maxima to get the paragraphs
        # 2nd order derivative is defined as :
        # f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
        # f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
        # we only need the derivative in the y direction here

        derivative_line_gap = line_gap_list
        for i in range(0, len(line_gap_list) - 1):
            derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i + 1] - 2 * line_gap_list[i]

        # removing outliers
        outlier_cut_off = statistics.stdev(derivative_line_gap)
        derivative_line_gap2 = [d for d in derivative_line_gap if abs(d) < 2*outlier_cut_off]
        cut_off = 0.9*statistics.stdev(derivative_line_gap2)
        if cut_off < 2:
            return [textlines]

        #	cut_off=statistics.stdev(derivative_line_gap)

        derivative_line_gap = list(map(lambda x: 0 if abs(x) < cut_off else x, derivative_line_gap))

        zero_crossings = np.where(np.diff(np.sign(derivative_line_gap)) == -2)[0]+1
        zero_crossings = zero_crossings.tolist()

        # checkjing how many are there with a line gap of less than 1
        # forming the paragraph:
        if 2 in zero_crossings:
            zero_crossings.remove(2)
        if len(zero_crossings) == 0:
            return [textlines]

        # split array in ranges
        for i in range(len(zero_crossings)):
            if zero_crossings[i] == i:
                zero_crossings[i] = i + 1
        zero_crossings.insert(0, 0)
        zero_crossings.insert(len(zero_crossings), len(textlines))

        paragraph_ranges = [(zero_crossings[i], zero_crossings[i + 1]) for i in range(len(zero_crossings) - 1)]
        paragraphs= [textlines[i:j] for i, j in paragraph_ranges]

        return paragraphs


def extract2(textlines):
    if len(textlines) <= 2:
        return [textlines]

    # normalizing the line gaps to get an average gap for detetcting the paraagarphs
    line_gap_list = [j[0].bottom - i[0].bottom + j[0].font_size for i, j in
                     zip(textlines[:-1], textlines[1:])]
    #        line_gap_list = [line.space_above+line.tokens[0].font_size for line in textlines if line.space_above != -1]
    if len(line_gap_list) < len(textlines):
        line_gap_list.insert(0, max(line_gap_list) if len(line_gap_list) else 0)
    #	curr_line=[line.Text for line in textlines]

    if len(line_gap_list) <= 3:
        return [textlines]

    # Now we need the 2nd order derivative so that we can  get the
    # global maxima to get the paragraphs
    # 2nd order derivative is defined as :
    # f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
    # f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
    # we only need the derivative in the y direction here

    derivative_line_gap = line_gap_list
    for i in range(0, len(line_gap_list) - 1):
        derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i + 1] - 2 * line_gap_list[i]

    # removing outliers
    outlier_cut_off = statistics.stdev(derivative_line_gap)
    derivative_line_gap2 = [d for d in derivative_line_gap if abs(d) < 2 * outlier_cut_off]
    cut_off = 0.9 * statistics.stdev(derivative_line_gap2)
    if cut_off < 2:
        return [textlines]

    #	cut_off=statistics.stdev(derivative_line_gap)

    derivative_line_gap = list(map(lambda x: 0 if abs(x) < cut_off else x, derivative_line_gap))

    zero_crossings = np.where(np.diff(np.sign(derivative_line_gap)) == -2)[0] + 1
    zero_crossings = zero_crossings.tolist()

    # checkjing how many are there with a line gap of less than 1
    # forming the paragraph:
    if 2 in zero_crossings:
        zero_crossings.remove(2)
    if len(zero_crossings) == 0:
        return [textlines]

    # split array in ranges
    for i in range(len(zero_crossings)):
        if zero_crossings[i] == i:
            zero_crossings[i] = i + 1
    zero_crossings.insert(0, 0)
    zero_crossings.insert(len(zero_crossings), len(textlines))

    paragraph_ranges = [(zero_crossings[i], zero_crossings[i + 1]) for i in range(len(zero_crossings) - 1)]
    paragraphs = [textlines[i:j] for i, j in paragraph_ranges]

    return paragraphs



class ContentType(Enum):
    Text=1
    Table=2
    Graph=3

class Paragraph:
    """
    A continuous group of tokens within a document.

    A paragraph is intended to label a group of tokens. Said tokens must be continuous
    in the document.

    Warning:
        You should not instantiate a PDFParagraph class yourself, but should call
        `create_paragraph` from the `PDFParagraphing` class below.

    Args:
        document (PDFDocument): A reference to the document.
        name (str): The name of the paragraph.
        unique_name (str): Multiple paragraphs can have the same name, but a unique name
            will be generated by the PDFParagraphing class.
        start_token (PDFToken): The first token in the paragraph.
        end_token (PDFToken): The last token in the paragraph.
    """

    document: "Document"
    name: str
    unique_name: str
    start_token: "Token"
    end_token: "Token"

    def __init__(self, document, name, unique_name, paragraph_number):
        self.document = document
        self.name = name
        self.unique_name = unique_name
        self.title = None
        self.number=paragraph_number

    @property
    def content(self):
        if not hasattr(self, "_content"):
            self._content=[]

        return self._content


    def add_content(self, content, type):

        if type==ContentType.Text:
            for token in content:
                token.paragraph=self


        self.content.append({'type':type, 'content':content})
        if len(self.content) >=2 and self.content[-1]['type']== ContentType.Table and self.content[-2]['type']==ContentType.Table:
            table1 = self.content[-1]['content']
            table2 = self.content[-2]['content']
            if len(table1.columns)==len(table2.columns):
                try:
                    table2=table2.columns.to_frame().T.append(table2, ignore_index=True)
                    table2.columns = [''] * len(table2.columns)

                    table1=table1.columns.to_frame().T.append(table1, ignore_index=True)
                    table1.columns = [''] * len(table1.columns)
                    table1=table1.append(table2)
                    table1=table1.dropna(axis=1, how='all')
                    self._content=self._content[:-1]
                    self._content[-1]['content']=table1
                except Exception as e:
                    pass





    @property
    def Text(self):
        return_str=""
        if self.title:
            return_str = ' '.join([t.Text for t in self.title]) + '\n'
            return_str += '-' * len(return_str)
        for content in self.content:
            if content["type"]==ContentType.Text:
                return_str += '\n' + ' '.join([c.Text for c in content["content"]])
            elif content["type"]==ContentType.Graph:
                return_str+="<START GRAPH DATA>\n"
                return_str+='\n'+content["content"].to_string(index=False)
                return_str+="\n<END GRAPH DATA>"
            elif content["type"]==ContentType.Table:
                return_str+="\n<START TABLE>\n"
                return_str+='\n'+content["content"].to_string(index=False)
                return_str+="\n<END TABLE>"
        return return_str


    def __eq__(self, other: object) -> bool:
        """
        Returns True if the two paragraphs have the same unique name and are from the
        same document
        """
        if not isinstance(other, Paragraph):
            raise NotImplementedError(f"Can't compare PDFParagraph with {type(other)}")
        return all(
            [
                self.document == other.document,
                self.unique_name == other.unique_name,
                self.start_token == other.start_token,
                self.end_token == other.end_token,
                self.__class__ == other.__class__,
            ]
        )

    def __len__(self):
        """
        Returns the number of tokens in the paragraph.
        """
        return len(self.text_lines)
    @property
    def text_lines(self):
        if hasattr(self, "_text_lines"):
            return self._text_lines

        self._text_lines=[c for c in self.content if c["type"]==ContentType.Text]
        return self._text_lines

    def __repr__(self):
        return (
            f"<PDFParagraph name: '{self.name}', unique_name: '{self.unique_name}', "
            f"number of tokens: {len(self)}>"
        )
    def filter_by_text_contains(self, texts: str, filter_type='any', case_sensitive=True, substring_match=False):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE
        regex_str='|'.join(texts)
        regex_str=r'\b('+regex_str+')'
        regex = re.compile(regex_str, flags=flags)

        if filter_type=='any' or len(texts)==1:
            lines = [line['content'] for line in self.text_lines if regex.search('\n'.join([token.Text for token in line['content']]))]
        elif filter_type=='all':
            lines = [line for line in self.text_lines if all(x in self.Text for x in texts)]
        else:
            raise Exception("Unknown filter type. Should be: 'any' or 'all'")


        return lines


class Paragraphs:
    """
    A paragraphing utilities class, made available on all PDFDocuments as ``.paragraphing``.
    """

    document: "Document"
    name_counts: Dict[str, int]
    paragraphs_dict: Dict[str, Paragraph]

    def __init__(self, document: "Document"):
        self.paragraphs_dict = {}
        self.paragraphs_dict_by_number = {}
        self.name_counts = defaultdict(int)
        self.document = document
        self.inverted_index=None
        self.docnumbers=[]


    def create_paragraph(  self, name=None):
        """
        Creates a new paragraph with the specified name.

        Creates a new paragraph with the specified name, starting at `start_token` and
        ending at `end_token` (inclusive). The unique name will be set to name_<idx>
        where <idx> is the number of existing paragraphs with that name.

        Args:
            name (str): The name of the new paragraph.
            start_token (PDFToken): The first token in the paragraph.
            end_token (PDFToken): The last token in the paragraph.
            include_last_token (bool): Whether the end_token should be included in
                the paragraph, or only the tokens which are strictly before the end
                token. Default: True (i.e. include end_token).

        Returns:
            Paragraph: The created paragraph.

        Raises:
            InvalidPDFParagraphError: If a the created paragraph would be invalid. This is
                usually because the end_token comes after the start token.
        """

        if name==None:
            name="paragraph"+str(len(self.document.paragraphs.paragraphs))
        current_count = self.name_counts[name]
        unique_name = f"{name}_{current_count}"
        self.name_counts[name] += 1

        paragraph = Paragraph(self.document, name, unique_name, paragraph_number=len(self.document.paragraphs.paragraphs))
        self.paragraphs_dict[unique_name] = paragraph
        self.paragraphs_dict_by_number[paragraph.number]=unique_name
        self.docnumbers.append(paragraph.number)
        return paragraph

    def get_paragraphs_with_name(self, name: str) -> Generator[Paragraph, None, None]:
        """
        Returns a list of all paragraphs with the given name.
        """
        return (
            self.paragraphs_dict[f"{name}_{idx}"]
            for idx in range(0, self.name_counts[name])
        )

    def get_paragraph(self, unique_name: str) -> Paragraph:
        """
        Returns the paragraph with the given unique name.

        Raises:
            PDFParagraphNotFoundError: If there is no paragraph with the given unique_name.
        """
        try:
            return self.paragraphs_dict[unique_name]
        except KeyError as err:
            raise ParagraphNotFoundError(
                f"Could not find paragraph with name {unique_name}"
            ) from err

    @property
    def paragraphs(self) -> ValuesView[Paragraph]:
        """
        Returns the list of all created PDFParagraphs.
        """
        return self.paragraphs_dict.values()


    def filter_by_title_equal(self, text: str):
        """
        Filter for tokens whose text is exactly the given string.

        Args:
            text (str): The text to filter for.
            stripped (bool, optional): Whether to strip the text of the token before
                comparison. Default: True.

        Returns:
            LineList: The filtered list.
        """

        return [paragraph for paragraph in self.paragraphs_dict.values() if paragraph.title == text]

    def filter_by_title_contains(self, text: str):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """


        paragraphs= [paragraph for paragraph in self.paragraphs_dict.values() if paragraph.title is not None and text in paragraph.title.Text]


        return paragraphs

    def filter_by_text_contains(self, texts: str, filter_type='any', case_sensitive=True, substring_match=False):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE
        texts=[re.escape(t) for t in texts]
        regex_str='|'.join(texts)
        regex_str=r'\b('+regex_str+')'
        regex = re.compile(regex_str, flags=flags)

        if filter_type=='any' or len(texts)==1:
            paragraphs = [paragraph for paragraph in self.paragraphs_dict.values() if regex.search(paragraph.Text)]
        elif filter_type=='all':
            paragraphs=[paragraph for paragraph in self.paragraphs_dict.values() if all(x in paragraph.Text for x in texts)]
        else:
            raise Exception("Unknown filter type. Should be: 'any' or 'all'")





        return paragraphs


    def filter_by_text_matches_regex(self, regex_str, case_sensitive=True):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE

        regex = re.compile(regex_str, flags=flags)

        paragraphs = [paragraph for paragraph in self.paragraphs_dict.values() if regex.search(paragraph.Text)]

        return paragraphs


    def get_last_paragraph(self):
        if len(self.paragraphs_dict.values())==0:
            return None
        return list(self.paragraphs_dict.values())[-1]

    def _getpositions(self, term):
        # For a term, retrieves a list of all positions from the inverted index.

        if term in self.inverted_index:
            index = self.inverted_index[term]
            return index

        return {}

    def getnot(self, lst_paragraph):
        # takes list of documents and returns the all documents in collection except those in list.

        all_docs = sorted(list(set(self.docnumbers)))
        return [n for n in ([int(x) for x in all_docs]) if n not in lst_paragraph]

    def get_docs(self, position_list):
        # extracts the documents from a list of {doc:[position]} dictionaries

        docs = []
        for doc in position_list:
            docs.append(doc)
        return docs

    def _phrase_search(self, i, phrase):
        # used for both phrase search and proximity search.
        # if phrase search, i=1, if proximity search, i is passed from proximity search method.

        phrase = re.sub('"', '', phrase)
        term1, term2 = phrase.split(' ')
        term1_positions = self._getpositions(term1)
        term2_positions = self._getpositions(term2)
        results = []

        # loops through all positions that both terms occur in and adds to list if distance between terms <= i.

        for position in term1_positions:
            for key in position:
                term1_doc = key
                term1_pos = position[key]

                for position2 in term2_positions:
                    for key2 in position2:
                        term2_doc = key2
                        term2_pos = position2[key2]

                        if term1_doc == term2_doc:
                            for p in term1_pos:
                                for p2 in term2_pos:
                                    if abs(p - p2) <= i:
                                        results.append(position)
                                        results.append(position2)

        return results  # return list of postions

    def _proximity_search(self, query):
        # format query and send to phrase search with i being the distance given.

        query = re.sub('#', '', query)
        i, query = query.split('(')
        query = re.sub(r'([^\s\w]|_)+', '', query)
        results = self._phrase_search(int(i), query)

        return list(set(self.get_docs(results)))

    def _boolean_search(self, query):
        # Gets type of boolean query, splits into the two terms mentioned.

        results = []

        if 'AND NOT' in query:
            idx1 = query.index('AND')
            idx2 = idx1 + 7
        elif 'OR NOT' in query:
            idx1 = query.index('OR')
            idx2 = idx1 + 6
        elif 'AND' in query:
            idx1 = query.index('AND')
            idx2 = idx1 + 3
        elif 'OR' in query:
            idx1 = query.index('OR')
            idx2 = idx1 + 2

        term1 = query[:idx1].strip()
        term2 = query[idx2:].strip()

        # If either term is a phrase search then get results from phrase method.

        if term1.startswith('"') and term1.endswith('"'):
            term1_positions = self._phrase_search(1, term1)
        else:
            term1_positions = self._getpositions(term1)
        if term2.startswith('"') and term2.endswith('"'):
            term2_positions = self._phrase_search(1, term2)
        else:
            term2_positions = self._getpositions(term2)

        # Convert to list of documents without indexes

        term1_positions = self.get_docs(term1_positions)
        term2_positions = self.get_docs(term2_positions)

        if 'NOT' in query:
            term2_positions = self.getnot(term2_positions)  # revert list

        if 'AND' in query:
            results = list(set(term1_positions) & set(term2_positions))
        if 'OR' in query:
            results = list(set(term1_positions) | set(term2_positions))

        return results

    def _rank_search(self, query):
        # gets list of positions for each term in the query and calculates tfidf score for each document

        query = query.split(' ')
        N = len(list(set(self.docnumbers)))
        tfidfs = {}  # Dictionary to store {docnumber: tfidf score}

        def tfidf(tf, df):
            return (1 + np.log10(tf)) * (np.log10(N / df))

        for term in query:
            positions = self._getpositions(term)
            docfreq = len(positions)

            for doc in positions:
                termfreq = len(positions[doc])
                t = tfidf(termfreq, docfreq)

                if doc not in tfidfs.keys():
                    tfidfs[doc] = t
                else:
                    newval = tfidfs[doc].__add__(t)
                    tfidfs[doc] = newval
        return tfidfs

    def search(self, query):

        results = []    # list of positions
        querytype = "not_ir"       # variable used to decide which print/save method to use for rank or bool/phrase query
        results_string = []
        if self.inverted_index is None:
            self.inverted_index=build_index(self.document)
        # check structure of query to send to appropriate search method

        if 'AND' in query or 'OR' in query:
            results = self._boolean_search(query)

        elif query.startswith('#') and query.endswith(")"):
            results = self._proximity_search(query)

        elif query.startswith('"') and query.endswith('"'):
            positions = self._phrase_search(1, query)
            t = []
            for p in positions:
                for key in p:
                    t.append(key)
            results.extend(list(set(t)))

        elif len(query.split(' ')) == 1: # single word query
            for item in self._getpositions(query):
                for key in item.keys():
                    results.append(key)
        else:
            querytype = "IR"
            results = self._rank_search(query)

        if isinstance(results, list):
            results_string.extend([self.paragraphs_dict[self.paragraphs_dict_by_number[n]] for n in results])
        else:#
            querytype = "IR"
            for doc, score in results.items():
                if score == 0.0:
                    results.pop(doc)
            results = (sorted(results.items(), key=lambda kv: kv[1], reverse=True))
            for item in results:
                doc, score = item
                results_string.append(self.paragraphs_dict[self.paragraphs_dict_by_number[doc]])

        return results_string