import sbt.Resolver


//resolvers in ThisBuild += Resolver.mavenLocal
resolvers in ThisBuild += Resolver.sonatypeRepo("snapshots")

lazy val guiApp = (project in file("gui"))
  .enablePlugins(PlayScala)
  .settings(
    libraryDependencies ++= Seq(
      "com.github.tototoshi" %% "scala-csv" % "1.3.6",
      "io.github.tetherless-world" %% "twxplore-base" % "1.0.0-SNAPSHOT",
      "org.scalatestplus.play" %% "scalatestplus-play" % "4.0.3" % Test
    ),
    maintainer := "gordom6@rpi.edu",
    name := "mowgli-gui-app",
    scalaVersion := "2.12.10",
    version := "1.0.0-SNAPSHOT"
  )

