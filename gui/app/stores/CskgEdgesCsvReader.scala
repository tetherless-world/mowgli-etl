package stores

import com.github.tototoshi.csv._
import models.cskg
import models.cskg.Edge

final class CskgEdgesCsvReader extends CskgCsvReader[Edge] {
  def read(csvReader: CSVReader): Stream[Edge] =
    csvReader.toStreamWithHeaders.map(row =>
      Edge(
        datasource = row("datasource"),
        `object` = row("object"),
        other = row.getNonBlank("other"),
        predicate = row("predicate"),
        subject = row("subject"),
        weight = row.getNonBlank("weight").map(weight => weight.toFloat)
    ))
}
