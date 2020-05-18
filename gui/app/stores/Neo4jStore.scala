package stores
import com.google.inject.Inject
import models.cskg.{Edge, Node}
import org.neo4j.driver.{AuthTokens, GraphDatabase, Session}

import scala.io.Source
import scala.collection.JavaConverters._

class Neo4jStore @Inject()(configuration: Neo4jStoreConfiguration) extends Store with WithResource {
  private val driver = GraphDatabase.driver(configuration.uri, AuthTokens.basic(configuration.user, configuration.password))

  def bootstrap(): Unit = {
    val bootstrapCypherString =
      withResource(getClass.getResourceAsStream("/cypher/bootstrap.cypher")) { inputStream =>
        Source.fromInputStream(inputStream).mkString
      }

    withSession { session =>
      session.writeTransaction { transaction =>
        transaction.run(bootstrapCypherString)
        transaction.commit()
      }
    }
  }

  def clear(): Unit = {
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

  override def getEdgesBySubject(subjectNodeId: String): List[Edge] = throw new UnsupportedOperationException

  override def getNodeById(id: String): Node = {
    withSession { session =>
      session.readTransaction { transaction => {
        val result =
          transaction.run(
            "MATCH (node:Node {id: $id}) RETURN node.aliases, node.datasource, node.label, node.other, node.pos;",
            Map("id" -> id).asJava.asInstanceOf[java.util.Map[String, Object]]
          )
        val record = result.single()
        val recordMap = record.asMap().asScala.toMap.asInstanceOf[Map[String, String]]
        Node(
          aliases = Option(recordMap("node.aliases")).map(aliases => aliases.split(' ').toList),
          datasource = recordMap("node.datasource"),
          id = id,
          label = recordMap("node.label"),
          other = Option(recordMap("node.other")),
          pos = Option(recordMap("node.pos"))
        )
      }
      }
    }
  }

  def putNodes(nodes: List[Node]): Unit = {
    withSession { session =>
      session.writeTransaction { transaction =>
        for (node <- nodes) {
          //          CREATE (:Node { id: node.id, label: node.label, aliases: node.aliases, pos: node.pos, datasource: node.datasource, other: node.other });
          transaction.run(
            "CREATE (:Node { id: $id, label: $label, aliases: $aliases, pos: $pos, datasource: $datasource, other: $other });",
            Map(
              "id" -> node.id,
              "label" -> node.label,
              "aliases" -> node.aliases.map(aliases => aliases.mkString(" ")).getOrElse(null),
              "pos" -> node.pos.getOrElse(null),
              "datasource" -> node.datasource,
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
