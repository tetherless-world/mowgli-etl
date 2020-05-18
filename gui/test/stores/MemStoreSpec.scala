package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.BeforeAndAfterAll

class MemStoreSpec extends StoreSpec with BeforeAndAfterAll {
  val sut = new TestStore

  "The mem store" can {
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
