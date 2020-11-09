from spacy import load

from mowgli_etl.pipeline.wdc.wdc_product_type import WdcProductType
from mowgli_etl.pipeline.wdc.wdc_product_type_classifier import WdcProductTypeClassifier
from mowgli_etl.pipeline.wdc.wdc_offers_corpus_entry import WdcOffersCorpusEntry

class WdcHeuristicProductTypeClassifier(WdcProductTypeClassifier):
    def __init__(self):
        self.NLP = load('en_core_web_sm')

    def __clean_words(self, line):
        words = line.split(' ')
        for i in range(len(words)):
            words[i] = words[i].split('_')
        pure_words = []
        for sequence in words:
            pure_words.extend(sequence)
        return ' '.join([word for word in pure_words if word.isalpha()])

    def classify(self, *, entry: WdcOffersCorpusEntry) -> WdcProductType:
        """
        Parse title/listing/other to pull ProductType with confidence value
        """
        for field in ["category", "description", "spec_table_content", "title"]:
            text = getattr(entry, field)
            if text is None:
                continue
            text = self.__clean_words(getattr(entry, field))
        
            doc = self.NLP(text)

            last_noun_name = None
            first_noun_sequence_name = None
            first_noun_flag = 0
            last_noun_sequence_name = None
            last_noun_flag = 1

            for token in doc:
                if token.pos in range(92, 101):
                    # Assume that general product name is last noun in title
                    last_noun_name = token.text

                    # Assume that general product name is the first sequence of just nouns
                    if first_noun_flag == 0:
                        if first_noun_sequence_name:
                            first_noun_sequence_name += " " + token.text
                        else:
                            first_noun_sequence_name = token.text

                    # Assume that general product name is the last sequence of just nouns
                    if last_noun_flag == 1:
                        last_noun_sequence_name = None
                        last_noun_flag = 0
                    if last_noun_sequence_name:
                        last_noun_sequence_name += " " + token.text
                    else:
                        last_noun_sequence_name = token.text

                else:
                    # Throw flag to terminate first noun sequence
                    if first_noun_sequence_name:
                        first_noun_flag = 1
                    last_noun_flag = 1

            if first_noun_sequence_name:
                first_noun_sequence_name.rstrip(" ")

            selections = []
            if last_noun_name:
                selections.append((last_noun_name, 1/3, "last_noun_heuristic"))
            if first_noun_sequence_name:
                selections.append((first_noun_sequence_name, 1/3, "first_noun_sequence_heuristic"))
            if last_noun_sequence_name:
                selections.append((last_noun_sequence_name, 1/3, "last_noun_sequence_heuristic"))

            yield WdcProductType(options=selections, source=text, key=field)


if __name__ == '__main__':
    from mowgli_etl.pipeline.wdc.wdc_constants import WDC_ARCHIVE_PATH
    from json import loads
    HPTC = WdcHeuristicProductTypeClassifier()
    with open(WDC_ARCHIVE_PATH / "offers_corpus_english_v2_random_100_clean.jsonl") as data:
        for line in data:
            for product_type in HPTC.classify(entry=WdcOffersCorpusEntry.from_json(line)):
                print(f"From {product_type.key}={product_type.source}:")
                print(f"\tFrom {len(product_type.possible)} options:")
                for product_option in product_type.possible:
                    print(f"\t\t{product_option.name}, {product_option.confidence*product_type.key_confidence:.3%} from {product_option.method}")
