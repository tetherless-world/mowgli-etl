package stores

import org.scalatest.{Matchers, WordSpec}

abstract class StoreSpec extends WordSpec with Matchers {
  val sut: Store

  protected def getEdgesBySubject() = {
    val node = TestData.nodes(0)
    val edges = sut.getEdgesBySubject(node.id)
    edges should not be empty
    for (edge <- edges) {
      edge.subject should equal(node.id)
    }
  }

  protected def getNodeById() = {
    val expected = TestData.nodes(0)
    val actual = sut.getNodeById(expected.id)
    actual should equal(expected)
  }

  protected def searchNodes(): Unit = {
    val expected = TestData.nodes(0)
    val actual = sut.searchNodes(limit = 10, offset = 0, text = expected.label)
    actual should not be empty
    actual(0) should equal(expected)
  }
}
