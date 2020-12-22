# WebDataCommons (WDC) ETL pipeline

## Sub-Parts

- Transformer: Generates spatial relationship predicate CSKG edges
- Product Type Classifier: Generates a sequence of potential generic product types from a corpus entry
  - Heuristic Product Type Classifier: The sequence of potential generic product types are created by the following heuristics:
    1. Take the last noun in the field
    2. Take the first noun sequence in the field
    3. Take the last noun sequence in the field
- Dimension Parser: Generates a potential set of dimensions from a corpus entry
  - Parsimonious Dimension Parser: Uses Parsimonious NLP to find the most likely dimensions from the field, using the heuristic:
    - dim unit x dim unit x dim unit ...
- Bucketer: Generates an average dimension set for the generic product type and dimensions entered and assigns relative size buckets
  - Half Order Size Bucket: Uses half order of magnitude heuristic to find relative bucket size using the formula:
      <img src="https://render.githubusercontent.com/render/math?math=bucket\leq\text{max}(\dfrac{(number\_of\_buckets-1)\text{log}(\frac{volume*10}{max\_volume})}{\text{log}(10)},1)">
  - Naive Size Buckets: Assigns the bucket to the volume (i.e. edges compare direct volumes)
  - Rounded Size Buckets: Assigns the bucket to the integer closest to the volume

### Findings
In general, the available file (offers_corpus_english_v2_1000.jsonl) doesn't have a lot of usable data points. Either the entries aren't in English, they don't have spatial dimensions, or they don't have appropriate spatial dimensions.

The data points also seem to cluster towards smaller objects, as found when 36 out of 46 bucketed products fell in bucket 1, even with over 1000 buckets

As a result, the majority of yielded Edges are "EquivalentTo" predicates

### Notes
A Regex approach for Product Type Classifier was considered, however it ended up being overly convoluted and unreliable, so it was scrapped

Other heuristics were considered for Heuristic Product Type Classifier, but were not implemented as they were not significantly more reliable

Other heuristics were considered for Parsimonious Dimension Parser, but were not implemented due to time constraints

We believe a major sticking point in the pipeline is the Product Type Classifier, as the heuristics used are rudimentary, and often result in overly specific product types

Reliability for the generated generic product types is weighted by the field used (e.g. "title", "description", "special key value table")

Reliability for the generated dimensions is weighted by the field used and the number of dimensions found (only applicable for spatial dimensions, where it's calculated by number_of_dimensions/3)

The Transformer is currently set up with temporary heuristics (SmallerThan, LargerThan, EquivalentTo)
