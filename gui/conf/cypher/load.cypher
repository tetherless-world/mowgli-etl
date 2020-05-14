USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS node FIELDTERMINATOR '\t'
CREATE (:Node { id: node.id, label: node.label, aliases: node.aliases, pos: node.pos, datasource: node.datasource, other: node.other });
//RETURN node.id;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS edge FIELDTERMINATOR '\t'
MATCH (subject:Node {id: edge.subject}), (object:Node {id: edge.object})
CALL apoc.create.relationship(subject, edge.predicate, {datasource: edge.datasource, weight: toFloat(edge.weight), other: edge.other}, object) YIELD rel
REMOVE rel.noOp;
//RETURN edge.subject + "," + edge.predicate + "," + edge.object;
