package models.cskg

final case class Edge(
                      datasource: String,
                      `object`: String,
                      other: Option[String], // No default values so the compiler can check missing fields on construction
                      predicate: String,
                      subject: String,
                      weight: Option[Double]
                     )
