import logging
import pickle
from pathlib import Path
from typing import Optional, Union, TextIO

from tqdm import tqdm

from mowgli import paths
from mowgli.lib.etl.pipeline.cskg.cskg_nodes_csv_transformer import CskgNodesCsvTransformer
from mowgli.lib.storage._leveldb import _Leveldb
from mowgli.lib.storage.cskg_release_archive import CskgReleaseArchive


class ConceptNetIndex(_Leveldb):
    __NAME_DEFAULT = paths.DATA_DIR / "cskg_release" / "indexed" / "concept_net"

    def __init__(self,
                 name: Optional[Union[str, Path]] = __NAME_DEFAULT, *,
                 limit: Optional[int] = None,
                 report_progress: bool = False,
                 **kwds):
        if id(name) == id(self.__NAME_DEFAULT):
            self.__NAME_DEFAULT.mkdir(parents=True)
        _Leveldb.__init__(self, name=name, **kwds)
        self.__logger = logging.getLogger(self.__class__.__name__)
        for _ in self._db.iterator(include_value=False):
            self.__logger.info("ConceptNet label index already built")
            return

        try:
            with CskgReleaseArchive() as cskg_release_archive:
                with cskg_release_archive.open_nodes_csv("conceptnet") as nodes_csv_file:
                    self.__build(nodes_csv_file=nodes_csv_file, limit=limit, report_progress=report_progress)
        except FileNotFoundError:
            self.__logger.warning("could not open ConceptNet nodes.csv from CSKG release")
            return

    def __build(self, *, nodes_csv_file: TextIO, limit: Optional[int], report_progress: bool):
        self.__logger.info("building ConceptNet index")
        nodes = CskgNodesCsvTransformer().transform(nodes_csv_file=nodes_csv_file)
        if report_progress:
            nodes = tqdm(nodes)
        for node_i, node in enumerate(nodes):
            if node.label.lower() != node.label:
                raise AssertionError(f"label is not lower-case: {node.label}")
            if node.aliases:
                raise AssertionError(f"node has aliases: {node.aliases}")

            assert '/' not in node.label
            key = self.__label_to_key(node.label)

            # Store the node ID(s) as the value
            # Other information, such as the part of speech, can be reconstructed from it.
            value = node.id

            existing_values = self._db.get(key)
            if existing_values is not None:
                existing_values = pickle.loads(existing_values)
                if isinstance(existing_values, str):
                    new_values = [existing_values, value]
                else:
                    assert isinstance(existing_values, list)
                    existing_values.append(value)
                    new_values = existing_values
            else:
                new_values = node.id

            self._db.put(node.label.encode("utf-8"), pickle.dumps(new_values))

            if limit is not None and node_i + 1 == limit:
                break
        self.__logger.info("built ConceptNet index")

    def get(self, label: str, *, pos: Optional[str] = None) -> Optional[str]:
        """
        Get the ConceptNet node ID corresponding to a label and optional part of speech.
        """
        value = self._db.get(self.__label_to_key(label))
        if value is None:
            return None
        node_id = pickle.loads(value)
        if isinstance(node_id, str):
            return node_id
        node_ids = node_id
        assert isinstance(node_ids, list)
        if pos is None:
            return node_ids[0]
        parsed_node_ids = []
        # Parse the node id's with the same label
        # If there's one that corresponds exactly with the requested qualifiers, return it.
        node_id_without_qualifiers = None
        for node_id in node_ids:
            node_id_split = node_id.split('/')
            assert len(node_id_split) >= 4
            unqualified_node_id, qualifiers = '/'.join(node_id_split[:4]), node_id_split[4:]
            if qualifiers:
                node_pos = qualifiers.pop(0)
                if node_pos == pos:
                    return node_id
            else:
                node_id_without_qualifiers = node_id
        # No node id corresponds exactly with the requested qualifiers, return a node id without qualifiers if we have one.
        return node_id_without_qualifiers

    def __label_to_key(self, label: str):
        return label.encode("utf-8")
