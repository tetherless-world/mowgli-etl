package models.graphql

import io.github.tetherlessworld.twxplore.lib.base.models.graphql.BaseGraphQlSchemaDefinition
import models.cskg.{Edge, Node}
import sangria.schema.{Argument, Field, FloatType, IntType, ListType, ObjectType, OptionType, Schema, StringType, fields}
import sangria.macros.derive._

object GraphQlSchemaDefinition extends BaseGraphQlSchemaDefinition {
  // Object types
  // Can't use deriveObjectType because we need to define node and edge recursively
  // https://github.com/sangria-graphql/sangria/issues/54
  lazy val EdgeType: ObjectType[GraphQlSchemaContext, Edge] = ObjectType("Edge", () => fields[GraphQlSchemaContext, Edge](
    Field("datasource", StringType, resolve = _.value.datasource),
    Field("object", StringType, resolve = _.value.`object`),
    Field("objectNode", OptionType(NodeType), resolve = ctx => ctx.ctx.store.getNodeById(ctx.value.`object`)),
    Field("other", OptionType(StringType), resolve = _.value.other),
    Field("predicate", OptionType(StringType), resolve = _.value.predicate),
    Field("subject", StringType, resolve = _.value.subject),
    Field("subjectNode", OptionType(NodeType), resolve = ctx => ctx.ctx.store.getNodeById(ctx.value.subject)),
    Field("weight", OptionType(FloatType), resolve = _.value.weight)
  ))
  lazy val NodeType: ObjectType[GraphQlSchemaContext, Node] = ObjectType("Node", () => fields[GraphQlSchemaContext, Node](
    Field("aliases", OptionType(ListType(StringType)), resolve = _.value.aliases),
    Field("datasource", StringType, resolve = _.value.datasource),
    Field("id", StringType, resolve = _.value.id),
    Field("label", OptionType(StringType), resolve = _.value.label),
    Field("objectOfEdges", ListType(EdgeType), resolve = ctx => ctx.ctx.store.getEdgesByObject(ctx.value.id)),
    Field("other", OptionType(StringType), resolve = _.value.other),
    Field("pos", OptionType(StringType), resolve = _.value.pos),
    Field("subjectOfEdges", ListType(EdgeType), resolve = ctx => ctx.ctx.store.getEdgesBySubject(ctx.value.id))
  ))

  val IdArgument = Argument("id", StringType)

  // Query types
  val RootQueryType = ObjectType("RootQuery",  fields[GraphQlSchemaContext, Unit](
    Field("matchingNodes", ListType(NodeType), arguments = LimitArgument :: OffsetArgument :: TextArgument :: Nil, resolve = ctx => ctx.ctx.store.getMatchingNodes(limit = ctx.args.arg(LimitArgument), offset = ctx.args.arg(OffsetArgument), text = ctx.args.arg(TextArgument))),
    Field("matchingNodesCount", IntType, arguments = TextArgument :: Nil, resolve = ctx => ctx.ctx.store.getMatchingNodesCount(text = ctx.args.arg(TextArgument))),
    Field("nodeById", OptionType(NodeType), arguments = IdArgument :: Nil, resolve = ctx => ctx.ctx.store.getNodeById(ctx.args.arg(IdArgument))),
    Field("randomNode", NodeType, resolve = ctx => ctx.ctx.store.getRandomNode),
    Field("totalEdgesCount", IntType, resolve = ctx => ctx.ctx.store.getTotalEdgesCount),
    Field("totalNodesCount", IntType, resolve = ctx => ctx.ctx.store.getTotalNodesCount)
  ))

  // Schema
  val schema = Schema(
    RootQueryType
  )
}
