from urllib.request import urlopen, urlretrieve
from io import BytesIO
from zipfile import ZipFile
try:
    import mowgli_etl
except ImportError:
    import os.path
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from mowgli_etl.pipeline.web_child.web_child_transformer import WebChildTransformer
from mowgli_etl.model.edge import Edge
from mowgli_etl.model.node import Node
from mowgli_etl.model.mowgli_predicates import WN_SYNSET
from random import sample
import csv
from mowgli_etl.pipeline_wrapper import PipelineWrapper
from mowgli_etl.pipeline.web_child.web_child_pipeline import WebChildPipeline
from mowgli_etl.pipeline_storage import PipelineStorage
from mowgli_etl.pipeline.web_child.web_child_extractor import WebChildExtractor
from mowgli_etl.paths import DATA_DIR, PROJECT_ROOT
from os import listdir


def loadcsv():

    extractor = WebChildExtractor()

    print("Extracting Zip")
    webchildstorage = PipelineStorage(pipeline_id='web_child',root_data_dir_path=DATA_DIR)
    extraction = extractor.extract(force=False,storage=webchildstorage)

    transformer = WebChildTransformer()

    print('Transforming')
    triplegen = transformer.transform(**extraction)

    part_whole_edges = {}
    nodes = dict()

    predicates = set()

    print('Mapping edges and nodes')
    for node_or_edge in triplegen:

        if isinstance(node_or_edge, Node):
            node = node_or_edge
            nodes[node.id] = node
        elif isinstance(node_or_edge, Edge):
            edge = node_or_edge
            if edge.predicate == WN_SYNSET:
                continue
            else:
                if part_whole_edges.get(edge.predicate) == None:
                    part_whole_edges[edge.predicate] = [edge]
                else:
                    part_whole_edges[edge.predicate].append(edge)
        else:
            raise TypeError

    selected_edges =list()
    for prededges in part_whole_edges.values():
        selected_edges.extend(sample(prededges, k= 67))

    print('Parsing definitions')
    definitions = dict()
    glossfile = [f for f in listdir( webchildstorage.extracted_data_dir_path ) if f.endswith('.gloss')]
    with open(webchildstorage.extracted_data_dir_path / glossfile[0]) as csv_file:
            csv_reader = csv.DictReader(
                csv_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in csv_reader:
                word_nid = "WebChild:" + row["WordNet-synsetid"]
                defin = row["Definition (WordNet gloss)"]
                definitions[word_nid] = defin

    print('Writing to csv')

    with open( webchildstorage.loaded_data_dir_path / 'sampling.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject ID", "Subject word", "Subject definition","Object ID",
         "Object Word", "Object Defnition","Predicate","Annotation"])

        for el in selected_edges:
            result = ["" for i in range(7)]
            result[0]= el.subject
            result[1]= nodes[el.subject].label
            result[2]= definitions.get(el.subject,'None')
            result[3]= el.object
            result[4]= nodes[el.object].label
            result[5]= definitions.get(el.object,'None')
            result[6] = el.predicate
            writer.writerow(result)

    return

if __name__ == "__main__":
    loadcsv()
