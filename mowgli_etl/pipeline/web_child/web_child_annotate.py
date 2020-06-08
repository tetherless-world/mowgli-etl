
import csv

try:
    import mowgli_etl
except ImportError:
    import os.path
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from mowgli_etl.pipeline.web_child.web_child_transformer import WebChildTransformer
from mowgli_etl.cskg.edge import Edge


def annotate():
    ogfiles = [open('etl/data/webchildsampling/loaded/DF_annotations.csv'), open('etl/data/webchildsampling/loaded/MG_annotations.csv')]
    newfiles = [open('etl/data/webchildsampling/loaded/DF_annotations_anlys.csv',mode='w'), 
     open('etl/data/webchildsampling/loaded/MG_annotations_anlys.csv', mode='w')]

    transformer = WebChildTransformer()
    print('Transforming')
    triplegen = transformer.transform(
        memberof_csv_file_path= 'etl/data/webchildsampling/extracted/webchild_partof_memberof.txt',
        physical_csv_file_path= 'etl/data/webchildsampling/extracted/webchild_partof_physical.txt',
        substanceof_csv_file_path= 'etl/data/webchildsampling/extracted/webchild_partof_substanceof.txt',
        wordnet_csv_file_path= 'etl/data/webchildsampling/extracted/httppeople.mpi-inf.mpg.de~ntandonresourcesrelationsmetadatanoun.gloss'
    )

    scores={}

    print("Mapping Edges to Scores")

    for edge in triplegen:
        if isinstance(edge, Edge):
            if scores.get(edge.subject) is None:
                scores[edge.subject] = {edge.object:edge.weight}
            else:
                scores[edge.subject][edge.object] = edge.weight

            #print(scores[edge.subject][edge.object])




    print("Parsing")
    for i in range(2):
        csv_reader = csv.DictReader(
            ogfiles[i], delimiter=","
        )

        writer = csv.writer(newfiles[i])
        writer.writerow(["Subject ID", "Subject word", "Subject definition","Object ID",
            "Object Word", "Object Defnition","Predicate","Annotation","Web Child Score","Diff"])

        for row in csv_reader:
            if row.get("Annotation") is None or row.get("Annotation") == "":
                continue

            result = ["" for i in range(10)]
            result[0]= row.get("Subject ID")
            #print(result[0])
            result[1]= row.get("Subject word")
            result[2]= row.get("Subject definition")
            result[3]= row.get("Object ID")
            #print(result[3])
            result[4]= row.get("Object Word")
            result[5]= row.get("Object Defnition")
            result[6] = row.get("Predicate")
            result[7] = row.get("Annotation")
            result[8] = str(round((scores[result[0]][result[3]] *5),1) )
            result[9] = str(round(abs( float(row.get("Annotation")) -float(result[8])  ),1))
            writer.writerow(result)

        ogfiles[i].close()







if __name__ == "__main__":
    annotate()