package stores

import java.io.InputStreamReader

import models.cskg.{Edge, Node}

final class TestStore extends MemStore(TestData.edges, TestData.nodes) {
}
