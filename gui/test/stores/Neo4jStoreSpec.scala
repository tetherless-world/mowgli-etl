package stores

import java.net.InetAddress

import org.neo4j.driver.exceptions.ClientException
import org.scalatest.{BeforeAndAfterAll, Matchers, WordSpec}
import org.slf4j.LoggerFactory

class Neo4jStoreSpec extends WordSpec with StoreBehaviors with BeforeAndAfterAll {
  val logger = LoggerFactory.getLogger(getClass)
  val sut = new Neo4jStore(new Neo4jStoreConfiguration(password = "nC1aB4mji623s2Zs", uri = "bolt://neo4j:7687", user = "neo4j"))
  val neo4jHostAddress = InetAddress.getByName("neo4j").getHostAddress
  val inTestingEnvironment = System.getenv("CI") != null || neo4jHostAddress != "128.113.12.49"

  override def beforeAll(): Unit = {
    if (!inTestingEnvironment) {
      return
    }
    if (!sut.hasConstraints) {
      try {
        sut.bootstrap()
      } catch {
        case e: ClientException => logger.warn("error bootstrapping neo4j: {}", e.getMessage);
      }
    }
    sut.clear()
    sut.putNodes(TestData.nodes)
    sut.putEdges(TestData.edges)
  }

  if (inTestingEnvironment) {
    "The neo4j store" can {
        behave like store(sut)
      }
  }
}
