package stores

import java.io.InputStreamReader

import org.scalatest.{Matchers, WordSpec}

class CskgEdgesCsvReaderSpec extends WordSpec with Matchers {
  "CSKG edges CSV reader" can {
    val sut = new CskgEdgesCsvReader()

    "read the test data" in {
      val reader = new InputStreamReader(getClass.getResourceAsStream("/test_data/edges.csv"))
      try {
        val edges = sut.read(reader).toList
        edges.size should be > 0
        for (edge <- edges) {
          edge.subject should not be empty
          edge.`object` should not be empty
          edge.datasource should not be empty
        }
      } finally {
        reader.close()
      }
    }
  }
}
