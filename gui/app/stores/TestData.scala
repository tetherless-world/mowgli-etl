package stores

import models.cskg.{Edge, Node}

import scala.util.Random

object TestData {
  private val random = new Random()

  val nodes: List[Node] = (0 to 1000).map(i => Node(datasource="test", id=s"node${i}", label=s"Node ${i}", pos=Some("n"))).toList

  val edges: List[Edge] = (0 to 10000).map(_ => {
    var edge: Edge = null
    while (edge == null) {
      val subjectNode = nodes(random.nextInt(nodes.length))
      val objectNode = nodes(random.nextInt(nodes.length))
      if (subjectNode.id != objectNode.id) {
        edge = Edge(datasource = "test", `object` = objectNode.id, predicate = "/r/RelatedTo", subject = subjectNode.id)
      }
    }
    edge
  }).toList
}
