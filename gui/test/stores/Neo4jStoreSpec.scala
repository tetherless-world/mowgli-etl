package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, Matchers, WordSpec}
import org.slf4j.LoggerFactory

class Neo4jStoreSpec extends WordSpec with StoreBehaviors with BeforeAndAfterAll {
  val logger = LoggerFactory.getLogger(getClass)
  val sut = new Neo4jStore(new Neo4jStoreConfiguration(password = "nC1aB4mji623s2Zs", uri = "bolt://neo4j:7687", user = "neo4j"))

  override def beforeAll(): Unit = {
    try {
      sut.bootstrap()
    } catch {
      case e: ClientException => logger.warn("error bootstrapping neo4j: {}", e.getMessage);
    }
    sut.clear()
    sut.putNodes(TestData.nodes)
    sut.putEdges(TestData.edges)
  }

  "The neo4j store" can {
    behave like store(sut)

    "get matching nodes by datasource" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"datasource:${expected.datasource}")
      actual should not be empty
      actual(0) should equal(expected)
    }

    "not return matching nodes for a non-extant datasource" in {
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"datasource:nonextant")
      actual.size should be(0)
    }

    "get matching nodes by datasource and label" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"datasource:${expected.datasource} label:'${expected.label}'")
      actual should not be empty
      actual(0) should equal(expected)
    }

    "get matching nodes by id" in {
      val expected = TestData.nodes(0)
      val actual = sut.getMatchingNodes(limit = 10, offset = 0, text = s"id:'${expected.id}'")
      actual.size should be(1)
      actual(0) should equal(expected)
    }
  }
}
