package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.BeforeAndAfterAll

class MemStoreSpec extends StoreSpec with BeforeAndAfterAll {
  val sut = new TestStore

  "The mem store" can {
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

    "get a node by ID" in {
      getNodeById()
    }

    "get total edges count" in {
      getTotalEdgesCount()
    }

    "get total nodes count" in {
      getTotalNodesCount()
    }
  }
}
