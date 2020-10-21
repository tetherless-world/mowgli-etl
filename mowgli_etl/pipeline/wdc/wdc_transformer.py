import json
from pathlib import Path
from typing import Generator, Set, Dict, Union
from urllib.parse import quote
import re
import spacy
import os.path

# from mowgli_etl.model.concept_net_predicates import
from mowgli_etl.model.kg_edge import KgEdge

# from mowtli_etl.model.mowgli_predicates import
from mowgli_etl.model.kg_node import KgNode
from mowgli_etl._transformer import _Transformer
from mowgli_etl.model.word_net_id import WordNetId
from mowgli_etl.pipeline.wdc.wdc_constants import WDC_DATASOURCE_ID, WDC_HAS_DIMENSIONS, WDC_ARCHIVE_PATH
from mowgli_etl.pipeline.wdc.wdc_heuristic_product_type_classifier import (
    WdcHeuristicProductTypeClassifier as HPTC,
)


class WdcTransformer(_Transformer):
    __BAD_DUPLICATE = '{"brand":'

    def __clean(self, wdc_jsonl_file_path: Path):
        """
        Clean input file, particularly checking for multiple json items in one line, or split json object; return file with original name + "_clean"
        """
        wdc_jsonl_dir_path, wdc_jsonl_file_name = os.path.split(wdc_jsonl_file_path)
        wdc_jsonl_file_base_name, _ext = os.path.splitext(wdc_jsonl_file_name)
        new_file_name = wdc_jsonl_dir_path + '/' + wdc_jsonl_file_base_name + "_clean.jsonl"

        with open(wdc_jsonl_file_path, "r") as wdc_jsonl_file_file, open(
            new_file_name, "w"
        ) as new_file:
            for line in wdc_jsonl_file_file:
                # Catch duplicate objects
                if line.count(self.__BAD_DUPLICATE) > 1:
                    temp_line = ""
                    data_starts = []
                    val = 0
                    while val != -1:
                        val = line.find(self.__BAD_DUPLICATE, val + 1)
                        if line[val - 2] == ":" or val == -1:
                            continue
                        data_starts.append(val - 1)

                    for i in range(len(data_starts)):
                        if i < len(data_starts) - 1:
                            temp_line += line[data_starts[i] : data_starts[i + 1]]
                            if temp_line[-1] != "}":
                                temp_line += "}"
                            temp_line += "\n"
                        else:
                            t = list(line[data_starts[i] : :])
                            t[0] = "{"
                            temp_line += "".join(t)

                        line = temp_line
                new_file.write(line)

        return new_file_name

    def __find_dimensions(self, description, listing, additional_info):
        """
        Extract dimension data using regex
        """
        dimensions = []

        if description != None:
            dimensions = re.findall(
                "\d+(?: \d+)?\s?\w*\sx\s\d+\
                    (?: \d+)?\s?(?:x\s\d+\s?)?\w*",
                description,
            )

        if len(dimensions) == 0:
            if description:
                dimensions = re.findall(
                    "\d+\s?\w+\s\d+\s?\w+\
                        \slead\sx\s\d+\s?\w+",
                    description,
                )

        if len(dimensions) == 0:
            dimensions = re.findall(
                "\d+\s?\w*\sx\s\d+\
                    \s?\w*",
                listing,
            )

        if len(dimensions) == 0:
            dimensions = re.findall(
                "\d+\s?\w+\s\d+\s?\w+\
                    \slead\sx\s\d+\s?\w+",
                listing,
            )

        if len(dimensions) == 0:
            if additional_info != None:
                dimensions = re.findall(
                    "\d+(?: \d+)?\s?\w*\sx\s\d+\
                        (?: \d+)?\s?(?:x\s\d+\s?)?\w*",
                    additional_info,
                )

            if dimensions:
                return dimensions

        # dimensions = re.findall("\d+\s?\w+\s\d+\s?\w+\
        #         \slead\sx\s\d+\s?\w+", additional_info)

        return dimensions

    def transform(
        self, *, wdc_jsonl_file_path: Path
    ) -> Generator[Union[KgNode, KgEdge], None, None]:
        # Prepare file and nlp
        wdc_clean_file_path = self.__clean(wdc_jsonl_file_path)
        nlp = spacy.load("en_core_web_sm")

        # Parse file
        with open(wdc_clean_file_path, mode="r") as data:
            for row in data:
                # print(row)
                information = json.loads(row)
                listing = information["title"]
                description = information["description"]
                additional_info = information["specTableContent"]
                category = information["category"]

                # Ignore product if there is no listing name
                if listing == None:
                    listing = description
                    if listing == None:
                        listing = category

                product = HPTC().classify(title=listing)

                # doc = nlp(listing)

                # last_noun_name = ""
                # first_noun_sequence_name = ""
                # first_noun_flag = 0
                # last_noun_sequence_name = ""
                # last_noun_flag = 1

                # for token in doc:
                #     if token.pos in range(92, 101):
                #         # Assume that general product name is last noun in title
                #         last_noun_name = token.text

                #         # Assume that general product name is the first sequence of just nouns
                #         if first_noun_flag == 0:
                #             if first_noun_sequence_name != "":
                #                 first_noun_sequence_name += " "
                #             first_noun_sequence_name += token.text

                #         # Assume that general product name is the last sequence of just nouns
                #         if last_noun_flag == 1:
                #             last_noun_sequence_name = ""
                #             last_noun_flag = 0
                #         if last_noun_sequence_name != "":
                #             last_noun_sequence_name += " "
                #         last_noun_sequence_name += token.text

                #     else:
                #         # Throw flag to terminate first noun sequence
                #         if first_noun_sequence_name != "":
                #             first_noun_flag = 1
                #         last_noun_flag = 1

                # first_noun_sequence_name.rstrip(" ")

                dimensions = self.__find_dimensions(
                    description, listing, additional_info
                )

                specs = ""
                if dimensions:
                    for d in dimensions:
                        specs += f" {d}"
                    specs.rstrip(" ")
                else:
                    specs = "NA"

                # general_name = f"{last_noun_name} or\
                #         {first_noun_sequence_name} or\
                #         {last_noun_sequence_name}"

                yield KgEdge.with_generated_id(
                    subject=product.name,
                    predicate=WDC_HAS_DIMENSIONS,
                    object=specs,
                    sources=(WDC_DATASOURCE_ID,),
                )
                # yield KgNode(id = f"{WDC_DATASOURCE_ID}:\"general_name\"",
                #     sources = (WDC_DATASOURCE_ID,),
                #     labels = dimensions if dimensions != None else ["NA"])
