package stores

import javax.inject.Inject
import javax.inject.Singleton
import play.api.Configuration

@Singleton
final class Neo4jStoreConfiguration(val password: String, val uri: String, val user: String) {
  @Inject
  def this(configuration: Configuration) =
    this(configuration.get[String]("neo4j.password"), configuration.get[String]("neo4j.uri"), configuration.get[String]("neo4j.user"))
}
