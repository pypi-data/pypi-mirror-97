from copy import copy
from pdf2txt.core.space_region import SpaceRegionExtractor
from pdf2txt.core.alignement_region import AlignementRegionExtractor
from pdf2txt import utils
from pdf2txt.settings import DEFAULT_X_SEPARATOR_WIDTH, DEFAULT_Y_SEPARATOR_HEIGHT, MIN_AREA_HIEGHT, MIN_AREA_WIDTH


class RegionExtractor:

    def __init__(self):

        self.space_region=SpaceRegionExtractor()
        self.alignement_region=AlignementRegionExtractor()


    def extract_regions(self, page, method='images'):

        from pdf2txt.core.page import Region


        if method=='objects':
            regions = self.space_region.extract_regions_from_objects(page)


            page_surface = utils.calculate_area(page.bbox)

            regions2 = copy(regions)
            for region in regions:
                area_surface_ratio = round(utils.calculate_area(region) / page_surface, 2)
                if area_surface_ratio > 0.2:
                    a_regions = self.alignement_region.extract_regions(region)
                    if len(a_regions) > 1:
                        regions2.remove(region)
                        regions2.extend(a_regions)


            return regions2

        elif method=='images':
            regions= self.space_region.extract_regions_from_image(page)

            regions=sorted(regions, key=lambda x: x.top)

            for i in range(0, len(regions)-1):
                if regions[0].top==0 and regions[1].top==0 and regions[0].bottom==regions[1].bottom and regions[i].bottom<page.page_image.shape[0]/4:
                    regions[1].left=regions[0].left
                    del regions[0]
                else:
                    break
            return [Region(page, r) for r in regions]