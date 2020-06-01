CALL db.index.fulltext.createNodeIndex("node",["Node"],["datasource", "label"]);
CREATE CONSTRAINT node_id_constraint ON (n:Node) ASSERT n.id IS UNIQUE;
