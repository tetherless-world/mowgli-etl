# Common Sense Knowledge Graph (CSKG) Graphical User Interface (GUI)

The CSKG GUI is a standard three-tier web application:
- Database: neo4j
- Middleware: Play framework web application in Scala
- Front end: TypeScript+React

# Running

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/)

## Starting the application

In the current directory:

    docker-compose up

## Bootstrapping the database

After starting the application, run

    script/bootstrap-neo4j

## Loading the database

After starting the application, copy a CSKG `nodes.csv` and `edges.csv` into `data/neo4j/import`, then run

    script/load-neo4j

## Clearing the database

After starting the application, run

    script/clear-neo4j
