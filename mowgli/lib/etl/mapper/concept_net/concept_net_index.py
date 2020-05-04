import logging
import pickle
from pathlib import Path
from shutil import rmtree
from typing import Optional, Union, TextIO

import plyvel
from tqdm import tqdm

from mowgli import paths
from mowgli.lib.etl.pipeline.cskg.cskg_nodes_csv_transformer import CskgNodesCsvTransformer
from mowgli.lib.storage._closeable import _Closeable
from mowgli.lib.storage.cskg_release_archive import CskgReleaseArchive
from mowgli.lib.storage.level_db import LevelDb


class ConceptNetIndex(_Closeable):
    __NAME_DEFAULT = paths.DATA_DIR / "cskg_release" / "indexed" / "concept_net"

    def __init__(self, db: LevelDb):
        self.__db = db

    @classmethod
    def __build(cls, *, db: LevelDb, nodes_csv_file: TextIO, limit: Optional[int], report_progress: bool):
        logger = logging.getLogger(cls.__name__)
        logger.info("building ConceptNet index")
        nodes = CskgNodesCsvTransformer().transform(nodes_csv_file=nodes_csv_file)
        if report_progress:
            nodes = tqdm(nodes)
        for node_i, node in enumerate(nodes):
            if node.label.lower() != node.label:
                raise AssertionError(f"label is not lower-case: {node.label}")
            if node.aliases:
                raise AssertionError(f"node has aliases: {node.aliases}")

            assert '/' not in node.label
            key = cls.__label_to_key(node.label)

            # Store the node ID(s) as the value
            # Other information, such as the part of speech, can be reconstructed from it.
            value = node.id

            existing_values = db.db.get(key)
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

            db.db.put(node.label.encode("utf-8"), pickle.dumps(new_values))

            if limit is not None and node_i + 1 == limit:
                break
        db.db.compact_range()  # Compact the underlying storage
        logger.info("built ConceptNet index")

    def close(self):
        self.__db.close()

    @classmethod
    def create(
            cls,
            name: Optional[Union[str, Path]] = __NAME_DEFAULT,
            *,
            limit: Optional[int] = None,
            nodes_csv_file: Optional[Union[Path, TextIO]] = None,  # Primarily for testing
            report_progress: bool = False
    ):
        if not isinstance(name, Path):
            name = Path(name)
        if name.exists():
            rmtree(name)
        name.mkdir(parents=True)
        db = LevelDb(name=name, create_if_missing=True)

        if nodes_csv_file is not None:
            cls.__build(db=db, nodes_csv_file=nodes_csv_file, limit=limit, report_progress=report_progress)
        else:
            with CskgReleaseArchive() as cskg_release_archive:
                with cskg_release_archive.open_nodes_csv("conceptnet") as nodes_csv_file:
                    cls.__build(db=db, nodes_csv_file=nodes_csv_file, limit=limit, report_progress=report_progress)

        return cls(db)

    @classmethod
    def open(cls, name: Optional[Union[str, Path]] = __NAME_DEFAULT):
        try:
            return cls(LevelDb(name=name, create_if_missing=False))
        except plyvel.Error:
            raise FileNotFoundError

    def get(self, label: str, *, pos: Optional[str] = None) -> Optional[str]:
        """
        Get the ConceptNet node ID corresponding to a label and optional part of speech.
        """
        value = self.__db.db.get(self.__label_to_key(label))
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

    @staticmethod
    def __label_to_key(label: str):
        return label.encode("utf-8")
