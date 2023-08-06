from pdf2txt.utils import get_BoundingBox_from_objects,BoundingBox
from collections import Counter
from pdf2txt.settings import DEFAULT_X_TOLERANCE, DEFAULT_Y_TOLERANCE, DEFAULT_TOKEN_EXTRACTION_SETTINGS
import copy
from pdf2txt.utils import are_in_same_Line


exceptions=['▪', 'l', '(%)']

class TokenExtractor:
    def __init__(self, page, **settings):

        for s, val in settings.items():
            if s not in DEFAULT_TOKEN_EXTRACTION_SETTINGS:
                raise ValueError(f"{s} is not a valid WordExtractor parameter")

            setattr(self, s, val)

        self.page=page

    def word_begins_new_token(self, current_word, next_word):



        if current_word.font!=next_word.font and (next_word.Text not in exceptions and  current_word.Text not in exceptions):
            return True
        if self.fixed_width:
            intraline_tol = self.x_tolerance * 3

        else:
            intraline_tol = next_word.font_width * 1.3

        interline_tol = self.y_tolerance

        return (
            (next_word.left > current_word.right + intraline_tol)
            or (next_word.right < current_word.left - intraline_tol)
            or (next_word.top > current_word.bottom - interline_tol)
            or (next_word.bottom < current_word.top + interline_tol)
        )

    def iter_words_to_tokens(self, words):
        current_token =None

        for word in words:
            if not current_token:
                current_token = Token(word, page=self.page)

            elif current_token and self.word_begins_new_token(current_token, word):
                yield current_token
                current_token = Token(word, page=self.page)

            else:
                current_token.add(word)

        if current_token:

            yield current_token


    def iter_sort_words2(self, words):
        words.sort(key=lambda x: (x.bottom))
        lines = []
        i = 0
        line=[words[0]]
        while i < len(words) - 1:
            if are_in_same_Line(words[i], words[i+1]):
                line.append( words[i+1])
            else:
                lines.append(sorted(line, key=lambda x: x.x0))
                line=[words[i+1]]
            i+=1
        lines.append(sorted(line, key=lambda x: x.x0))
        return lines

    def iter_sort_words(self, words):
        for word in sorted(words, key=lambda x: (x.bottom, x.x0)):
            yield word

    def iter_extract(self, words):
        words=self.iter_sort_words2(words)
        words = [w for line in words for w in line]#self.iter_sort_words(words)

        for token in self.iter_words_to_tokens(words):
            yield token



    def extract(self, words):
        return list(self.iter_extract(words))

class Token(BoundingBox):

    def __init__(self, word, page, index=-1, **kwargs):

#        super().__init__(**kwargs)
        self.page = page
        self.original_words = []
        self.add(word)
        self._index = index
        self.paragraph=None
    @staticmethod
    def copy( token):
        words=copy.copy(token.original_words)
        newtoken=Token(words[0], token.page)
        for w in words[1:]:
            newtoken.add(w)
        return newtoken

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Token):
            return self.Text == other.Text and self.left == other.left and self.top == other.top
        return False

    def __repr__(self):
        return '<' + self.Text + '>'

    def __str__(self):
        return self.Text

    def __hash__(self):
        return hash(str(self ) +str(self._index))

    def partially_within(self, bbox) -> bool:
        """
        Whether any part of the element is within the bounding box.

        Args:
            bbox (BoundingBox): The bounding box to check whether the element
                is partially within.

        Returns:
            bool: True if any part of the element is within the bounding box.
        """
        return all(
            [
                bbox.left <= self.right,
                bbox.right >= self.left,
                bbox.top <= self.bottom,
                bbox.bottom >= self.top,
            ]
        )

    def within(self, bbox, tollerance=2) -> bool:
        """
        Whether any part of the element is within the bounding box.

        Args:
            bbox (BoundingBox): The bounding box to check whether the element
                is partially within.

        Returns:
            bool: True if any part of the element is within the bounding box.
        """
        return all(
            [
                bbox.left < self.left,
                bbox.right > self.right,
                bbox.top-tollerance <= self.top,
                bbox.bottom+tollerance >= self.bottom,
            ]
        )

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
        return ' '.join([e.Text for e in self.original_words])

    @property
    def width(self):
        return self.right-self.left

    @property
    def left(self):
        return self.bbox.left

    @property
    def right(self):
        return self.bbox.right
    @right.setter
    def right(self, value):
        self.bbox.right=value

    @left.setter
    def left(self, value):
        self.bbox.left=value

    @property
    def top(self):
        return self.bbox.top

    @property
    def bottom(self):
        return self.bbox.bottom

    def add(self, other):
        self.original_words.append(other)
        self.bbox=get_BoundingBox_from_objects(self.original_words)
        return self

    def combine(self, other_token):
        self.original_words.extend(other_token.original_words)
        self.bbox=get_BoundingBox_from_objects(self.original_words)
        return self


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

        if hasattr(self, "_font_size"):
            return self._font_size

        counter = Counter(
            (
                word.font_size
                for word in self.original_words
            )
        )
        self._font_size = counter.most_common(1)[0][0]

        return self._font_size


    @property
    def font_name(self) -> float:
        """
        The size of the font.

        This will be taken from the pdf itself, using the most common size within all
        the characters in the element.

        Returns:
            float: The font size of the element, rounded to the font_size_precision of
                the document.
        """

        if hasattr(self, "_font_name"):
            return self._font_name

        counter = Counter(
            (
                word.font_name
                for word in self.original_words
            )
        )
        self._font_name = counter.most_common(1)[0][0]

        return self._font_name

    @property
    def font(self):
        return self.font_name+'+'+str(self.font_size)

    @property
    def is_bold(self):
        return 'bold' in self.font_name.lower()