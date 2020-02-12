from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.webchild.webchild_transformer import WebchildTransformer
from mowgli.lib.etl.webchild.webchild_transformer import WebchildTransformer
import pathlib
import os

def test_transform():
    file_list = os.listdir(os.getcwd())
    txt_list = []
    for file in file_list:
        if file[-3] == "txt":
            txt_list.append(file)

    nodes, edges = set(), set()
    for file_name in txt_list:
        for result in transformer.transform(csv_file_path=file_name):
            if isinstance(result, Node):
                nodes.add(result)
            elif isinstance(result, Edge):
                edges.add(result)
        if 'memberof' in file_name:
            expected_memberof_node_names = ['welfare state', 'membership', 'Flaviviridae', 'Brotulidae', 'Bunyaviridae', 'Juncaceae', 'arthropod family', 'subfamily']
            expected_memberof_nodes = set(Node(name) for name in  expected_node_names)

            relation = '/r/HasA'

            expected_memberof_edge_tuples = [
                ('webchild_member_of','welfare state', relation, 'membership'),
                ('webchild_member_of','Brotulidae', relation, 'Flaviviridae'),
                ('webchild_member_of','Juncaceae', relation, 'Bunyaviridae'),
                ('webchild_member_of','arthropod family', relation, 'subfamily'),
            ]
            expected_memberof_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation.object2_node) in expected_edge_tuples)

            assert nodes == expected_memberof_nodes
            assert edges == expected_memberof_edges
        elif 'substanceof' in file_name:
            expected_substanceof_node_names = ['cloth', 'fibre', 'boiler', 'steel', 'brooklet', 'buffer', 'pharmacologist', 'tissue', 'scoinson arch', 'steel', 'alderleaf Juneberry', 'lignum', 'club', 'glucosamine']
            expected_substanceof_nodes = set(Node(name) for name in  expected_node_names)

            relation = '/r/MadeOf'
            
            expected_substanceof_edge_tuples = [
                ('webchild_substance_of','cloth', relation, 'fibre'),
                ('webchild_substance_of','boiler', relation, 'steel'),
                ('webchild_substance_of','brooklet', relation, 'buffer'),
                ('webchild_substance_of','pharmacologist', relation, 'tissue'),
                ('webchild_substance_of','scoinson arch', relation, 'steel'),
                ('webchild_substance_of','alderleaf Juneberry', relation, 'lignum'),
                ('webchild_substance_of','club', relation, 'glucosamine')
            ]
            expected_substanceof_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation.object2_node) in expected_edge_tuples)

            assert nodes == expected_substanceof_nodes
            assert edges == expected_substanceof_edges
        elif 'physical' in file_name:

            expected_physical_node_names = ['half blood', 'instep', 'transferee', 'musculus adductor brevis', 'Chartist', 'trachea', 'starer', 'metacarpal vein', 'godmother', 'breast', 'towhee', 'dentate nucleus', 'place-kicker', 'instep']
            expected_physical_nodes = set(Node(name) for name in  expected_node_names)

            relation = '/r/HasA'

            expected_physical_edge_tuples = [
                ('webchild_physical_of','half blood', relation, 'instep'),
                ('webchild_physical_of','transferee', relation, 'musculus adductor brevis'),
                ('webchild_physical_of','Chartist', relation, 'trachea'),
                ('webchild_physical_of','starer', relation, 'metacarpal vein'),
                ('webchild_physical_of','scoinson arch', relation, 'steel'),
                ('webchild_physical_of','godmother', relation, 'breast'),
                ('webchild_physical_of','towhee', relation, 'dentate nucleus'),
                ('webchild_physical_of','place-kicker', relation, 'instep')
            ]
            expected_physical_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation.object2_node) in expected_edge_tuples)

            assert nodes == expected_physical_nodes
            assert edges == expected_physical_edges
        else:

            expected_word_net_node_names = ['entity', 
                                            'that which is perceived or known or inferred to have its own distinct existence (living or nonliving)', 
                                            'physical entity', 
                                            'an entity that has physical existence', 
                                            'abstraction', 
                                            'a general concept formed by extracting common features from specific examples', 
                                            'abstract entity' 
                                            ]
            expected_word_net_nodes = set(Node(name) for name in  expected_node_names)
            
            relation = '/r/DefinedAs'

            expected_word_net_edge_tuples = [
                ('webchild_word_net_wrapper','entity', relation, 'that which is perceived or known or inferred to have its own distinct existence (living or nonliving)'),
                ('webchild_word_net_wrapper','physical entity', relation, 'an entity that has physical existence'),
                ('webchild_word_net_wrapper','abstraction', relation, 'a general concept formed by extracting common features from specific examples'),
                ('webchild_word_net_wrapper','abstract entity', relation, 'a general concept formed by extracting common features from specific examples'),
            ]
            expected_word_net_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation.object2_node) in expected_edge_tuples)


            assert nodes == expected_word_net_nodes
            assert edges == expected_word_net_edges
