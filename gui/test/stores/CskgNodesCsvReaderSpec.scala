package stores

import java.io.InputStreamReader

import org.scalatest.{Matchers, WordSpec}

class CskgNodesCsvReaderSpec extends WordSpec with Matchers {
  "CSKG nodes CSV reader" can {
    val sut = new CskgNodesCsvReader()

    "read the test data" in {
      val reader = new InputStreamReader(getClass.getResourceAsStream("/test_data/nodes.csv"))
      try {
        val nodes = sut.read(reader).toList
        nodes.size should be > 0
        for (node <- nodes) {
          node.id should not be empty
          node.label should not be empty
          node.datasource should not be empty
        }
      } finally {
        reader.close()
      }
    }
  }
}
