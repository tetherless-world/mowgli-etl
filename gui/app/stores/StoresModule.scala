package stores

import com.google.inject.AbstractModule

final class StoresModule extends AbstractModule {
  override def configure(): Unit = {
    val storeClass =
      if (System.getProperty("testIntegration") != null)
        classOf[TestStore]
      else
        classOf[Neo4jStore]
    bind(classOf[Store]).to(storeClass)
  }
}
