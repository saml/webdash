name := "webdash"

organization := "web-scale"

version := "0.0.0"

scalaVersion := "2.11.4"

jetty()

libraryDependencies ++= Seq(
  "javax.servlet" % "javax.servlet-api" % "3.1.0" % "provided",
  "org.scala-lang.modules" %% "scala-xml" % "1.0.2"
)


