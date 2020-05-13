package stores

import com.google.inject.AbstractModule
import org.paradicms.lib.generic.stores.UserStore

final class StoresModule extends AbstractModule {
  override def configure(): Unit = {
    val storeClass =
      if (System.getProperty("testIntegration") != null)
        classOf[TestStore]
      else
        classOf[PlaceholderStore]
    bind(classOf[Store]).to(storeClass)
  }
}
