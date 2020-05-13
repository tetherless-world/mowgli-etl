# Build
FROM hseeberger/scala-sbt:11.0.5_1.3.7_2.12.10 as build
WORKDIR /mowgli
# The root of the repository is the context
COPY /build.sbt .
COPY /gui/app ./gui/app
COPY /gui/conf ./gui/conf
COPY /project ./project
RUN sbt "project guiApp" playUpdateSecret dist

# Deployment
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y default-jre-headless unzip

COPY --from=build /mowgli/gui/target/universal/mowgli-gui-app-1.0.0-SNAPSHOT.zip /
RUN unzip -q mowgli-gui-app-1.0.0-SNAPSHOT.zip && mv /mowgli-gui-app-1.0.0-SNAPSHOT /app && chmod +x /app/bin/mowgli-gui-app

EXPOSE 9000

ENTRYPOINT ["/app/bin/mowgli-gui-app"]
