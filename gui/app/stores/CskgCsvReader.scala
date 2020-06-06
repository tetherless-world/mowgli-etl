package stores

import java.io.{FileInputStream, InputStream, InputStreamReader, Reader, UnsupportedEncodingException}
import java.nio.file.Path

import com.github.tototoshi.csv.CSVReader.open
import com.github.tototoshi.csv.{CSVFormat, CSVReader, TSVFormat}
import org.apache.commons.compress.compressors.CompressorStreamFactory
import org.apache.commons.lang3.StringUtils

abstract class CskgCsvReader[T] {
  private implicit val csvFormat: CSVFormat = new TSVFormat {}

  protected implicit class RowWrapper(row: Map[String, String]) {
    def getNonBlank(key: String) =
      row.get(key).flatMap(value => if (!StringUtils.isBlank(value) && value != "::") Some(value) else None)
  }

  def read(filePath: Path): Stream[T] = {
    val fileInputStream = new FileInputStream(filePath.toFile)
    try {
      if (filePath.getFileName.endsWith(".bz2")) {
        readCompressed(fileInputStream)
      } else {
        read(fileInputStream)
      }
    } finally {
      fileInputStream.close()
    }
  }

  def read(inputStream: InputStream): Stream[T] = {
    read(new InputStreamReader(inputStream, CSVReader.DEFAULT_ENCODING))
  }

  def read(reader: Reader): Stream[T] =
    read(CSVReader.open(reader))

  def read(csvReader: CSVReader): Stream[T]

  def readCompressed(inputStream: InputStream): Stream[T] = {
    val bz2InputStream = new CompressorStreamFactory().createCompressorInputStream(inputStream)
//    try {
      read(bz2InputStream)
//    } finally {
//      bz2InputStream.close()
//    }
  }
}
