from urllib.request import urlopen, urlretrieve
from io import BytesIO
from zipfile import ZipFile
from mowgli.lib.etl.web_child.web_child_transformer import WebChildTransformer
from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.cskg.mowgli_predicates import WN_SYNSET
from random import sample
import csv
from mowgli.lib.etl.pipeline_wrapper import PipelineWrapper
from mowgli.lib.etl.web_child.web_child_pipeline import WebChildPipeline
from mowgli.lib.etl.pipeline_storage import PipelineStorage



def loadcsv():

    print("Downloading Zip")
    url = urlopen('http://people.mpi-inf.mpg.de/~ntandon/resources/relations/partOf/webchild_partof.zip')
    urlstream = BytesIO(url.read())

    z = ZipFile(urlstream)
    print("Extracting Zip")
    z.extractall()
    
    print("Downloading Glossary")
    wordnet = urlretrieve('http://people.mpi-inf.mpg.de/~ntandon/resources/relations/metadata/noun.gloss','noun.gloss')

    transformer = WebChildTransformer()

    print('transforming')
    triplegen = transformer.transform(memberof_csv_file_path ="webchild_partof_memberof.txt",
        physical_csv_file_path="webchild_partof_physical.txt",
        substanceof_csv_file_path="webchild_partof_substanceof.txt",
        wordnet_csv_file_path="noun.gloss")


    nodemap = dict()
    edgemap = dict()
    part_whole_edges = list()
    nodes = dict()

    print('mapping edges and nodes')
    for node_or_edge in triplegen:    
        
        if isinstance(node_or_edge, Node):
            node = node_or_edge
            nodes[node.id] = node
        elif isinstance(node_or_edge, Edge):
            edge = node_or_edge
            if edge.predicate == WN_SYNSET:
                continue
            else:
                part_whole_edges.append(edge)
        else:
            raise TypeError

    selected_edges = sample(part_whole_edges, k= 200)

    print('parsing definitions')
    definitions = dict()
    with open('noun.gloss') as csv_file:
            csv_reader = csv.DictReader(
                csv_file, delimiter="\t", quoting=csv.QUOTE_NONE
            )
            for row in csv_reader:
                word_nid = "WebChild:" + row["WordNet-synsetid"]
                defin = row["Definition (WordNet gloss)"]
                definitions[word_nid] = defin

    print('writing to csv')

    with open('sampling.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject ID", "Subject word", "Subject definition","Object ID",
         "Object Word", "Object Defnition","Predicate","Annotation"])

        for el in selected_edges:
            result = ["" for i in range(7)]
            result[0]= el.subject
            result[1]= nodes[el.subject].label
            result[2]= definitions.get(el.subject) if definitions.get(el.subject) else 'None'
            result[3]= el.object
            result[4]= nodes[el.object].label
            result[5]= definitions.get(el.object) if definitions.get(el.object) else 'None'
            result[6] = el.predicate
            writer.writerow(result)

    return

if __name__ == "__main__":
    loadcsv()
