package models.cskg

final case class Edge(
                      datasource: String,
                      `object`: String,
                      predicate: String,
                      subject: String,
                      other: Option[String] = None,
                      weight: Option[Float] = None
                     )
