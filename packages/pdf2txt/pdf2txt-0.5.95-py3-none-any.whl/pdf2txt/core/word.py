from pdf2txt.settings import DEFAULT_WORD_EXTRACTION_SETTINGS
from pdf2txt.utils import BoundingBox, cluster_objects, get_bbox_from_objects
from operator import itemgetter
import itertools
from collections import Counter

class WordExtractor:
    def __init__(self, page, **settings):
        for s, val in settings.items():
            if s not in DEFAULT_WORD_EXTRACTION_SETTINGS:
                raise ValueError(f"{s} is not a valid WordExtractor parameter")

            setattr(self, s, val)
            self.keep_blank_chars=False
            self.page=page
    def merge_chars(self, ordered_chars):
        x0, top, x1, bottom = get_bbox_from_objects(ordered_chars)
        upright = ordered_chars[0]["upright"]

        direction = 1 if (self.horizontal_ltr if upright else self.vertical_ttb) else -1

        word = {
            "text": "".join(map(itemgetter("text"), ordered_chars)),
            "left": x0,
            "right": x1,
            "top": top,
            "bottom": bottom,
            "upright": upright,
            "direction": direction,
            "chars": ordered_chars
        }

        for key in self.extra_attrs:
            word[key] = ordered_chars[0][key]

        return Word(word, page=self.page)

    def char_begins_new_word(self, current_chars, next_char):
        upright = current_chars[0]["upright"]
        intraline_tol = next_char["width"]/3 if upright else self.y_tolerance
        interline_tol = self.y_tolerance if upright else self.x_tolerance

        word_x0, word_top, word_x1, word_bottom = get_bbox_from_objects(current_chars)

        return (
            (next_char["left"] > word_x1 + intraline_tol)
            or (next_char["right"] < word_x0 - intraline_tol)
            or (next_char["top"] > word_bottom - interline_tol)
            or (next_char["bottom"] <  word_top + interline_tol)
        )

    def iter_chars_to_words(self, chars):
        current_word = []

        for char in chars:
            if not self.keep_blank_chars and char["text"].isspace():
                if current_word:
                    yield current_word
                    current_word = []

            elif current_word and self.char_begins_new_word(current_word, char):
                yield current_word
                current_word = [char]

            else:
                current_word.append(char)

        if current_word:

            yield current_word

    def iter_sort_chars(self, chars):
        def upright_key(x):
            return -int(x["upright"])

        for upright_cluster in cluster_objects(chars, upright_key, 0):
            upright = upright_cluster[0]["upright"]
            cluster_key = "bottom" if upright else "left"

            # Cluster by line
            subclusters = cluster_objects(
                upright_cluster, cluster_key, self.y_tolerance
            )

            for sc in subclusters:
                # Sort within line
                sort_key = "left" if upright else "bottom"
                sc = sorted(sc, key=itemgetter(sort_key))

                # Reverse order if necessary
                if not (self.horizontal_ltr if upright else self.vertical_ttb):
                    sc = reversed(sc)

                yield from sc

    def iter_extract(self, chars):
#        if not self.use_text_flow:
#            chars = list(self.iter_sort_chars(chars))

        grouping_key = itemgetter("upright", *self.extra_attrs)
        grouped = itertools.groupby(chars, grouping_key)

        for keyvals, char_group in grouped:
            for word_chars in self.iter_chars_to_words(char_group):
                yield self.merge_chars(word_chars)

    def extract(self, chars):
        return list(self.iter_extract(chars))

class Word(BoundingBox):
    _index = -1
    __font_name = None
    __font_size = None
    __font_width = None
    __font_size_precision = 1
    def __init__(self, word, page=None, index=-1):

        super().__init__(word["left"], word["top"], word["right"], word["bottom"])
        self.page = page
        self.original_word = word
        self._index = index

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Word):
            return self.Text == other.Text and self.x0 == other.x0 and self.bottom == other.bottom
        return False


    def __repr__(self):
        return '<' + self.Text + '>'

    def __str__(self):
        return self.Text

    def __hash__(self):
        return hash(str(self)+str(self._index))

    @property
    def index(self):
        return self._index
    @index.setter
    def index(self, val):
        self._index=val

    @property
    def page_number(self):
        return self.page.page_number

    @property
    def Text(self):
        return self.original_word["text"]

    @property
    def font_name(self) -> str:
        """
        The name of the font.

        This will be taken from the pdf itself, using the most common font within all
        the characters in the element.

        Returns:
            str: The font name of the element.
        """
        if self.__font_name is not None:
            return self.__font_name

        counter = Counter(
            (
                character["fontname"]
                for line in self.original_tokens
                for character in line
                if "fontname" in character
            )
        )
        self.__font_name = counter.most_common(1)[0][0]
        return self.__font_name

    @property
    def font(self):
        return self.font_name+'+'+str(self.font_size)


    @property
    def x0(self):
        return self.original_word["left"]

    @property
    def x1(self):
        return self.original_word["right"]

    @property
    def font_size(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if self.__font_size is not None:
            return self.__font_size

        counter = Counter(
            (
                character["height"]
                for character in self.original_word["chars"]
                if ("height" in character)
            )
        )
        self.__font_size = round(
            counter.most_common(1)[0][0], self.__font_size_precision
        )
        return self.__font_size

    @property
    def font_width(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if self.__font_width is not None:
            return self.__font_width

        counter = Counter(
            (
                character["width"]
                for character in self.original_word["chars"]
                if ("width" in character)
            )
        )
        mc=counter.most_common(1)
        self.__font_width = round(
            counter.most_common(1)[0][0], self.__font_size_precision
        )
        return self.__font_width


    @property
    def font_name(self):
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if hasattr(self, "_fontname"):
            return self._font_name

        counter = Counter(
            (
                character["fontname"]
                for character in self.original_word["chars"]
                if ("fontname" in character)
            )
        )

        self._font_name = counter.most_common(1)[0][0]

        return self._font_name

    @property
    def font_scolor(self):
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if hasattr(self, "_font_s_color"):
            return self._font_s_color

        counter = Counter(
            (
                character["stroking_color"]
                for character in self.original_word["chars"]
                if ("stroking_color" in character)
            )
        )

        self._font_s_color = counter.most_common(1)[0][0]
        return self._font_s_color

    @property
    def font_ncolor(self):
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """
        if hasattr(self, "_font_n_color"):
            return self._font_n_color

        counter = Counter(
                (
                    frozenset(character["non_stroking_color"])
                    for character in self.original_word["chars"]
                    if ("non_stroking_color" in character and character["non_stroking_color"] is not None)
                )
            )

        self._font_n_color = counter.most_common(1)[0][0]
        return self._font_n_color

    @property
    def is_bold(self):
        return 'bold' in self.font_name.lower()

    @property
    def ignored(self) -> bool:
        """
        A flag specifying whether the element has been ignored.
        """
        return self._index in self.document._ignored_indexes
