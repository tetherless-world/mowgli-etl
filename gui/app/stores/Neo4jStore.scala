package stores
import com.google.inject.Inject
import models.cskg.{Edge, Node}
import org.neo4j.driver.{AuthTokens, GraphDatabase, Record, Result, Session}

import scala.io.Source
import scala.collection.JavaConverters._

class Neo4jStore @Inject()(configuration: Neo4jStoreConfiguration) extends Store with WithResource {
  private val driver = GraphDatabase.driver(configuration.uri, AuthTokens.basic(configuration.user, configuration.password))
  private val edgePropertyNames = List("datasource", "other", "weight")
  private val nodePropertyNames = List("aliases", "datasource", "id", "label", "other", "pos")

  final def bootstrap(): Unit = {
    val bootstrapCypherStatements =
      withResource(getClass.getResourceAsStream("/cypher/bootstrap.cypher")) { inputStream =>
        Source.fromInputStream(inputStream).getLines().toList
      }

    withSession { session =>
      session.writeTransaction { transaction =>
        for (bootstrapCypherStatement <- bootstrapCypherStatements) {
          transaction.run(bootstrapCypherStatement)
        }
        transaction.commit()
      }
    }
  }

  final def clear(): Unit = {
    val clearCypherString =
      withResource(getClass.getResourceAsStream("/cypher/clear.cypher")) { inputStream =>
        Source.fromInputStream(inputStream).mkString
      }

    withSession { session =>
      session.writeTransaction { transaction =>
        transaction.run(clearCypherString)
        transaction.commit()
      }
    }
  }

