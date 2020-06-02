package stores

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, Matchers, WordSpec}
import org.slf4j.LoggerFactory

class Neo4jStoreSpec extends WordSpec with StoreBehaviors with BeforeAndAfterAll {
  val logger = LoggerFactory.getLogger(getClass)
  val sut = new Neo4jStore(new Neo4jStoreConfiguration(password = "nC1aB4mji623s2Zs", uri = "bolt://neo4j:7687", user = "neo4j"))

  override def beforeAll(): Unit = {
    if (System.getenv("CI") == null) {
      return
    }
    try {
      sut.bootstrap()
    } catch {
      case e: ClientException => logger.warn("error bootstrapping neo4j: {}", e.getMessage);
    }
    sut.clear()
    sut.putNodes(TestData.nodes)
    sut.putEdges(TestData.edges)
  }

  if (System.getenv("CI") != null) {
    "The neo4j store" can {
        behave like store(sut)
      }
  }
}
