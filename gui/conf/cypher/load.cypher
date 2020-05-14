USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///nodes.csv' AS node FIELDTERMINATOR '\t'
CREATE (:Node { id: node.id, label: node.label, aliases: node.aliases, pos: node.pos, datasource: node.datasource, other: node.other })
RETURN linenumber() AS number
