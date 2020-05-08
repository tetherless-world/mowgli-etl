from pathlib import Path

try:
    from mowgli_etl.mapper.concept_net.concept_net_index import ConceptNetIndex
except ImportError:
    ConceptNetIndex = None

if ConceptNetIndex is not None:
    def create(tmpdir):
        return ConceptNetIndex.create(directory_path=Path(tmpdir), limit=10000,
                                      report_progress=True)


    def test_create(tmpdir):
        create(tmpdir)


    def test_get(tmpdir):
        with create(tmpdir) as index:
            # There is only one "a" label
            assert index.get("a") == "/c/en/a"
            # There are multiple "30" labels, return the unqualified node id
            assert index.get("30") == "/c/en/30"
            # Return the "30" adjective
            assert index.get("30", pos="a") == "/c/en/30/a/wn"
            # There's no "30" noun, should return the unqualified node id as above
            assert index.get("30", pos="v") == "/c/en/30"


    def test_open(tmpdir):
        with create(tmpdir) as _:
            pass
        with ConceptNetIndex.open(tmpdir) as index:
            assert index.get("a") == "/c/en/a"

