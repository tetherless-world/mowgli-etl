package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, WordSpec}

class MemStoreSpec extends WordSpec with StoreBehaviors {
  behave like store(new TestStore)
}
