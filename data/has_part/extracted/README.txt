This directory contains the following files:

1. hasPartKB.jsonl : Our hasPartKB with ~50k first-order hasPart extractions, one extraction object per line. Each object represents an aggregated extraction created by grouping together extractions with the same normalized arguments. The top-level score is the average of the individual extraction scores from which it was obtained. The arguments contain links to Wikipedia and WordNet if successfully linked, under 'metadata'. The raw extractions that were grouped to create the aggregated extraction are retained with detailed argument information and provenance (sentence and argument character spans) under 'supporting tuples'. E.g.-
   {   "arg1": 
         { "normalized": "insect",
           "metadata": {"wikipedia_primary_page": "Insect", "synset": "wn.insect.n.01"}
         },
       "arg2": 
         { "normalized": "respiratory system",
           "metadata": {"wikipedia_primary_page": "Respiratory system", "synset": "wn.respiratory_system.n.01"}
         },
       "average_score": 0.9990711510181427,
       "supporting_tuples": [
         { "tuple":
             { "arg1":
                 { "raw": "insects",
                   "normalized": "insect",
                   "concept": "insect",
                   "metadata": {"wikipedia_primary_page": "Insect", "synset": "wn.insect.n.01"}
                 },
               "arg2":
                 { "raw": "respiratory system",
                   "normalized": "respiratory system",
                   "concept": "respiratory system",
                   "metadata": {"wikipedia_primary_page": "Respiratory system", "synset": "wn.respiratory_system.n.01"}
                 }
             },
             "score": 0.999285876750946,
             "matches": [["insects do have a respiratory system.", [[[18, 36], [0, 7]]]]]},
         { "tuple":
             { "arg1":
                 { "raw": "most insects",
                   "normalized": "insect",
                   "concept": "insect",
                   "metadata": {"wikipedia_primary_page": "Insect", "quantifiers": ["most"], "synset": "wn.insect.n.01"}
                 },
               "arg2":
                 {"raw": "respiratory system", "normalized": "respiratory system", "concept": "respiratory system", "metadata": {"wikipedia_primary_page": "Respiratory system", "synset": "wn.respiratory_system.n.01"}
                 }
             },
             "score": 0.9988564252853394,
             "matches": [["most insects have a respiratory system akin to ventilation in a building.", [[[20, 38], [0, 12]]]]]
         }
       ]
    }

2. hasPartKB.tsv : The above KB file in TSV format for convenience.

3. hasPartKBTaxonomyDepth5.txt : A pretty-printed text file containing the taxonomy created by building from hasPartKB transitively to a depth of 5 and a maximum fanout of 10 for the last level. 

4. hasPartKBTaxonomyDepth4.txt : Similar to above, but restricted to depth 4.

5. hasPartKBTaxonomyDepth3.txt : Similar to above, but restricted to depth 3.