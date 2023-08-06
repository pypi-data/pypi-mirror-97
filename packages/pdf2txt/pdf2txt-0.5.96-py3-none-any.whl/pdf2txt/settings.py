

DEFAULT_X_TOLERANCE = 2
DEFAULT_Y_TOLERANCE = 2
DEFAULT_X_SEPARATOR_WIDTH=10
DEFAULT_Y_SEPARATOR_HEIGHT=10
MIN_AREA_HIEGHT=40
MIN_AREA_WIDTH=150
MIN_HEADER_HEIGHT=40
DEFAULT_MIN_WORDS_VERTICAL = 3


ALL_ATTRS = {"adv", "height", "linewidth", "pts", "size", "srcsize", "width", "x0", "x1", "y0", "y1","bits", "upright", "font", "fontname", "name", "text", "imagemask", "colorspace",
                             "evenodd", "fill", "non_stroking_color", "path", "stream", "stroke", "stroking_color"}


DEFAULT_WORD_EXTRACTION_SETTINGS = dict(
    x_tolerance=DEFAULT_X_TOLERANCE,
    y_tolerance=DEFAULT_Y_TOLERANCE,
    keep_blank_chars=False,
    use_text_flow=False,
    horizontal_ltr=True,  # Should words be read left-to-right?
    vertical_ttb=True,  # Should vertical words be read top-to-bottom?
    extra_attrs=[],
)

DEFAULT_TOKEN_EXTRACTION_SETTINGS = dict(
    x_tolerance=DEFAULT_X_TOLERANCE,
    y_tolerance=DEFAULT_Y_TOLERANCE,
    keep_blank_chars=False,
    use_text_flow=False,
    fixed_width=False,
    horizontal_ltr=True,  # Should words be read left-to-right?
    vertical_ttb=True,  # Should vertical words be read top-to-bottom?
    extra_attrs=[],
)

