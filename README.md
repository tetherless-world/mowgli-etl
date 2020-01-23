# mowgli

DARPA Machine Common Sense (MCS) Multi-modal Open World Grounded Learning and Inference (MOWGLI) sub-project 

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

On Unix:

    pip3 install -r requirements.txt
    
On Windows:

    pip install -r requirements.txt
    
# Running tests

Activate the virtual environment as above, then run:

    pytest
