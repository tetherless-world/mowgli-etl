from pathlib import Path

import pytest

from mowgli.lib.etl.mapper.concept_net.concept_net_index import ConceptNetIndex


@pytest.fixture
def concept_net_index(tmpdir):
    return ConceptNetIndex(Path(tmpdir), limit=10000, report_progress=True)


def test_get(concept_net_index):
    # There is only one "a" label
    assert concept_net_index.get("a") == "/c/en/a"
    # There are multiple "30" labels, return the unqualified node id
    assert concept_net_index.get("30") == "/c/en/30"
    # Return the "30" adjective
    assert concept_net_index.get("30", pos="a") == "/c/en/30/a/wn"
    # There's no "30" noun, should return the unqualified node id as above
    assert concept_net_index.get("30", pos="v") == "/c/en/30"
