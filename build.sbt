import sbt.Resolver


//resolvers in ThisBuild += Resolver.mavenLocal
resolvers in ThisBuild += Resolver.sonatypeRepo("snapshots")

lazy val guiApp = (project in file("gui"))
  .enablePlugins(PlayScala)
  .settings(
    libraryDependencies ++= Seq(
      "io.github.tetherless-world" %% "twxplore-base" % "1.0.0-SNAPSHOT"
    ),
    maintainer := "gordom6@rpi.edu",
    name := "mowgli-gui-app",
    scalaVersion := "2.12.10",
    version := "1.0.0-SNAPSHOT"
  )

