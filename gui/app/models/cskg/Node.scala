package models.cskg

final case class Node(
                       datasource: String,
                       id: String,
                       label: String,
                       aliases: Option[List[String]] = None,
                       other: Option[String] = None,
                       pos: Option[String] = None,
                     )
