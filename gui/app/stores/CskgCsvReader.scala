package stores

import java.io.Reader
import java.nio.file.Path

import com.github.tototoshi.csv.{CSVFormat, CSVReader, TSVFormat}

abstract class CskgCsvReader[T] {
  private implicit val csvFormat: CSVFormat = new TSVFormat {}

  protected implicit class RowWrapper(row: Map[String, String]) {
    def getNonBlank(key: String) =
      row.get(key).flatMap(value => if (!value.isBlank && value != "::") Some(value) else None)
  }

  def read(filePath: Path): Stream[T] = {
    val csvReader = CSVReader.open(filePath.toFile)
    try {
      read(csvReader)
    } finally {
      csvReader.close()
    }
  }

  def read(reader: Reader): Stream[T] =
    read(CSVReader.open(reader))

  def read(csvReader: CSVReader): Stream[T]
}
