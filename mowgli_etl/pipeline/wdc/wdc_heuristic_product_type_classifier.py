from spacy import load

from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier


class WdcHeuristicProductTypeClassifier(WdcProductTypeClassifier):
    def classify(self, *, title: str) -> WdcProductType:
        '''
        Parse title/listing/other to pull ProductType with confidence value
        '''
        nlp = load("en_core_web_sm")
        
        doc = nlp(title)

        last_noun_name = ""
        first_noun_sequence_name = ""
        first_noun_flag = 0
        last_noun_sequence_name = ""
        last_noun_flag = 1

        for token in doc:
            if token.pos in range(92, 101):
                # Assume that general product name is last noun in title
                last_noun_name = token.text

                # Assume that general product name is the first sequence of just nouns
                if first_noun_flag == 0:
                    if first_noun_sequence_name != "":
                        first_noun_sequence_name += " "
                    first_noun_sequence_name += token.text

                # Assume that general product name is the last sequence of just nouns
                if last_noun_flag == 1:
                    last_noun_sequence_name = ""
                    last_noun_flag = 0
                if last_noun_sequence_name != "":
                    last_noun_sequence_name += " "
                last_noun_sequence_name += token.text

            else:
                # Throw flag to terminate first noun sequence
                if first_noun_sequence_name != "":
                    first_noun_flag = 1
                last_noun_flag = 1

        first_noun_sequence_name.rstrip(" ")
        return \
            WdcProductType(
                name=last_noun_name,
                confidence=1/3,
                alternate=[first_noun_sequence_name, last_noun_sequence_name]
            )
