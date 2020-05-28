package stores

import com.google.inject.AbstractModule
import org.slf4j.LoggerFactory

final class StoresModule extends AbstractModule {
  private val logger = LoggerFactory.getLogger(classOf[StoresModule])

  override def configure(): Unit = {
    val storeClass =
      if (System.getProperty("testIntegration") != null) {
        logger.info("using test store from local data")
        classOf[TestStore]
      } else {
        logger.info("using neo4j store")
        classOf[Neo4jStore]
      }
    bind(classOf[Store]).to(storeClass)
  }
}
