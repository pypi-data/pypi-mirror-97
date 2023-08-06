from pdf2txt.settings import DEFAULT_X_SEPARATOR_WIDTH, DEFAULT_Y_SEPARATOR_HEIGHT, MIN_AREA_HIEGHT, MIN_AREA_WIDTH
from pdf2txt.core.tree import Node
from scipy import ndimage
from pdf2txt.utils import BoundingBox, is_ovarlaping_with_objects
from pdf2txt import utils
from pdf2txt.settings import DEFAULT_MIN_WORDS_VERTICAL
from copy import copy
import numpy as np


class AlignementRegionExtractor:
    h_separator_width = DEFAULT_X_SEPARATOR_WIDTH
    v_separator_height = DEFAULT_Y_SEPARATOR_HEIGHT

    def __init__(self, min_area_height=MIN_AREA_HIEGHT, min_area_width=MIN_AREA_WIDTH):

        self.min_area_height = min_area_height
        self.min_area_width = min_area_width
        self.objects=None

    def sanitize_objects(self, page):
        """
        Removes some objects that hinder the region detection: large rectangles, large vertical lines top large horizental line and bottom large horisental line
        """

        # these are graphical lines that span the page from side to side. However, they
        self.horizontal_separators = sorted(
            [line for line in page.lines if (line.right - line.left) >= 0.98 * (page.content_width)],
            key=lambda l: l.top)
        # we also filter out large vertical lines as we will noy use them a region separators
        lines = sorted([line for line in page.lines if (
                    (line.right - line.left) < 0.98 * (page.content_width) and line.height < 0.65 * (
                        page.bottom_margin - page.top_margin))], key=lambda l: l.top)
        # we fitler out large rectangles surrouning the content. They get in the way a a generic algorithm

        rects = sorted([rect for rect in page.rects if (
                (rect.width < 0.98 * (page.content_width)) and (
                rect.height < 0.65 * (page.bottom_margin - page.top_margin)))],
                       key=lambda l: (l.left, l.top))

        clustered = utils.cluster_objects(rects, "left", 2)
        if clustered:
            for cluster in clustered:
                joined = [cluster[0]]
                for r in cluster:
                    if r.top <= joined[-1].bottom:
                        joined.append(r)

                if joined[-1].bottom - joined[0].top > 0.65 * (page.bottom_margin - page.top_margin):
                    for r in cluster:
                        rects.remove(r)

        self.objects = lines + rects + page.graphs + page.tokens + page.tables

    def extract_regions(self, page):
        from pdf2txt.core.page import Region

        self.sanitize_objects(page)

        rects=self.extract_from_alignement(page)
        return [Region(page, r) for r in rects]

    def adjust_edge(self, edge, page):

        delta_step=5
        horizontal_bar_width=2 # a horizontal imaginary lines to check if there is an overlap with text across the width of the page
        edge.left-=delta_step
        edge.right-=delta_step
        delta_step=2
        indexes=utils.get_max_non_overlap_zone(edge, self.objects)
        if indexes:
            edge.top=indexes[0]+0.5
            edge.bottom=indexes[1]-0.5
        i=0
        while i <3 and utils.is_ovarlaping_with_objects(edge, self.objects):
            edge.left-=delta_step
            edge.right-=delta_step
            i+=1

        while not utils.is_ovarlaping_with_objects(edge, self.objects) and edge.left>=page.bbox.left:
            edge.left-=delta_step

        edge.left = (edge.left + edge.right) / 2
        edge.right = edge.left

        while not utils.is_ovarlaping_with_objects(edge, self.objects) and edge.top>=page.bbox.top:
            edge.top-=delta_step

        horizontal = BoundingBox(left=edge.left - MIN_AREA_WIDTH, top=edge.top, bottom=edge.top+horizontal_bar_width,
                                 right=edge.right + MIN_AREA_WIDTH)

        while is_ovarlaping_with_objects(horizontal, self.objects) and horizontal.bottom> horizontal.top:
            edge.top += delta_step
            horizontal.top=edge.top
            horizontal.bottom=edge.top+horizontal_bar_width


        if edge.top<page.bbox.top:
            edge.top=page.bbox.top
        else:
            edge.top+=delta_step

        while not utils.is_ovarlaping_with_objects(edge, self.objects) and edge.bottom <=page.bbox.bottom:
            edge.bottom+=delta_step

        horizontal=BoundingBox(left=edge.left-MIN_AREA_WIDTH, top=edge.bottom, bottom=edge.bottom+horizontal_bar_width, right=edge.right+MIN_AREA_WIDTH)

        while is_ovarlaping_with_objects(horizontal, self.objects) and horizontal.bottom> horizontal.top:
            edge.bottom-=delta_step
            horizontal.top=edge.bottom
            horizontal.bottom=edge.bottom+horizontal_bar_width

        if edge.bottom>page.bbox.bottom:
            edge.bottom=page.bbox.bottom
        else:
            edge.bottom-=delta_step

        if utils.is_ovarlaping_with_objects(edge, self.objects):
            edge.top=0
            edge.bottom=0
        return edge

    def _get_region_separators(self, page):

        top=page.top_margin

        if len(self.horizontal_separators)>0:
            edges = []
            for separator in sorted(self.horizontal_separators, key=lambda x: x.bottom):
                tokens=[token for token in page.tokens if token.top >top and token.bottom<=separator.bottom]
                if tokens:
                    edges.extend(self.words_to_left_edges(tokens))
                top=separator.bottom
            if top<page.bottom_margin:
                tokens=[token for token in page.tokens if token.top >top and token.bottom<=page.bottom_margin]
                edges.extend(self.words_to_left_edges(tokens))
        else:
            edges = self.words_to_left_edges(page.tokens)

        #transfrom into intial page coordinate and filter edges too close to the borders of the page
        edges=[edge for edge in edges if edge.left+page.bbox.left > (page.bbox.left+page.content_width) / 3.3 and edge.left+page.bbox.left < 2 * ((page.bbox.left+page.content_width) / 2.5)]

        edges=[self.adjust_edge(edge, page) for edge in edges]

        # sort edges by longest and remove the ones that are too close to the edges of the page
        edges=sorted([edge for edge in edges if (edge.bottom-edge.top)>=MIN_AREA_HIEGHT],  key=lambda x: -(x.bottom - x.top))

        if len(edges)==0:
            return []

