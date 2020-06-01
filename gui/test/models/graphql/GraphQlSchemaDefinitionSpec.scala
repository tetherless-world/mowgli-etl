package models.graphql

import org.scalatestplus.play.PlaySpec
import play.api.libs.json.{JsObject, Json}
import play.api.test.FakeRequest
import sangria.ast.Document
import sangria.execution.Executor
import sangria.macros._
import sangria.marshalling.playJson._
import stores.{TestData, TestStore}

import scala.concurrent.Await
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._

class GraphQlSchemaDefinitionSpec extends PlaySpec {
  "GraphQL schema" must {
    "get a node by id" in {
      val node = TestData.nodes(0)
      val query =
        graphql"""
         query NodeByIdQuery($$id: String!) {
           nodeById(id: $$id) {
            label
           }
         }
       """

      executeQuery(query, vars = Json.obj("id" -> node.id)) must be(Json.parse(
        s"""
           |{"data":{"nodeById":{"label":"${node.label}"}}}
           |""".stripMargin))
    }

    "get edges the node is a subject of" in {
      val node = TestData.nodes(0)
      val query =
        graphql"""
         query EdgesQuery($$nodeId: String!) {
           nodeById(id: $$nodeId) {
             subjectOfEdges {
               predicate
               object
               objectNode {
                 label
               }
             }
           }
         }
       """

      val result = Json.stringify(executeQuery(query, vars = Json.obj("nodeId" -> node.id)))
      for (edge <- TestData.edges.filter(edge => edge.subject == node.id)) {
        result must include(s"""{"predicate":"${edge.predicate}","object":"${edge.`object`}"""")
      }
    }

    "get edges the node is an object of" in {
      val node = TestData.nodes(0)
      val query =
        graphql"""
         query EdgesQuery($$nodeId: String!) {
           nodeById(id: $$nodeId) {
             objectOfEdges {
               predicate
               subject
             }
           }
         }
       """

      executeQuery(query, vars = Json.obj("nodeId" -> node.id)) must be(Json.parse(
        s"""
           |{"data":{"nodeById":{"objectOfEdges":[]}}}
           |""".stripMargin))
    }

    "search nodes" in {
      val node = TestData.nodes(0)
      val query =
        graphql"""
         query MatchingNodesQuery($$text: String!) {
           matchingNodes(text: $$text, limit: 1, offset: 0) {
            id
           }
           matchingNodesCount(text: $$text)
         }
       """

      executeQuery(query, vars = Json.obj("text" -> s"""label:"${node.label}"""")) must be(Json.parse(
        s"""
           |{"data":{"matchingNodes":[{"id":"${node.id}"}],"matchingNodesCount":1}}
           |""".stripMargin))
    }

    "get total node and edge count" in {
      val nodeCount = TestData.nodes.size
      val edgeCount = TestData.edges.size
      val query =
        graphql"""
          query TotalCountsQuery {
            totalNodesCount
            totalEdgesCount
          }
        """

      executeQuery(query) must be(Json.parse(
        s"""{"data":{"totalNodesCount":${nodeCount},"totalEdgesCount":${edgeCount}}}"""
      ))
    }
  }

  def executeQuery(query: Document, vars: JsObject = Json.obj()) = {
    val futureResult = Executor.execute(GraphQlSchemaDefinition.schema, query,
      variables = vars,
      userContext = new GraphQlSchemaContext(FakeRequest(), new TestStore())
    )
    Await.result(futureResult, 10.seconds)
  }
}
