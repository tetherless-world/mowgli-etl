import re
import json
import sys

from mowgli_etl.pipeline.wdc.wdc_product_dimensions import WdcProductDimensions
from mowgli_etl.pipeline.wdc.wdc_dimension_parser import WdcDimensionParser
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH


class WdcREDimensionParser(WdcDimensionParser):
    def __init__(self):
        self.__RE_DIMENSION_DECIMAL_STR = r"\d+\s\d+[hwl]"
        self.__RE_DIMENSION_STR = r"\d+[hwl]"
        self.__RE_DIMENSION_UNIT_STR = r"(?<=\d\w\s)\w\w"
        self.__UNITS = ["ml", "cm", "mm", "in", "ft", "m"]

    """
    Parse dimensions from the title
    """

    def _parseTitle(self, *, title: str):
        if not title:
            return None

        dimensions = re.findall(self.__RE_DIMENSION_DECIMAL_STR, title)
        dimensions += re.findall(self.__RE_DIMENSION_STR, title)
        unit = re.findall(self.__RE_DIMENSION_UNIT_STR, title)
        unit = [val for val in unit if val in self.__UNITS]

        return [list(set(dimensions)), unit]

    """
    Parse dimensions from the description
    """

    def _parseDescription(self, *, description: str):
        if not description:
            return None

        dimensions = re.findall(self.__RE_DIMENSION_DECIMAL_STR, description)
        dimensions += re.findall(self.__RE_DIMENSION_STR, description)
        unit = re.findall(self.__RE_DIMENSION_UNIT_STR, description)
        unit = [val for val in unit if val in self.__UNITS]

        return [list(set(dimensions)), unit]

    """
    Parse dimensions from the specTableContent
    """

    def _parseSpecTableContent(self, *, specTableContent: str):
        if not specTableContent:
            return None

        dimensions = re.findall(self.__RE_DIMENSION_DECIMAL_STR, specTableContent)
        dimensions += re.findall(self.__RE_DIMENSION_STR, specTableContent)
        unit = re.findall(self.__RE_DIMENSION_UNIT_STR, specTableContent)
        unit = [val for val in unit if val in self.__UNITS]

        return [list(set(dimensions)), unit]

    def _formatKVP(self, *, build: str, trigger: str):
        build = build.split(" ")
        build[-2] += trigger
        return build

    """
    Parse dimensions from the keyValuePairs
    """

    def _parseKeyValuePairs(self, *, keyValuePairs: dict):
        if not keyValuePairs:
            return None

        dimensions = []
        unit = []
        if "width" in keyValuePairs.keys():
            build = self._formatKVP(build=keyValuePairs["width"], trigger="w")
            unit.append(build.pop(-1))
            dimensions.append(" ".join(build))
        if "depth" in keyValuePairs.keys():
            build = self._formatKVP(build=keyValuePairs["depth"], trigger="d")
            unit.append(build.pop(-1))
            dimensions.append(" ".join(build))
        if "length" in keyValuePairs.keys():
            build = self._formatKVP(build=keyValuePairs["length"], trigger="l")
            unit.append(build.pop(-1))
            dimensions.append(" ".join(build))
        if "height" in keyValuePairs.keys():
            build = self._formatKVP(build=keyValuePairs["height"], trigger="h")
            unit.append(build.pop(-1))
            dimensions.append(" ".join(build))

        return [list(set(dimensions)), unit]

    def parse(self, *, information: dict) -> WdcProductDimensions:
        """
        We want to find any case where there is a numberxnumberxnumber... combination
        Or number+d, number+w, number+h, number+l
        Known dimensions:
            in description: " 340x400x706mm "
            in description: " 700ml bis 899ml "
            in description: " 125g "
            in description: " 24 x 30 in "
            in description: " length 48 quot li li height 17 3 8 quot li li seat width 14 quot li li total height 32 1 4 quot li li total depth 26 1 8 quot li li weight 66 lbs "
            in keyValuePairs: "{"height":"17 5cm 6 89 in","width":"19 3cm 7 6 in","depth":"19 3cm 7 6 in""
            in specTableContent: "height 17 5cm 6 89 in width 19 3cm 7 6 in depth 19 3cm 7 6 in "
            in description: " 8 1 2 x 11 "
            in description: " 5 3 4 x 8 3 4 "
            in title: "3 x21 "
            in specTableContent: " xxs 78cm 60 5cm 85 5cm xs 80 5cm 63 5cm 88 5cm s 83cm 66cm 91cm m 88cm 71cm 96cm l 93cm 76cm 101cm xl 98cm 81cm 106cm xxl 103cm 86cm 111cm xxxl 109cm 92cm 117cm xxxxl 116cm 99cm 124cm "
            in title: " 6 x 1 0 12 mm "
            in keyValuePairs: ""capacity weight":"1 42 lbs""
            in keyValuePairs: ""item weight":"1 540 lbs""
            in title: " 94 x 2400mm "
            in specTableContent: " xxs 78cm 60 5cm 85 5cm xs 80 5cm 63 5cm 88 5cm s 83cm 66cm 91cm m 88cm 71cm 96cm l 93cm 76cm 101cm xl 98cm 81cm 106cm xxl 103cm 86cm 111cm xxxl 109cm 92cm 117cm xxxxl 116cm 99cm 124cm "
            in title: " 50ml "
            in title: " 15ft "
            in description: " 120 inch opening x 54 inch high gates "
            in keyValuePairs: ""size":"width 3 2cm 1 3 length 30cm 11 8","weight":"200g""
            in specTableContent: " width 3 2cm 1 3 length 30cm 11 8 weight 200g "
            in specTableContent: " 6 mm x 12 in "
            in description: " 9 8h x 10 3w cm "
            in description: " 350ml or 400ml "
            in specTableContent: " 7 x10"
            in specTableContent: " xs 2 34 s 4 6 35 36 m 8 10 37 38 l 12 14 39 5 41 xl 16 18 42 5 44 5 2xl 20 46 3xl 22 47 5 4xl 24 49"
        """
        """
        OLD CODE:
        
        dimensions = []

        if description != None:
            dimensions = re.findall("\d+(?: \d+)?\s?\w*\sx\s\d+\
                    (?: \d+)?\s?(?:x\s\d+\s?)?\w*", description)

        if len(dimensions) == 0:
            if(description):
                dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\
                        \slead\sx\s\d+\s?\w+", description)

        if len(dimensions) == 0:
            dimensions = re.findall("\d+\s?\w*\sx\s\d+\
                    \s?\w*", listing)

        if len(dimensions) == 0:
            dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\
                    \slead\sx\s\d+\s?\w+", listing)

        if len(dimensions) == 0:
            if additional_info != None:
                dimensions = re.findall("\d+(?: \d+)?\s?\w*\sx\s\d+\
                        (?: \d+)?\s?(?:x\s\d+\s?)?\w*", additional_info)

            # if dimensions:
            #     return dimensions

        # dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\
        #         \slead\sx\s\d+\s?\w+", additional_info)

        return dimensions
        """
        titleDimensions = self._parseTitle(title=information["title"])
        if titleDimensions and len(titleDimensions[0]) > 1:
            print("from title:", titleDimensions, sep="\n\t")
        descriptionDimensions = self._parseDescription(
            description=information["description"]
        )
        if descriptionDimensions and len(descriptionDimensions[0]) > 1:
            print("from description:", descriptionDimensions, sep="\n\t")
        specTableContentDimensions = self._parseSpecTableContent(
            specTableContent=information["specTableContent"]
        )
        if specTableContentDimensions and len(specTableContentDimensions[0]) > 1:
            print("from specTable:", specTableContentDimensions, sep="\n\t")
        keyValuePairsDimensions = self._parseKeyValuePairs(
            keyValuePairs=information["keyValuePairs"]
        )
        if keyValuePairsDimensions and len(keyValuePairsDimensions[0]) > 1:
            print("from keyValuePairs:", keyValuePairsDimensions, sep="\n\t")
        """
        RE code goes here
        """

        return WdcProductDimensions(
            depth=None,
            height=None,
            length=None,
            width=None,
            volume=None,
            mass=None,
            depth_unit=None,
            height_unit=None,
            length_unit=None,
            width_unit=None,
            volume_unit=None,
            mass_unit=None,
        )


# with open(
#     WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r"
# ) as data:
#     count = 0
#     for row in data:
#         count += 1
#         print(count)
#         info = json.loads(row)
#         WdcREDimensionParser().parse(information=info)
