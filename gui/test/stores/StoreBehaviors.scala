package stores

import org.scalatest.{Matchers, WordSpec}

trait StoreBehaviors extends Matchers { this: WordSpec =>
  def store(sut: Store) {
    "get edges by object" in {
      for (node <- TestData.nodes) {
        val edges = sut.getEdgesByObject(node.id)
        if (!edges.isEmpty) {
          val edgeWithObject = edges.find(edge => edge.`object` == node.id)
          edgeWithObject should not equal (None)
        }
      }
    }

    "get edges by subject" in {
      val node = TestData.nodes(0)
      val edges = sut.getEdgesBySubject(node.id)
      edges should not be empty
      for (edge <- edges) {
        edge.subject should equal(node.id)
      }
    }

    "get matching nodes by label" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = expected.label)
      actual should not be empty
      actual(0) should equal(expected)
    }

    "get count of matching nodes by label" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodesCount(text = expected.label)
      actual should be >= 1
    }

    "get matching nodes by datasource" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"datasource:${expected.datasource}")
      actual should not be empty
      actual(0).datasource should equal(expected.datasource)
    }

    "not return matching nodes for a non-extant datasource" in {
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"datasource:nonextant")
      actual.size should be(0)
    }

    "get matching nodes by datasource and label" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"""datasource:${expected.datasource} label:"${expected.label}"""")
      actual should not be empty
      actual(0) should equal(expected)
    }

    "get matching nodes by id" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"""id:"${expected.id}"""")
      actual.size should be(1)
      actual(0) should equal(expected)
    }

    "get node by id" in {
      val expected = TestData.nodes(0)
      val actual = sut.getNodeById(expected.id)
      actual should equal(Some(expected))
    }

    "get total edges count" in {
      val expected = TestData.edges.size
      val actual = sut.getTotalEdgesCount
      actual should equal(expected)
    }

    "get total nodes count" in {
      val expected = TestData.nodes.size
      val actual = sut.getTotalNodesCount
      actual should equal(expected)
    }
  }
}
