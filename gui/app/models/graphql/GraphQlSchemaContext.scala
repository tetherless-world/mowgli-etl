package models.graphql

import play.api.mvc.Request
import stores.{Store}

final class GraphQlSchemaContext(request: Request[_], val store: Store)
