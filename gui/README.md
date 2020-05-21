# Common Sense Knowledge Graph (CSKG) Graphical User Interface (GUI)

The CSKG GUI is a standard three-tier web application:
- Database: neo4j
- Middleware: Play framework web application in Scala
- Front end: TypeScript+React

# Running the application

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

After starting the application, copy a CSKG `nodes.csv` and `edges.csv` into `data/neo4j/import`. There is a small test data set in `conf/test_data`.
 
Then run:

    script/load-neo4j

## Clearing the database

After starting the application, run

    script/clear-neo4j
    
## Viewing the application

After starting the application and loading the data, open your browser to [http://localhost:8080](http://localhost:8080).

# Developing

## Database

You can run the neo4j database locally with Docker:

    docker-compose up neo4j
    
Then following the steps above to bootstrap (one time) and load the database.
    
## Middleware

### Prerequisites

* [Java Development Kit (JDK)](https://adoptopenjdk.net/)
* [sbt](https://www.scala-sbt.org/)

### Running

The Play app can be run in the usual way. From the root of the repository:

    sbt "project guiApp" run
    
or in the sbt shell. The app listens to port 9000.

### Front end

The front end is built with webpack. To start the webpack-dev-server, run

    cd gui/gui
    npm start
    
from the root of the repository. The webpack-dev-server listens to port 9001 and proxies API requests to port 9000.

You can then open the app on

    http://localhost:9001
