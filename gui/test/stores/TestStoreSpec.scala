package stores

import java.io.InputStreamReader

import org.scalatest.{Matchers, WordSpec}

class TestStoreSpec extends WordSpec with Matchers {
  "Test store" can {
    "instantiate with data" in {
      val store = new TestStore()
      store.edges should not be empty
      store.nodes should not be empty
    }
  }
}
