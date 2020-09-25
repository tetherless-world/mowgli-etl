# MOWGLI Extract-Transform-Load (ETL) project

This project consists of a series of [extract-transform-load (ETL)](https://en.wikipedia.org/wiki/Extract,_transform,_load) pipelines for adding common sense knowledge triples to the MOWGLI Common Sense Knowledge Graph (CSKG).

The CSKG is used by downstream applications such as question answering systems and knowledge graph browsers. The graph consists of nodes and edges serialized in [KGTK edge format](https://docs.google.com/document/d/1fbbqgyX0N2EdxLam6hatfke1R-nZWkoN6M1oB_f4aQo/edit#heading=h.yz6ztsi7h1xa), which is a specialization of the general [KGTK format](https://kgtk.readthedocs.io/en/latest/specification/).

[ConceptNet](http://conceptnet.io/) serves as the core of the CSKG, and other sources such as Wikidata are linked to it. The majority of the predicates/relations in the CSKG are [reused from ConceptNet](https://github.com/commonsense/conceptnet5/wiki/Relations).

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

    python3 -m mowgli_etl.cli etl rpi_combined
    
to run all of the available pipelines as well as combine their output.

## `data` directory

The extract, transform, and load stages of the pipelines write data to the `data` directory. (The path to this directory can be changed on the command line). The structure of the `data` directory is `data/<pipeline id>/<stage>`. For example, `data/swow/loaded` for the final products of the `swow` pipeline.

The `rpi_combined` pipeline "loads" the outputs of the other pipelines into its `data/rpi_combined/loaded` directory in the CSKG CSV format.

# Augmenting a CSKG release

Activate the virtual environment as above, then run:

    python3 -m mowgli_etl.cli etl rpi_combined

Download the latest CSKG release .zip file (e.g., `cskg_v004.zip`) into `data/cskg_release/extracted`. You can also pass an existing path to the command below as `--cskg-release-zip-file-path`.

Run

    python3 -m mowgli_etl.cli augment-cskg-release

This produces an augmented .zip file in the same directory as the CSKG release .zip.

# Development

## Overview

The mowgli-etl code base consists of:
* a minimal bespoke framework for implementing ETL pipelines
* pipeline implementations for different data sources, such as the `swow` pipeline for the [Small World of Words](https://smallworldofwords.org/en/project) word association lexicon

### Pipelines

A pipeline consists of:
* an extractor, inheriting from the `_Extractor` abstract base class
* a transformer, inheriting from the `_Transformer` abstract base class
* an optional loader (`_Loader` subclass), which is usually not explicitly specified by pipelines; a default is provided instead
* a `_Pipeline` subclass that ties everything together

#### Pipeline execution

Running a pipeline with a command like

    python3 -m mowgli_etl.cli etl swow

initiates the following process, where `swow` is the _pipeline id_.

1. Instantiate the pipeline by
    1. finding a module named exactly `mowgli_etl.pipeline.swow.swow_pipeline` (or adapted from another pipeline id)
    1. finding a subclass of _Pipeline declared in that module
    1. instantiating that subclass with a few arguments from the command line as constructor parameters
1. Call the `extract` method of the `extractor` on the pipeline. See the docstring of `_Extractor.extract` for information on the contract of `extract`.
1. Call the `transform` method of the `transformer` on the pipeline, passing in a `**kwds` dictionary returned by `extract`. See the docstring of `_Transformer.transform` for more information.
1. The `transform` method is a generator for a sequence of models, typically `KgEdge`s and `KgNode`s to add to the CSKG. This generator is passed to the loader, which iterates over it, loading data as it goes. For example, the default KGTK loader buffers nodes and appends edge rows to an output KGTK file. This loading process does not usually need to be handled by the pipeline implementations, most of which rely on the default loader.

## Python libraries, patterns, and idioms in `mowgli-etl`

* [Generators](https://wiki.python.org/moin/Generators)
* Type hints and the [`typing` module](https://docs.python.org/3/library/typing.html), especially `NamedTuple`
* [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
* Keyword-only arguments (`def f(*, x, y)`), and `**kwds` keyword variadic arguments
* Abstract base classes, abstract methods, and the [`abc` module](https://docs.python.org/3/library/abc.html)
* The [pytest framework](https://docs.pytest.org/en/stable/) for unit testing
* The [`pathlib` module](https://docs.python.org/3/library/pathlib.html)
* [Class methods](https://docs.python.org/3/library/functions.html#classmethod)

## Coding conventions

We follow [PEP8](https://www.python.org/dev/peps/pep-0008/) and the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), preferring the former where the two are inconsistent.

We encourage using an IDE such as PyCharm. Please format your code with [Black](https://black.readthedocs.io/en/stable/) before committing it. The formatter can be integrated into most editors, to format on save.

Most code should be part of a class. There should be one class per file, and the file should be named after the class (`SomeClass` as `some_class.py`).

## Implementing a new pipeline

The `swow` pipeline is the best model for new pipelines.

### Implementing a new extractor

Extractors typically work in one of two ways:
1. Using pre-downloaded data that is committed to the per-pipeline `data` subdirectory. This is the best approach for smaller data sets that change infrequently.
1. Downloading source data when the `extract` method is called. The data can be cached in the per-pipeline `data` subdirectory and reused if `force` is not specified. Cached data should be `.gitignore`d. Use an implementation of the `EtlHttpClient` rather than using `urllib`, `requests`, or another HTTP client directly. This makes it easier to mock the HTTP client in unit tests.

The `extract` method receives a `storage` parameter that points to a `PipelineStorage` instance, which has the path to appropriate subdirectory of `data`. Extractors should use this path (`storage.extracted_data_dir_path`) rather than trying to locate `data` directly, since the path to `data` can be changed on the command line.

Once the data is available, the extractor must pass it to the transformer by returning a `**kwds` dictionary. This is typically done in one of two ways:
1. Returning `{"path_to_file": Path("the/file/path")}` from `extract`, so that `transform` is `def transform(self, *, path_to_file: Path)`. This is the preferred approach for large files.
1. Reading the file in the extractor and returning `{"file_data": "..."}`, in which case `transform` is `def transform(self, *, file_data: str)` or similar. This is acceptable for small data.

### Implementing a new transformer

Given extracted data in one of the forms listed above, the transformer's task is to:
1. parse the data in its source format
1. create a sequence of `KgEdge` and `KgNode` models that capture the data
1. yield those models

Transformers can be implemented in a variety of ways, as long as they conform to the `_Transformer` abstract base class. For example, in many implementations the top-level `transform` methods delegates to multiple private helper methods or helper classes. It is easier to test the code if the logic of the transformer is broken up into relatively small methods that can be tested individually, rather than one large `transform` method with many branches.

Note that `KgEdge` and `KgNode` have legacy factory classmethods (`.legacy` in both cases) corresponding to an older data model. These should not be used in new code. New code should instantiate the models directly or use one of the other factory classmethods as a convenience.

## Testing a pipeline

The `swow` pipeline tests in `tests/mowgli_etl_test/pipeline/swow` can be used as a model for how to test a pipeline. Familiarity with the `pytest` framework is necessary.

## Source control workflow

We use the [GitHub flow](https://guides.github.com/introduction/flow/) with feature branches on this code. Branches should be named after (e.g., `GH-###`) or otherwise linked to an issue in the issue tracker. Please tag a staff person for code reviews, and re-tag when you have addressed the staff person's comments in the code and rebutted the comments in the PR. See the [Google Code Review Developer Guide](https://google.github.io/eng-practices/review/) for more information on code reviews.

## Continuous Integration

We use [CircleCI](https://circleci.com/) for [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration). CircleCI runs the tests in `tests/` on every push to `origin`. Merging a feature branch is contingent on having adequate tests and all tests passing. We encourage [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development).
