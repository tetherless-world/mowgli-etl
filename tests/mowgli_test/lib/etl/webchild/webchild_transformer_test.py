from mowgli.lib.cskg.edge import Edge
from mowgli.lib.cskg.node import Node
from mowgli.lib.etl.webchild.webchild_transformer import WebchildTransformer
from mowgli.lib.etl.webchild.webchild_constants import WEBCHILD_MEMBEROF_DATASOURCE_ID, WEBCHILD_PHYSICAL_DATASOURCE_ID,WEBCHILD_NAMESPACE, WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,WEBCHILD_WORD_NET_WRAPPER
from mowgli.lib.cskg.concept_net_predicates import HAS_A, PART_OF, DEFINED_AS,MADE_OF
import pathlib
import os

def test_memberof_transform():
   
    expected_memberof_node_names = ['welfare state', 'membership', 'Flaviviridae', 'Brotulidae', 'Bunyaviridae', 'Juncaceae', 'arthropod family', 'subfamily']
    expected_memberof_node_ids = ['108178085', '108400965', '102558980', '101332653', '111743109', '101331345', '101759182', '108108627']
    expected_memberof_nodes = set()

    for i in range(0,len(expected_memberof_node_names)):
        expected_memberof_nodes.add(Node(datasource="webchild", id="webchild:" + expected_memberof_node_ids[i], label=expected_memberof_node_names[i]))

    relation = HAS_A

    expected_memberof_edge_tuples = [
        (WEBCHILD_MEMBEROF_DATASOURCE_ID,'welfare state', relation, 'membership'),
        (WEBCHILD_MEMBEROF_DATASOURCE_ID,'Brotulidae', relation, 'Flaviviridae'),
        (WEBCHILD_MEMBEROF_DATASOURCE_ID,'Juncaceae', relation, 'Bunyaviridae'),
        (WEBCHILD_MEMBEROF_DATASOURCE_ID,'arthropod family', relation, 'subfamily')
    ]
    expected_memberof_edges = set(Edge(datasource="webchild", object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation,object2_node) in expected_memberof_edge_tuples)

    assert relation ==  '/r/HasA'
    assert WEBCHILD_MEMBEROF_DATASOURCE_ID == 'webchild_member_of'
    return (expected_memberof_nodes,expected_memberof_edges)

def test_physical_transform():
    

    expected_physical_node_names = ['half blood', 'instep', 'transferee', 'musculus adductor brevis', 'Chartist', 'trachea', 'starer', 'metacarpal vein', 'godmother', 'breast', 'towhee', 'dentate nucleus', 'place-kicker', 'instep']
    expected_physical_node_ids = ['110157271', '105576950', '110724570', '105291945', '109911051', '105532050', '110648909', '105373790','110134870','105553288','101541922','105485988','110436851','105576950']
    expected_physical_nodes = set()

    for i in range(0,len(expected_physical_node_names)):
        expected_physical_nodes.add(Node(datasource="webchild", id="webchild:" + expected_physical_node_ids[i], label=expected_physical_node_names[i]))


    relation = HAS_A

    expected_physical_edge_tuples = [
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'half blood', relation, 'instep'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'transferee', relation, 'musculus adductor brevis'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'Chartist', relation, 'trachea'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'starer', relation, 'metacarpal vein'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'scoinson arch', relation, 'steel'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'godmother', relation, 'breast'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'towhee', relation, 'dentate nucleus'),
        (WEBCHILD_PHYSICAL_DATASOURCE_ID,'place-kicker', relation, 'instep')
    ]
    expected_physical_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation,object2_node) in expected_physical_edge_tuples)

    assert relation ==  '/r/HasA'
    assert WEBCHILD_PHYSICAL_DATASOURCE_ID == 'webchild_physical'
    return (expected_physical_nodes, expected_physical_edges)

def test_substanceof_transform():
    
    expected_substanceof_node_names = ['cloth', 'fibre', 'boiler', 'steel', 'brooklet', 'buffer', 'pharmacologist', 'tissue', 'scoinson arch', 'steel', 'alderleaf Juneberry', 'lignum', 'club', 'glucosamine']
    expected_substanceof_node_ids = ['103309808', '114866889', '102863750', '114802450', '109229641', '114785941', '110421753', '105267345', '104148464', '114802450', '112623818', '113096779', '103053788', '114752323']
    
    expected_substanceof_nodes = set()

    for i in range(0,len(expected_substanceof_node_names)):
        expected_substanceof_nodes.add(Node(datasource=WEBCHILD_SUBSTANCEOF_DATASOURCE_ID, id="webchild:" + expected_substanceof_node_ids[i], label=expected_substanceof_node_names[i]))


    relation = MADE_OF
    
    expected_substanceof_edge_tuples = [
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'cloth', relation, 'fibre'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'boiler', relation, 'steel'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'brooklet', relation, 'buffer'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'pharmacologist', relation, 'tissue'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'scoinson arch', relation, 'steel'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'alderleaf Juneberry', relation, 'lignum'),
        (WEBCHILD_SUBSTANCEOF_DATASOURCE_ID,'club', relation, 'glucosamine')
    ]
    expected_substanceof_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation,object2_node) in expected_substanceof_edge_tuples)
    
    assert relation ==  '/r/MadeOf'
    assert WEBCHILD_SUBSTANCEOF_DATASOURCE_ID == 'webchild_substance_of'
    return (expected_substanceof_nodes, expected_substanceof_edges)

