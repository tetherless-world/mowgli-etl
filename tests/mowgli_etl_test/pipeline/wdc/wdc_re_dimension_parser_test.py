from json import loads
from pathlib import Path

from mowgli_etl.pipeline.wdc.wdc_re_dimension_parser import (
    WdcREDimensionParser as WdcReDP,
)

# Should have path argument. For now using clean file in directory
def test_re_dimension_parser(wdc_json_clean_file_path: Path):
    with open(wdc_json_clean_file_path, "r") as data:
        item_counter = 0
        for row in data:
            item_counter += 1
            information = loads(row)

            dimensions = WdcReDP().parse(information=information)

            """
            Uncomment once RE code is implemented
            """
            # if item_counter == 23:
            #     assert dimensions.depth == 19.3
            #     assert dimensions.height == 17.5
            #     assert dimensions.lenght == None
            #     assert dimensions.width == 19.3
            #     assert dimensions.unit == "cm"

            # elif item_counter == 85:
            #     assert dimensions.depth == None
            #     assert dimensions.height == None
            #     assert dimensions.length == 30
            #     assert dimensions.width == 3.2
            #     assert dimensions.unit == "cm"

            # elif item_counter == 91:
            #     assert dimensions.depth == None
            #     assert dimensions.height == 9.8
            #     assert dimensions.length == None
            #     assert dimensions.width == 10.3
            #     assert dimensions.unit == "cm"
            """
            Comment out once RE code is implemented
            """
            assert dimensions.depth == None
            assert dimensions.width == None
            assert dimensions.length == None
            assert dimensions.height == None
