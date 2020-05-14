package stores

import java.io.Reader
import java.nio.file.Path

import com.github.tototoshi.csv.{CSVFormat, CSVReader, TSVFormat}

abstract class CskgCsvReader[T] {
  implicit val csvFormat: CSVFormat = new TSVFormat {}

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
