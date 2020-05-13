package models.cskg

final case class Node(
                       datasource: String,
                       id: String,
                       label: String,
                       aliases: List[String] = List(),
                       other: Option[String] = None,
                       pos: Option[String] = None,
                     )
