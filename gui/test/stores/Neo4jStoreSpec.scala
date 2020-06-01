package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, Matchers, WordSpec}
import org.slf4j.LoggerFactory

class Neo4jStoreSpec extends StoreSpec with BeforeAndAfterAll {
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
    "get edges by object" in {
      getEdgesByObject()
    }

    "get edges by subject" in {
      getEdgesBySubject()
    }

    "get matching nodes" in {
      getMatchingNodes()
    }

    "get matching nodes count" in {
      getMatchingNodesCount()
    }

    "get total nodes count" in {
      getTotalNodesCount()
    }

    "get total edges count" in {
      getTotalEdgesCount()
    }

    "get a node by ID" in {
      getNodeById()
    }
  }
}
