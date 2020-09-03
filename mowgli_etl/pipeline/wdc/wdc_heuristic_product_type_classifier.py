from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier


class WdcHeuristicProductTypeClassifier(WdcProductTypeClassifier):
    def classify(self, *, title: str) -> WdcProductType:
        '''
        Parse title/listing/other to pull ProductType with confidence value
        '''
        return \
            WdcProductType(
                name=title.split()[-1]
            )
