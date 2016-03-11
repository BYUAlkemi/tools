/*
  Usage:
    <executable> /path/to/input/file /path/to/output/file
*/

import scala.io.Source

object CsvFix {
  val lineFixRegex = "Vector2d|<|>|\\s".r

  def main(args: Array[String]): Unit = {
    val inFilePath = args(0)
    val outFilePath = args(1)

    val inStream = Source.fromFile(inFilePath)
    val outWriter = new java.io.FileWriter(outFilePath)
    val outStream = new java.io.BufferedWriter(outWriter)

    fixFile(inStream.getLines, outStream)

    outStream.close()
    inStream.close()
  }

  def fixFile(inStream: Iterator[String], outWriter: java.io.BufferedWriter): Unit = {
    var timestep = 0

    val nonBlankLines = inStream
      .map(line => line.trim)
      .filter(line => !line.isEmpty)

    nonBlankLines
      .take(1)
      .map(fixSchemaLine)
      .foreach { fixedSchemaLine =>
        outWriter.write(s"timestep,$fixedSchemaLine")
        outWriter.newLine
      }

    nonBlankLines
      .map{ line => 
        if ((line(0).isDigit || line(0).isLetter) && line.startsWith("Sim")) {
          timestep += 1
          ""
        } else {
          line
        }
      }
      .filter(line => !line.isEmpty)
      .map(fixLine)
      .foreach { fixedLine => 
        outWriter.write(fixedLine)
        outWriter.newLine
      } 
  }

  def fixSchemaLine(line: String): String = {
    line.replaceAll("Position", "positionX,positionY")
  }

  def fixLine(line: String): String = {
    lineFixRegex.replaceAllIn(line, "")
  }
}
