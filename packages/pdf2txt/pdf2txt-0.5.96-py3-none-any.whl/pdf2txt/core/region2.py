from pdf2txt.settings import DEFAULT_X_SEPARATOR_WIDTH, DEFAULT_Y_SEPARATOR_HEIGHT, MIN_AREA_HIEGHT, MIN_AREA_WIDTH
from pdf2txt.core.tree import Node
from scipy import ndimage
from pdf2txt.utils import BoundingBox, is_ovarlaping_with_objects
from pdf2txt import utils
from pdf2txt.settings import DEFAULT_MIN_WORDS_VERTICAL
from copy import copy
import numpy as np


class RegionExtractor:
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

        #these are graphical lines that span the page from side to side. However, they
        self.horizontal_separators = sorted([line for line in page.lines if (line.right - line.left) >= 0.98 * (page.content_width)], key=lambda l: l.top)
        #we also filter out large vertical lines as we will noy use them a region separators
        lines = sorted([line for line in page.lines if ((line.right - line.left) < 0.98 * (page.content_width) and line.height < 0.65 * (page.bottom_margin-page.top_margin))], key=lambda l: l.top)
        #we fitler out large rectangles surrouning the content. They get in the way a a generic algorithm


        rects = sorted([rect for rect in page.rects if (
                            (rect.width < 0.98 * (page.content_width)) and (
                                rect.height < 0.65 * (page.bottom_margin - page.top_margin)))],
                key=lambda l: (l.left, l.top))

        clustered=utils.cluster_objects(rects, "left", 2)
        if clustered:
            for cluster in clustered:
                joined=[cluster[0]]
                for r in cluster:
                    if r.top<=joined[-1].bottom:
                        joined.append(r)

                if joined[-1].bottom-joined[0].top> 0.65 * (page.bottom_margin - page.top_margin):
                    for r in cluster:
                        rects.remove(r)


        self.objects=lines+rects+page.graphs+page.tokens+page.tables

    def extract_regions(self, page):
        from pdf2txt.core.page import Region

        self.parent_right=page.right
        self.parent_bottom=page.bottom

        statistics=page.font_statistics
        h=max(statistics['interline'], 2)
        self.sanitize_objects(page)
        regions = self.regions_from_spaces(page, stride=2, horizental_separator_width=h,
                                                     vertical_separator_width=2)


        page_surface = utils.calculate_area(page.bbox)

        regions2 = copy(regions)
        for region in regions:
            area_surface_ratio = round(utils.calculate_area(region) / page_surface, 2)
            if area_surface_ratio > 0.2:
                rects = self.extract_from_alignement(region)
                if len(rects) > 1:
                    regions2.remove(region)
                    regions2.extend([Region(region, r) for r in rects])


        return regions2

    def regions_from_spaces(self, page, stride=4, vertical_separator_width=None, horizental_separator_width=None, split_direction='all'):

        if vertical_separator_width:
            self.v_separator_height = vertical_separator_width
        if horizental_separator_width:
            self.h_separator_width = horizental_separator_width

        area_tree = self.split_tree_of_rectangles(page=page, stride=stride, split_direction=split_direction,)

        return area_tree.get_leaf_nodes()

    def split_tree_of_rectangles(self, page, stride=None, split_direction='all', step=0):
        #possible values for split_direction: 'all',  'horizental', 'vertical'
        self.sanitize_objects(page)
        tree = Node(page)

        split_vertical=False
        split_horizental=False

        if split_direction=='all':
            split_vertical = True
            split_horizental = True
        elif split_direction in ['vertical', 'v']:
            split_vertical = True
        elif split_direction in ['horizental', 'h']:
            split_horizental=True
        else:
            raise Exception("split_direction have to be either 'all', 'vertical' , 'v  'horizental' or 'h'")
        split = (None, None)
        if split_vertical:
            split = self._split_region_vertical(page, stride)

        if split == (None, None):
            if split_horizental:
                min_area_height = self.min_area_height
                if step > 1:
                    min_area_height = 2 * self.min_area_height
                split = self._split_region_horizental(area=page, stride=stride, min_height=min_area_height)

        if split != (None, None):
            if split[0]:
                tree.left = self.split_tree_of_rectangles(split[0], stride,  split_direction, step+1)
            if split[1]:
                tree.right = self.split_tree_of_rectangles(split[1], stride, split_direction, step+1)
        return tree

    def _split_region_horizental2(self, area, stride, min_height):
        from pdf2txt.core.page import Region

        nb_overlaps = []
        r1 = None
        r2 = None
        for top in range(int(area.top), int(area.bottom), stride):
            bottom = top + self.h_separator_width
            separator = BoundingBox(left=area.left, right=area.right, top=top, bottom=bottom)
            nb_overlaps.append((bottom, int(not is_ovarlaping_with_objects(separator, self.objects))))

        oo = [val[1] for val in nb_overlaps]
        if len(set(oo)) > 1:

            while oo[-1] == 1:
                oo = oo[:-1]
                nb_overlaps = nb_overlaps[:-1]
            i = 0
            while oo[i] == 1:
                oo[i] = 0
                nb_overlaps[i] = (nb_overlaps[i][0], 0)
                i += 1
            if sum(oo) > 1:

                split_indeces = self.get_gaps_by_largest(nb_overlaps)
                if len(split_indeces) > 0:
                    split_y = split_indeces[0]
                    i = 1
                    while (abs(split_y - area.top) < min_height or (abs(split_y - area.bottom)< min_height)) and i < len(split_indeces):
                        split_y = split_indeces[i]
                        i += 1
                    if (abs(split_y - area.top) >= min_height and abs(
                            area.bottom - split_y) >= min_height):
                        r1 = Region(area, BoundingBox(top=area.top, left=area.left, right=area.right, bottom=split_y))
                        r2 = Region(area, BoundingBox(top=split_y, left=area.left, right=area.right, bottom=area.bottom))

        return r1, r2

    def _split_region_horizental(self, area, stride, min_height):
        from pdf2txt.core.page import Region
        nb_overlaps = []
        r1 = None
        r2 = None
        stride=1

        for top in range(int(area.top), int(area.bottom), stride):
            bottom = top# + self.h_separator_width
            separator = BoundingBox(left=area.left, right=area.right, top=top, bottom=bottom)
            nb_overlaps.append(is_ovarlaping_with_objects(separator, self.objects))

        overlap_counts = np.array([int(val) for val in nb_overlaps])

        i=1
        while overlap_counts[-i] == 0:
            overlap_counts[-i] = 1
            i+=1
        i=0
        while overlap_counts[i] == 0:
            overlap_counts[i] = 1
            i+=1

        split_indices, labels, s = self.get_gaps_by_largest2(overlap_counts)
        if len(split_indices) > 0:
            indices = np.where(labels == split_indices[0] + 1)
            if len(indices[0]) > self.h_separator_width:
                split_y = indices[0][int(len(indices[0]) / 2)]
                i = 1
                while (abs(split_y - area.top) < min_height or (abs(split_y - area.bottom)< min_height)) and i < len(split_indices) and len(
                        indices[0]) < self.h_separator_width:
                    indices = np.where(labels == split_indices[i] + 1)
                    split_y = indices[0][int(len(indices[0]) / 2)]
                    i += 1
                if abs(split_y - area.top) >= min_height and abs(area.bottom - split_y) >= min_height and len(
                        indices[0]) >= self.h_separator_width:
                    r1 = Region(area, BoundingBox(top=area.top, left=area.left, right=area.right, bottom=split_y))
                    r2 = Region(area, BoundingBox(top=split_y, left=area.left, right=area.right, bottom=area.bottom))
        return r1, r2

    def _split_region_vertical(self, area, stride):
        from pdf2txt.core.page import Region

        nb_overlaps = []
        r1 = None
        r2 = None

        for left in range(int(area.left), int(area.right), stride):
            right = left + self.v_separator_height
            separator = BoundingBox(left=left, right=right, top=area.top, bottom=area.bottom)
            nb_overlaps.append((right, not is_ovarlaping_with_objects(separator, self.objects)))

        oo = [int(val[1]) for val in nb_overlaps]
        if len(set(oo)) != 1:
            while oo[-1] == 1:
                oo = oo[:-1]
                nb_overlaps = nb_overlaps[:-1]
            i = 0
            while oo[i] == 1:
                oo[i] = 0
                nb_overlaps[i] = (nb_overlaps[i][0], 0)
                i += 1
            if sum(oo) > 1:
                split_indeces = self.get_gaps_by_largest(nb_overlaps)
                if len(split_indeces) > 0:
                    split_x = split_indeces[0]
                    i = 1
                    while (abs(split_x - area.left) < self.min_area_width or abs(split_x - area.right) < self.min_area_width) and i < len(split_indeces) - 1:
                        split_x = split_indeces[i]

                        i += 1
                    if abs(split_x - area.left) >= self.min_area_width and abs(
                            area.right - split_x) >= self.min_area_width:
                        r1 = Region(area, BoundingBox(top=area.top, left=area.left, right=split_x, bottom=area.bottom))
                        r2 = Region(area, BoundingBox(top=area.top, left=split_x, right=area.right, bottom=area.bottom))
        # if r1:
        #     plot_page([r1, r2], page.width, page.height)
        return r1, r2

    def get_gaps_by_largest(self, arr):
        indices = [(i, a) for i, (a, x) in enumerate(arr) if x == 1]
        sizes = []
        size = 0
        for i in range(0, len(indices) - 1):
            if indices[i + 1][0] - indices[i][0] == 1:
                size += 1
            elif size > 0:
                sizes.append((indices[i - int(size / 2)][1], size))
                size = 0
        if size > 0:
            sizes.append((indices[i - int(size / 2)][1], size))

        #    indices2=[]
        return [i for i, j in sorted(sizes, key=lambda x: (-x[1], x[0]))]

    def get_gaps_by_largest2(self, arr):
        labels, num_label = ndimage.label(arr == 0)
        sizes = np.bincount(labels.ravel())
        biggest_labels = (-sizes[1:]).argsort()
        return biggest_labels, labels, sizes

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
