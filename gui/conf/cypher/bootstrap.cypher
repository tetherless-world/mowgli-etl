CALL db.index.fulltext.createNodeIndex("nodeLabel",["Node"],["label"]);
CREATE CONSTRAINT node_id_constraint ON (n:Node) ASSERT n.id IS UNIQUE;