  override final def getEdgesByObject(objectNodeId: String): List[Edge] = {
    withSession { session =>
      session.readTransaction { transaction => {
        val result =
          transaction.run(
            s"MATCH (subject:Node)-[edge]->(object:Node {id: $$objectNodeId}) RETURN type(edge), object.id, subject.id, ${edgePropertyNames.map(edgePropertyName => "edge." + edgePropertyName).mkString(", ")};",
            Map(
              "objectNodeId" -> objectNodeId
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        getEdgesFromRecords(result)
      }
      }
    }
  }


  override final def getEdgesBySubject(subjectNodeId: String): List[Edge] = {
    withSession { session =>
      session.readTransaction { transaction => {
        val result =
          transaction.run(
            s"MATCH (subject:Node {id: $$subjectNodeId})-[edge]->(object:Node) RETURN type(edge), object.id, subject.id, ${edgePropertyNames.map(edgePropertyName => "edge." + edgePropertyName).mkString(", ")};",
            Map(
              "subjectNodeId" -> subjectNodeId
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        getEdgesFromRecords(result)
      }
      }
    }
  }

  override final def getNodeById(id: String): Option[Node] = {
    withSession { session =>
      session.readTransaction { transaction => {
        val result =
          transaction.run(
            s"MATCH (node:Node {id: $$id}) RETURN ${nodePropertyNames.map(nodePropertyName => "node." + nodePropertyName).mkString(", ")};",
            Map("id" -> id).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        val nodes = getNodesFromRecords(result)
        nodes.headOption
      }
      }
    }
  }

  final override def getMatchingNodes(limit: Int, offset: Int, text: String): List[Node] =
    withSession { session =>
      session.readTransaction { transaction =>
        val result =
          transaction.run(
            s"""CALL db.index.fulltext.queryNodes("nodeLabel", $$nodeLabel) YIELD node, score
              |RETURN ${nodePropertyNames.map(nodePropertyName => "node." + nodePropertyName).mkString(", ")}
              |SKIP ${offset}
              |LIMIT ${limit}
              |""".stripMargin,
            Map(
              "nodeLabel" -> text
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
          getNodesFromRecords(result)
      }
    }

  final override def getMatchingNodesCount(text: String): Int =
    withSession { session =>
      session.readTransaction { transaction =>
        val result =
          transaction.run(
            s"""CALL db.index.fulltext.queryNodes("nodeLabel", $$nodeLabel) YIELD node, score
               |RETURN COUNT(node)
               |""".stripMargin,
            Map(
              "nodeLabel" -> text
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        val record = result.single()
        record.get("COUNT(node)").asInt()
      }
    }

  private def getEdgeFromRecord(record: Record): Edge = {
    val recordMap = record.asMap().asScala.toMap.asInstanceOf[Map[String, Object]]
    Edge(
      datasource = recordMap("edge.datasource").asInstanceOf[String],
      `object` = recordMap("object.id").asInstanceOf[String],
      other = Option(recordMap("edge.other")).map(other => other.asInstanceOf[String]),
      predicate = recordMap("type(edge)").asInstanceOf[String],
      subject = recordMap("subject.id").asInstanceOf[String],
      weight = Option(recordMap("edge.weight")).map(weight => weight.asInstanceOf[Double].floatValue())
    )
  }

  private def getEdgesFromRecords(result: Result): List[Edge] =
    result.asScala.toList.map(record => getEdgeFromRecord(record))

  private def getNodeFromRecord(record: Record): Node = {
    val recordMap = record.asMap().asScala.toMap.asInstanceOf[Map[String, String]]
    Node(
      aliases = Option(recordMap("node.aliases")).map(aliases => aliases.split(' ').toList),
      datasource = recordMap("node.datasource"),
      id = recordMap("node.id"),
      label = recordMap("node.label"),
      other = Option(recordMap("node.other")),
      pos = Option(recordMap("node.pos"))
    )
  }

  private def getNodesFromRecords(result: Result): List[Node] =
    result.asScala.toList.map(record => getNodeFromRecord(record))

  final override def getTotalEdgesCount: Int =
    withSession { session =>
      session.readTransaction { transaction =>
        val result = transaction.run("MATCH ()-[r]->() RETURN COUNT(*) as count")
        val record = result.single()
        record.get("count").asInt()
      }
    }

  final override def getTotalNodesCount: Int =
    withSession { session =>
      session.readTransaction { transaction =>
        val result = transaction.run("MATCH (n) RETURN COUNT(n) as count")
        val record = result.single()
        record.get("count").asInt()
      }
    }

  final def putEdges(edges: List[Edge]): Unit = {
    withSession { session =>
      session.writeTransaction { transaction =>
        for (edge <- edges) {
          //          CREATE (:Node { id: node.id, label: node.label, aliases: node.aliases, pos: node.pos, datasource: node.datasource, other: node.other });
          transaction.run(
            """MATCH (subject:Node {id: $subject}), (object:Node {id: $object})
              |CALL apoc.create.relationship(subject, $predicate, {datasource: $datasource, weight: toFloat($weight), other: $other}, object) YIELD rel
              |REMOVE rel.noOp
              |""".stripMargin,
            Map(
              "datasource" -> edge.datasource,
              "object" -> edge.`object`,
              "other" -> edge.other.getOrElse(null),
              "predicate" -> edge.predicate,
              "subject" -> edge.subject,
              "weight" -> edge.weight.getOrElse(null)
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        }
        transaction.commit()
      }
    }
  }

  final def putNodes(nodes: List[Node]): Unit = {
    withSession { session =>
      session.writeTransaction { transaction =>
        for (node <- nodes) {
          //          CREATE (:Node { id: node.id, label: node.label, aliases: node.aliases, pos: node.pos, datasource: node.datasource, other: node.other });
          transaction.run(
            "CREATE (:Node { id: $id, label: $label, aliases: $aliases, pos: $pos, datasource: $datasource, other: $other });",
            Map(
              "aliases" -> node.aliases.map(aliases => aliases.mkString(" ")).getOrElse(null),
              "datasource" -> node.datasource,
              "id" -> node.id,
              "label" -> node.label,
              "pos" -> node.pos.getOrElse(null),
              "other" -> node.other.getOrElse(null)
            ).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        }
        transaction.commit()
      }
    }
  }

  private def withSession[V](f: Session => V): V =
    withResource[Session, V](driver.session())(f)
}
