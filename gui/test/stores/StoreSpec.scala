package stores

import org.scalatest.{Matchers, WordSpec}

abstract class StoreSpec extends WordSpec with Matchers {
  val sut: Store

  protected def getEdgesByObject(): Unit = {
    for (node <- TestData.nodes) {
      val edges = sut.getEdgesByObject(node.id)
      if (!edges.isEmpty) {
        for (edge <- edges) {
          edge.`object` should equal(node.id)
          return
        }
      }
    }
  }

  protected def getEdgesBySubject() = {
    val node = TestData.nodes(0)
    val edges = sut.getEdgesBySubject(node.id)
    edges should not be empty
    for (edge <- edges) {
      edge.subject should equal(node.id)
    }
  }


  protected def getMatchingNodes(): Unit = {
    val expected = TestData.nodes(0)
    val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = expected.label)
    actual should not be empty
    actual(0) should equal(expected)
  }

  protected def getMatchingNodesCount(): Unit = {
    val expected = TestData.nodes(0)
    val actual = sut.getMatchingNodesCount(text = expected.label)
    actual should be >= 1
  }

  protected def getNodeById() = {
    val expected = TestData.nodes(0)
    val actual = sut.getNodeById(expected.id)
    actual should equal(expected)
  }
}
