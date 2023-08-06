class PDFParserError(Exception):
    pass


# Components
class PageNotFoundError(PDFParserError):
    pass


class NoTokensOnPageError(PDFParserError):
    pass


# Filtering
class NoTokenFoundError(PDFParserError):
    pass


class MultipleTokensFoundError(PDFParserError):
    pass


class TokenOutOfRangeError(PDFParserError):
    pass


# PDFParagraphing
class InvalidPDFParagraphError(PDFParserError):
    pass


class ParagraphNotFoundError(PDFParserError):
    pass


# Tables
class TableExtractionError(PDFParserError):
    pass


class InvalidTableError(PDFParserError):
    pass


class InvalidTableHeaderError(PDFParserError):
    pass


class InvalidCoordinatesError(PDFParserError):
    pass

class PDFParserError(Exception):
    pass


# Components
class PageNotFoundError(PDFParserError):
    pass


class NoElementsOnPageError(PDFParserError):
    pass


# Filtering
class NoElementFoundError(PDFParserError):
    pass


class MultipleElementsFoundError(PDFParserError):
    pass


class ElementOutOfRangeError(PDFParserError):
    pass


# Sectioning
class InvalidSectionError(PDFParserError):
    pass


class SectionNotFoundError(PDFParserError):
    pass

