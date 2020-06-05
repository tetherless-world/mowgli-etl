package stores

import java.io.InputStreamReader

import org.scalatest.{Matchers, WordSpec}

class CskgNodesCsvReaderSpec extends WordSpec with Matchers {
  "CSKG nodes CSV reader" can {
    val sut = new CskgNodesCsvReader()

    "read the test data" in {
      val inputStream = getClass.getResourceAsStream("/test_data/nodes.csv.bz2")
      try {
        val nodes = sut.readCompressed(inputStream).toList
        nodes.size should be > 0
        for (node <- nodes) {
          node.id should not be empty
          node.label should not be empty
          node.datasource should not be empty
        }
      } finally {
        inputStream.close()
      }
    }
  }
}
