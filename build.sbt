import sbt.Resolver


//resolvers in ThisBuild += Resolver.mavenLocal
resolvers in ThisBuild += Resolver.sonatypeRepo("snapshots")

lazy val `gui` = (project in file("gui"))
  .enablePlugins(PlayScala)
  .settings(
    libraryDependencies ++= Seq(
      "io.github.tetherless-world" %% "twxplore-base" % "1.0.0-SNAPSHOT"
    ),
    name := "mowgli-gui",
    scalaVersion := "2.12.10",
    version := "1.0.0-SNAPSHOT"
  )