def test_wordnet_transform():
    
    expected_wordnet_node_names = ['entity', 
                                    'that which is perceived or known or inferred to have its own distinct existence (living or nonliving)', 
                                    'physical entity', 
                                    'an entity that has physical existence', 
                                    'abstraction', 
                                    'a general concept formed by extracting common features from specific examples', 
                                    'abstract entity' 
                                    ]

    expected_wordnet_node_names = ['100001740','100001740', '100001930', '100001930', '100002137','100002137', '100002137', '100002137']

    
    expected_wordnet_nodes = set()

    for i in range(0,len(expected_wordnet_node_names)):
        expected_wordnet_nodes.add(Node(datasource=WEBCHILD_SUBSTANCEOF_DATASOURCE_ID, id="webchild:" + expected_wordnet_node_names[i], label=expected_wordnet_node_names[i]))

    relation = DEFINED_AS 
    
    expected_wordnet_edge_tuples = [
        ('webchild_word_net_wrapper','entity', relation, 'that which is perceived or known or inferred to have its own distinct existence (living or nonliving)'),
        ('webchild_word_net_wrapper','physical entity', relation, 'an entity that has physical existence'),
        ('webchild_word_net_wrapper','abstraction', relation, 'a general concept formed by extracting common features from specific examples'),
        ('webchild_word_net_wrapper','abstract entity', relation, 'a general concept formed by extracting common features from specific examples')
    ]
    expected_wordnet_edges = set(Edge(datasource=datasource, object_=object1_node, relation=relation, subject=object2_node) for (datasource,object1_node,relation,object2_node) in expected_wordnet_edge_tuples)

    assert relation ==  '/r/DefinedAs'
    assert WEBCHILD_WORD_NET_WRAPPER == 'webchild_word_net_wrapper'
    return (expected_wordnet_nodes, expected_wordnet_edges)


def test_transform():
    
    transformer = WebchildTransformer()
    
    memberof_file_path =str(pathlib.Path(__file__).parent.absolute().joinpath('test_webchild_partof_memberof.txt'))
    physical_file_path = str(pathlib.Path(__file__).parent.absolute().joinpath('test_webchild_partof_physical.txt'))
    substanceof_file_path = str(pathlib.Path(__file__).parent.absolute().joinpath('test_webchild_partof_substanceof.txt'))
    wordnet_file_path = str(pathlib.Path(__file__).parent.absolute().joinpath('test_WordNetWrapper.txt'))

    memberof_nodes, memberof_edges,physical_nodes,physical_edges, substanceof_nodes, substanceof_edges, wordnet_nodes, wordnet_edges = set(), set(),set(),set(),set(),set(),set(),set()
    for result in transformer.transform(memberof_csv_file_path = memberof_file_path, physical_csv_file_path=physical_file_path,substanceof_csv_file_path= substanceof_file_path,wordnet_csv_file_path = wordnet_file_path):
        if isinstance(result, Node):
            if(result.datasource == 'webchild_member_of'):
                memberof_nodes.add(result)
            elif(result.datasource == 'webchild_physical'):
                physical_nodes.add(result)
            elif(result.datasource == 'webchild_substance_of'):
                substanceof_nodes.add(result)
            elif(result.datasource == 'webchild_word_net_wrapper'):
                wordnet_nodes.add(result)
        elif isinstance(result, Edge):
            if(result.datasource == 'webchild_member_of'):
                memberof_edges.add(result)
            elif(result.datasource == 'webchild_physical'):
                physical_edges.add(result)
            elif(result.datasource == 'webchild_substance_of'):
                substanceof_edges.add(result)
            elif(result.datasource == 'webchild_word_net_wrapper'):
                wordnet_edges.add(result)

    expected_member_of_nodes,expected_member_of_edges = test_memberof_transform()
    expected_physical_nodes,expecetd_physical_edges = test_physical_transform()
    expected_substanceof_nodes,expecetd_substanceof_edges = test_substanceof_transform()
    expected_wordnet_nodes,expecetd_wordnet_edges = test_wordnet_transform()
    


    memberof_nodes = list(memberof_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    expected_member_of_nodes = list(expected_member_of_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    
    memberof_edges = list(memberof_edges).sort(key=lambda x: x._Edge__object, reverse=False)
    expected_member_of_edges = list(expected_member_of_edges).sort(key=lambda x: x._Edge__object, reverse=False)

    physical_nodes = list(physical_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    expected_physical_nodes = list(expected_physical_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    
    physical_edges = list(physical_edges).sort(key=lambda x: x._Edge__object, reverse=False)
    expecetd_physical_edges = list(expecetd_physical_edges).sort(key=lambda x: x._Edge__object, reverse=False)
    
    substanceof_nodes = list(substanceof_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    expected_substanceof_nodes = list(expected_substanceof_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    
    substanceof_edges = list(substanceof_edges).sort(key=lambda x: x._Edge__object, reverse=False)
    expecetd_substanceof_edges = list(expecetd_substanceof_edges).sort(key=lambda x: x._Edge__object, reverse=False)

    wordnet_nodes = list(wordnet_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    expected_wordnet_nodes = list(expected_wordnet_nodes).sort(key=lambda x: x._Node__label, reverse=False)
    
    wordnet_edges = list(wordnet_edges).sort(key=lambda x: x._Edge__object, reverse=False)
    expecetd_wordnet_edges = list(expecetd_wordnet_edges).sort(key=lambda x: x._Edge__object, reverse=False)



    assert memberof_nodes ==  expected_member_of_nodes
    assert memberof_edges ==  expected_member_of_edges
    assert physical_nodes ==  expected_physical_nodes
    assert physical_edges ==  expecetd_physical_edges
    assert substanceof_nodes ==  expected_substanceof_nodes
    assert substanceof_edges ==  expecetd_substanceof_edges
    assert wordnet_nodes ==  expected_wordnet_nodes
    assert wordnet_edges ==  expecetd_wordnet_edges
    



