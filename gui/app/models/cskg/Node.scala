package models.cskg

final case class Node(
                       aliases: Option[List[String]], // No default values so the compiler can check missing fields on construction
                       datasource: String,
                       id: String,
                       label: String,
                       other: Option[String],
                       pos: Option[String],
                     )
