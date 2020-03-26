import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path
from mowgli.lib.etl.sentic.sentic_mappers import sentic_node, sentic_edge
from mowgli.lib.cskg.concept_net_predicates import RELATED_TO
from mowgli.lib.etl.sentic.sentic_constants import sentiment

_sample_sentic_file_path = Path(__file__).parent / 'test_data.owl'

@pytest.fixture
def strengths():
    return open(_sample_sentic_file_path)

@pytest.fixture
def url():
    return "https://github.com/famildtesting/test_data/archive/master.zip"

@pytest.fixture
def sample_sentic_nodes():
    expected_node_names = {'face', 'book', 'time', 'lift', 'mask', 'half', 'life', 
        'whole', 'part','split' , 'full', 'swing', 'bat', 'dance', 'set', 'sway'}

    expected_nodes = set(sentic_node(name) for name in expected_node_names)
    return expected_nodes


@pytest.fixture
def sample_sentic_edges():
    expected_edge_tuples = [
        ('face', 'book',None,RELATED_TO),
        ('face', 'time',None,RELATED_TO),
        ('face', 'lift',None,RELATED_TO),
        ('face', 'mask',None,RELATED_TO),

        ('face', 'pleasantness',0,sentiment),
        ('face', 'attention',0.1,sentiment),
        ('face', 'sensitivity',0.416,sentiment),
        ('face', 'aptitude',-0.80,sentiment),
        ('face', 'polarity',-0.51,sentiment),

        ('half', 'life',None,RELATED_TO),
        ('half', 'whole',None,RELATED_TO),
        ('half', 'part',None,RELATED_TO),
        ('half', 'split',None,RELATED_TO),
        ('half', 'full',None,RELATED_TO),

        ('half', 'pleasantness',-0.74,sentiment),
        ('half', 'attention',0,sentiment),
        ('half', 'sensitivity',0.882,sentiment),
        ('half', 'aptitude',0.9,sentiment),
        ('half', 'polarity',-0.74,sentiment),

        ('swing', 'bat',None,RELATED_TO),
        ('swing', 'dance',None,RELATED_TO),
        ('swing', 'set',None,RELATED_TO),
        ('swing', 'sway',None,RELATED_TO),

        ('swing', 'pleasantness',-0.04,sentiment),
        ('swing', 'attention',0.127,sentiment),
        ('swing', 'sensitivity',-0.12,sentiment),
        ('swing', 'aptitude',0.223,sentiment),
        ('swing', 'polarity',0.061,sentiment)    
    ]

    expected_edges = set(sentic_edge(subject=c, object_=r, weight=w, predicate=p) for (c, r, w, p) in expected_edge_tuples)
    return expected_edges
