# mowgli

DARPA Machine Common Sense (MCS) Multi-modal Open World Grounded Learning and Inference (MOWGLI) sub-project 

This repository contains code to:
* extract, transform, and load (ETL) data into the Common Sense Knowledge Graph (CSKG)

# One-time setup

## Create the Python virtual environment

From the current directory:

    python3 -m venv venv
    
## Activate the virtual environment 

On Unix:

    source venv/bin/activate
    
On Windows

    venv\Scripts\activate
    
## Install the dependencies

    pip install -r requirements.txt
    
### Optional: install LevelDB

The framework uses LevelDB for whole-graph operations such as duplicate checking.

OS X:

    brew install leveldb
    CFLAGS=-I$(brew --prefix)/include LDFLAGS=-L$(brew --prefix)/lib pip install plyvel

Linux:

    pip install plyvel
    
### Optional: install bsddb3

The RDF loader can use the rdflib "Sleepycat" store if the `bsddb3` module is present.    
    
Linux:

    pip install bsddb3
    
# Running tests

Activate the virtual environment as above, then run:

    pytest

# Executing an ETL pipeline

Activate the virtual environment as above, then run:

    python3 -m mowgli.cli etl rpi_combined
    
to run all of the available pipelines as well as combine their output.

## `data` directory

The extract, transform, and load stages of the pipelines write data to the `data` directory. (The path to this directory can be changed on the command line). The structure of the `data` directory is `data/<pipeline id>/<stage>`. For example, `data/swow/loaded` for the final products of the `swow` pipeline.

The `rpi_combined` pipeline "loads" the outputs of the other pipelines into its `data/rpi_combined/loaded` directory in the CSKG CSV format.

# Augmenting a CSKG release

Activate the virtual environment as above, then run:

    python3 -m mowgli.cli etl rpi_combined

Download the latest CSKG release .zip file (e.g., `cskg_v004.zip`) into `data/cskg_release/extracted`. You can also pass an existing path to the command below as `--cskg-release-zip-file-path`.

Run

    python3 -m mowgli.cli augment-cskg-release

This produces an augmented .zip file in the same directory as the CSKG release .zip.
