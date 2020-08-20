import json
from pathlib import Path
from typing import Generator, Set, Dict, Union
from urllib.parse import quote
import spacy

# from mowgli_etl.model.concept_net_predicates import
from mowgli_etl.model.kg_edge import KgEdge
# from mowtli_etl.model.mowgli_predicates import
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.word_net_id import WordNetId
from mowgli_etl.pipeline.wdc.constants import WDC_DATASOURCE_ID, WDC_HAS_DIMENSIONS

class WDCTransformer(_Transformer):
    __BAD_DUPLICATE = "\"brand\":"

    def __clean(self, wdc_jsonl_file_path: Path):
        new_file_name = wdc_jsonl_file_path[0:-6] + "_clean.jsonl"

        with open(wdc_jsonl_file_path, "r") as wdc_jsonl_file_file, open(new_file_name, "w") as new_file:
            for line in wdc_jsonl_file_file:
                if line.count(__BAD_DUPLICATE) > 1:
                    data_starts = []
                    val = 0
                    while val != -1:
                        val = line.find(__BAD_DUPLICATE, val + 1)
                        if line[val - 2] == ':' or val == -1:
                            continue
                        data_starts.append(val - 1)

                    for i in range(len(data_starts)):
                        if i < len(data_starts - 1):
                            new_file.write(line[data_starts[i]:data_starts[i+1]] + '\n')
                        else:
                            new_file.write(line[data_starts[i]::])
        
        return new_file_name

    def __find_dimensions(desctiption, listing, additional_info):
        dimensions = []

        if description != None:
            dimensions = re.findall("\d+(?: \d+)?\s?\w*\sx\s\d+\
                    (?: \d+)?\s?(?:x\s\d+\s?)?\w*", description)

        if len(dimensions) == 0:
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

            if len(dimensions) == 0:
                dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\
                        \slead\sx\s\d+\s?\w+", additional_info)

        return dimensions

    def transform(self, *, wdc_jsonl_file_path: Path)  -> Generator[Union[KgNode, KgEdge], None, None]:
        # Prepare file and nlp
        wdc_clean_file_path = self.clean(wdc_jsonl_file_path)
        nlp = spacy.load("en_core_web_sm")
        
        # Parse file
        with open(wdc_clean_file_path, mode="r") as data:
            for row in data:
                information = json.loads(row)
                listing = information["title"]
                description = information["description"]
                additional_info = line["specTableContent"]
                category = line["category"]

                # Ignore product if there is no listing name
                if listing == None:
                    continue

                doc = nlp(listing)

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

                dimensions = self.__find_dimensions(
                        description,
                        listing, 
                        additional_info)

                specs = ""
                if dimensions:
                    for d in dimensions:
                        specs += f" {d}"
                    specs.rstrip(" ")
                else:
                    specs = "NA"

                general_name = f"{last_noun_name} or\
                        {first_noun_sequence_name} or\
                        {last_noun_sequence_name}"

                yield KgEdge.with_generated_id(subject = general_name, predicate = WDC_HAS_DIMENSIONS, object = specs)
                # yield KgNode(id = f"{WDC_DATASOURCE_ID}:\"general_name\"",
                #     sources = (WDC_DATASOURCE_ID,),
                #     labels = dimensions if dimensions != None else ["NA"])
