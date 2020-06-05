package stores

import com.outr.lucene4s.{DirectLucene, Lucene}
import models.cskg.{Edge, Node}

import scala.util.Random

class MemStore(val edges: List[Edge], val nodes: List[Node]) extends Store {
  private val lucene = new DirectLucene(List("datasource", "id", "label"))
  private val luceneNodeDatasourceField = lucene.create.field[String]("datasource", fullTextSearchable = true)
  private val luceneNodeIdField = lucene.create.field[String]("id", fullTextSearchable = true)
  private val luceneNodeLabelField = lucene.create.field[String]("label", fullTextSearchable = true)
  nodes.foreach(node => {
    lucene.doc().fields(luceneNodeDatasourceField(node.datasource), luceneNodeIdField(node.id), luceneNodeLabelField(node.label)).index()
  })
  private val nodesById = nodes.map(node => (node.id, node)).toMap
  private val random = new Random()
  private val datasources = nodes.flatMap(_.datasource.split(",")).distinct

  final override def getDatasources: List[String] =
    this.datasources

  final override def getEdgesByObject(objectNodeId: String): List[Edge] =
    edges.filter(edge => edge.`object` == objectNodeId)

  final override def getEdgesBySubject(subjectNodeId: String): List[Edge] =
    edges.filter(edge => edge.subject == subjectNodeId)

  final override def getNodeById(id: String): Option[Node] =
    nodesById.get(id)

  final override def getMatchingNodes(limit: Int, offset: Int, text: String): List[Node] = {
    val results = lucene.query().filter(text).limit(limit).offset(offset).search()
    results.results.toList.map(searchResult => nodesById(searchResult(luceneNodeIdField)))
  }

  final override def getMatchingNodesCount(text: String): Int = {
    val results = lucene.query().filter(text).search()
    results.total.intValue
  }

  override def getRandomNode: Node =
    nodes(random.nextInt(nodes.size))

  final override def getTotalEdgesCount: Int =
    edges.size

  final override def getTotalNodesCount: Int =
    nodes.size
}
