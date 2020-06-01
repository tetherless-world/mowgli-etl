package stores

import com.google.inject.ImplementedBy
import models.cskg.{Edge, Node}

@ImplementedBy(classOf[Neo4jStore])
trait Store {
  /**
   * Get all of the edges that have the given node ID as an object.
   */
  def getEdgesByObject(objectNodeId: String): List[Edge]

  /**
   * Get all of the edges that have the given node ID as a subject.
   */
  def getEdgesBySubject(subjectNodeId: String): List[Edge]

  /**
   * Fulltext search nodes.
   */
  def getMatchingNodes(limit: Int, offset: Int, text: String): List[Node]

  /**
   * Get count of fulltext search results.
   */
  def getMatchingNodesCount(text: String): Int;

  /**
   * Get a node by ID.
   */
  def getNodeById(id: String): Option[Node]

  /**
   * Get toal number of edges.
   */
  def getTotalEdgesCount: Int;

  /**
   * Get total number of nodes.
   */
  def getTotalNodesCount: Int;
}
