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
           |{"data":{"nodeById":{"objectOfEdges":[{"predicate":"/r/MadeOf","subject":"gui_test_data:901"},{"predicate":"/r/HasLastSubevent","subject":"gui_test_data:169"},{"predicate":"/r/IsA","subject":"gui_test_data:676"},{"predicate":"/r/MotivatedByGoal","subject":"gui_test_data:68"},{"predicate":"/r/AtLocation","subject":"gui_test_data:984"},{"predicate":"/r/DefinedAs","subject":"gui_test_data:224"},{"predicate":"/r/SimilarTo","subject":"gui_test_data:194"},{"predicate":"/r/HasProperty","subject":"gui_test_data:523"},{"predicate":"/r/DerivedFrom","subject":"gui_test_data:428"},{"predicate":"/r/HasA","subject":"gui_test_data:514"},{"predicate":"/r/Causes","subject":"gui_test_data:42"},{"predicate":"/r/LocatedNear","subject":"gui_test_data:337"},{"predicate":"/r/DerivedFrom","subject":"gui_test_data:952"},{"predicate":"/r/CausesDesire","subject":"gui_test_data:453"},{"predicate":"/r/SymbolOf","subject":"gui_test_data:532"},{"predicate":"/r/HasA","subject":"gui_test_data:788"},{"predicate":"/r/EtymologicallyDerivedFrom","subject":"gui_test_data:949"},{"predicate":"/r/DistinctFrom","subject":"gui_test_data:637"},{"predicate":"/r/HasFirstSubevent","subject":"gui_test_data:689"},{"predicate":"/r/CapableOf","subject":"gui_test_data:340"},{"predicate":"/r/CausesDesire","subject":"gui_test_data:122"},{"predicate":"/r/HasSubevent","subject":"gui_test_data:359"},{"predicate":"/r/Desires","subject":"gui_test_data:123"},{"predicate":"/r/DerivedFrom","subject":"gui_test_data:826"},{"predicate":"/r/ObstructedBy","subject":"gui_test_data:43"},{"predicate":"/r/LocatedNear","subject":"gui_test_data:373"},{"predicate":"/r/HasContext","subject":"gui_test_data:264"},{"predicate":"/r/ObstructedBy","subject":"gui_test_data:21"},{"predicate":"/r/HasContext","subject":"gui_test_data:466"},{"predicate":"/r/HasLastSubevent","subject":"gui_test_data:131"},{"predicate":"/r/HasSubevent","subject":"gui_test_data:682"},{"predicate":"/r/CausesDesire","subject":"gui_test_data:499"},{"predicate":"/r/MadeOf","subject":"gui_test_data:470"},{"predicate":"/r/CreatedBy","subject":"gui_test_data:831"},{"predicate":"/r/CapableOf","subject":"gui_test_data:237"},{"predicate":"/r/PartOf","subject":"gui_test_data:396"},{"predicate":"/r/SimilarTo","subject":"gui_test_data:259"},{"predicate":"/r/LocatedNear","subject":"gui_test_data:729"},{"predicate":"/r/Synonym","subject":"gui_test_data:543"},{"predicate":"/r/ReceivesAction","subject":"gui_test_data:473"},{"predicate":"/r/SimilarTo","subject":"gui_test_data:390"},{"predicate":"/r/SimilarTo","subject":"gui_test_data:107"},{"predicate":"/r/CapableOf","subject":"gui_test_data:872"}]}}}
           |""".stripMargin))
    }

    "get a random node" in {
        val query =
          graphql"""
         query RandomNodeQuery {
           randomNode {
            id
            label
           }
         }
       """

        val results = Json.stringify(executeQuery(query))
        results must include("""{"data":{"randomNode":{"id":"""")
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
