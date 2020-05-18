package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, Matchers, WordSpec}

class Neo4jStoreSpec extends StoreSpec with BeforeAndAfterAll {
  val sut = new Neo4jStore(new Neo4jStoreConfiguration(password = "nC1aB4mji623s2Zs", uri = "bolt://neo4j:7687", user = "neo4j"))

  override def beforeAll(): Unit = {
    try {
      sut.bootstrap()
    } catch {
      case _: ClientException => // Ignore constraint already exists
    }
    sut.clear()
    sut.putNodes(TestData.nodes)
    sut.putEdges(TestData.edges)
  }

  "The neo4j store" can {
    "get edges by subject" in {
      getEdgesBySubject()
    }

    "get a node by ID" in {
      getNodeById()
    }

    "search nodes" in {
      searchNodes()
    }
  }
}
