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
    
# Running tests

Activate the virtual environment as above, then run:

    pytest

# Executing an ETL pipeline

Activate the virtual environment as above, then run:

    python3 -m mowgli.cli --pipeline-module combined
    
to run all of the available pipelines as well as combine their output.

## `data` directory

The extract, transform, and load stages of the pipelines write data to the `data` directory. (The path to this directory can be changed on the command line). The structure of the `data` directory is `data/<pipeline id>/<stage>`. For example, `data/swow/loaded` for the final products of the `swow` pipeline.

The `combined` pipeline "loads" the outputs of the other pipelines into its `data/combined/loaded` directory in the CSKG CSV format.
