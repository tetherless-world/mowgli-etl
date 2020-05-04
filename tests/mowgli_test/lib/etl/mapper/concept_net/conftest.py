from pathlib import Path

import pytest

try:
    from mowgli.lib.etl.mapper.concept_net.concept_net_index import ConceptNetIndex
except ImportError:
    ConceptNetIndex = None

if ConceptNetIndex is not None:
    @pytest.fixture
    def concept_net_index(tmpdir):
        concept_net_index = ConceptNetIndex.create(name=Path(tmpdir), limit=10000,
                                                   report_progress=True)
        yield concept_net_index
        concept_net_index.close()
