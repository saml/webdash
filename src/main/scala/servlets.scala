package servlets

import scala.xml.PrettyPrinter
import javax.servlet.http.HttpServlet
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse

class MyServlet extends HttpServlet {

  override def doGet(request: HttpServletRequest, response: HttpServletResponse) {

    response.setContentType("text/html")
    response.setCharacterEncoding("UTF-8")

    val responseBody =
      <html>
        <body>
          <h1>Hello, world!</h1>
        </body>
      </html>

    val printer = new PrettyPrinter(80, 2)

    val writer = response.getWriter
    val content = printer.formatNodes(responseBody)
    writer.write("<!doctype html>\n")
    writer.write(content)

  }

}

// vim: set ts=4 sw=4 et:
