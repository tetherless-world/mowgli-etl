package stores

import scala.util.control.NonFatal

// https://medium.com/@dkomanov/scala-try-with-resources-735baad0fd7d
trait WithResource {
  protected def withResource[T <: AutoCloseable, V](r: => T)(f: T => V): V = {
    val resource: T = r
    require(resource != null, "resource is null")
    var exception: Throwable = null
    try {
      f(resource)
    } catch {
      case NonFatal(e) =>
        exception = e
        throw e
    } finally {
      if (exception != null) {
        try {
          resource.close()
        } catch {
          case NonFatal(suppressed) =>
            exception.addSuppressed(suppressed)
        }
      } else {
        resource.close()
      }
    }
  }
}
