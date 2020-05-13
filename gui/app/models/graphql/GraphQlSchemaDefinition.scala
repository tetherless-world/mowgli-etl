package models.graphql

import io.github.tetherlessworld.twxplore.lib.base.models.graphql.BaseGraphQlSchemaDefinition
import sangria.schema.{ObjectType, Schema, fields}

object GraphQlSchemaDefinition extends BaseGraphQlSchemaDefinition {
  // Query types
  val RootQueryType = ObjectType("RootQuery",  fields[GraphQlSchemaContext, Unit](
  ))

  // Schema
  val schema = Schema(
    RootQueryType
  )
}
