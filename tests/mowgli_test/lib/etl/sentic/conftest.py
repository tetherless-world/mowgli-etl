import bz2
import pytest
from io import TextIOWrapper
from pathlib import Path
from mowgli.lib.etl.sentic.sentic_mappers import sentic_node, sentic_edge

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
        ('face', 'book'),
        ('face', 'time'),
        ('face', 'lift'),
        ('face', 'mask'),
        ('half', 'life'),
        ('half', 'whole'),
        ('half', 'part'),
        ('half', 'split'),
        ('half', 'full'),
        ('swing', 'bat'),
        ('swing', 'dance'),
        ('swing', 'set'),
        ('swing', 'sway')    
    ]

    expected_edges = set(sentic_edge(subject=c, object_=r) for (c, r) in expected_edge_tuples)
    return expected_edges
