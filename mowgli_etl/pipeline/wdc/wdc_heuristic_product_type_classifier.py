from spacy import load

from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier


class WdcHeuristicProductTypeClassifier(WdcProductTypeClassifier):
    def classify(*, title: str) -> WdcProductType:
        """
        Parse title/listing/other to pull ProductType with confidence value
        """
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

        selections = [WdcProductType.option(last_noun_name, 1/3, "last_noun_heuristic"),
                    WdcProductType.option(first_noun_sequence_name, 1/3, "first_noun_sequence_heuristic"),
                    WdcProductType.option(last_noun_sequence_name, 1/3, "last_noun_sequence_heuristic")]

        return WdcProductType(options=selections, source=title)


if __name__ == '__main__':
    from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
    from json import loads
    with open(WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl", "r") as data:
        for line in data:
            line = loads(line)
            for key in ["title", "description", "specTableContent", "category"]:
                if line[key]:
                    product_type = WdcHeuristicProductTypeClassifier.classify(title=line[key])
                    print(f"From {key}={product_type.source}:")
                    print(f"\tFrom {len(product_type.possible)} options:")
                    for product_option in product_type.possible:
                        print(f"\t\t{product_option.name}, {product_option.confidence:.3%} from {product_option.method}")