#        edges=[edges[0]]+[y for x, y in zip(edges[:-1], edges[1:]) if (abs(y.left - x.left)> MIN_AREA_WIDTH or utils.vertical_overlap(x, y)==0)]
        no_overlap_edges=[edges[0]]
        for i in range(1, len(edges)):
            close_match=[edge for edge in no_overlap_edges if np.isclose(edges[i].left, edge.left, atol=MIN_AREA_WIDTH) and utils.vertical_overlap(edges[i], edge)>0]
            if not close_match:
                no_overlap_edges.append(edges[i])

        return no_overlap_edges

    def words_to_left_edges(self, words, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
        """
        Find (imaginary) vertical lines that connect the left, right, or
        center of at least `word_threshold` words.
        """
        # Find words that share the same left, right, or centerpoints

        by_left = utils.cluster_objects(words, "left", 0.5)

        if by_left is None:
            return []
        # Find the points that align with the most words
        by_left = list(filter(lambda x: len(x) >= word_threshold, by_left))


        edges = [
            BoundingBox(left=min(w.left for w in words), right=min(w.left for w in words), top=min(w.top for w in words),
                        bottom=max(w.bottom for w in words)) for words in by_left]

        return edges

    def _get_areas_from_separators(self, page, separators):
        table_areas = []
        # sort vertical lines by desending order of top edge (this allow to form the top area
        separators.sort(key=lambda te: te.top)
        left = page.bbox.left
        top = page.bbox.top
        right = page.bbox.right

        separator = separators[0]
        bottom = separator.top
        # top page area
        if bottom>top:
            area = utils.BoundingBox(left, top, right, bottom)
            table_areas.append(area)

        for separator in separators:

            # left area
            top = separator.top
            separator_to_the_left=self._get_left_separator(separators, separator)
            left=page.bbox.left

            if separator_to_the_left:
                left= page.bbox.left if separator.top< separator_to_the_left.top else separator_to_the_left.left
                bottom=separator_to_the_left.top if separator.top< separator_to_the_left.top else separator.bottom
                if separator.top== separator_to_the_left.top:
                    bottom=separator_to_the_left.bottom
            else:
                bottom=separator.bottom
            right = separator.left
            area = utils.BoundingBox(left, top, right, bottom)
            table_areas.append(area)
            #right area
            left=separator.left
            right = page.bbox.right
            separator_to_the_right=self._get_right_separator(separators, separator)

            if separator_to_the_right:
                if separator_to_the_right.top>=separator.top:
                    bottom=separator_to_the_right.top
                else:
                    bottom=separator_to_the_right.bottom if separator_to_the_right.bottom<separator.bottom else separator.bottom

#                bottom=separator_to_the_right.bottom if bottom<separator_to_the_right.bottom else separator_to_the_right.top
                    right = page.bbox.right if separator_to_the_right.top>separator.top else separator_to_the_right.right
            else:
                bottom = separator.bottom
            if bottom>top:
                area = utils.BoundingBox(left, top, right, bottom)
                table_areas.append(area)

            #bottom area
            top=separator.bottom
            separator_bellow=self._get_separator_bellow(separators, separator)
            left = page.bbox.left
            right= page.bbox.right
            if separator_to_the_right and separator_to_the_right.bottom> separator.bottom:
                bottom=separator_to_the_right.bottom
                right=separator_to_the_right.right
            elif separator_to_the_left and separator_to_the_left.bottom> separator.bottom:
                bottom=separator_to_the_left.bottom
                left=separator_to_the_left.left
            else:
                bottom=page.bbox.bottom
            if separator_bellow:
                bottom=separator_bellow.top


            if bottom>top:
                area = utils.BoundingBox(left, top, right, bottom)
                table_areas.append(area)

        return table_areas

    def extract_from_alignement(self, page):
        self.sanitize_objects(page)
        sepearators = self._get_region_separators(page)
        if sepearators:
            return self._get_areas_from_separators(page, sepearators)


        return []

    def _get_separator_bellow(self, separators, separator):
        # separators are sorted acording to  decreasing y0
        for s in separators:
            if s.top> separator.bottom:
                return s
        return None

    def _get_left_separator(self, separators, separator):
        # separators are sorted acording to  decreasing y0
        for s in separators:
            if s.left < separator.left and (separator.top <= s.top <= separator.bottom  or s.top <= separator.top <= s.bottom):
                return s
        return None

    def _get_right_separator(self, separators, separator):
        # separators are sorted acording to  decreasing y0
        for s in separators:
            if s.left > separator.left and (separator.top <= s.top < separator.bottom or s.top <= separator.top <= s.bottom):
                return s
        return None
