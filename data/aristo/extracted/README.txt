
		THE ARISTO TUPLE KB - Version 4 (Mar 2017 Release)
		=====================================================

---------
REFERENCE
---------
If you use this data in your research please refer to the tuple KB by its release name and snapshot date ("Aristo Tuple KB v1.03 - Mar 2017 Release"), and provide an acknowledgement to the Allen Institute for AI (www.allenai.org). A reference for this work is:
 * Dalvi, B., Tandon, N., Clark, P. "Domain-Targeted, High Precision Knowledge Extraction", TACL, 2017 (to appear)

-------
SUMMARY
-------
This package contains a collection of filtered, high precision triples within a target vocabulary. The tuples constitute simple facts about the world along with a rough degree of quantification (most/some). For example:

QStrength	Quantifier	Arg1	Pred	Arg2	Sentence	Score	Inferred?	Multiword?	Canonical?	Domain	Range	Provenance
0.92	most	aardvark	eat	insect	Most aardvarks eat insects.	0.77	n	n	n	animal_n1	insect_n1	830913 
0.83	most	grass seed	need	consistent moisture	Most grass seeds need consistent moisture.	0.79	y	y	n	plant_part_n1	state_n4	248630 
0.92	most	house	have	wall	Most houses have walls.	0.84	y	n	n	building_n1	artifact_n1	799741 816067 
0.25	some	panda	live in	zoo	Some pandas live in zoos.	0.75	y	n	n	animal_n1	artifact_n1	484726 
0.50	some	acid	kill	bacterium	Some acid kills bacteria.	1.00	n	n	n	substance_n1	microorganism_n1	880809 608079 670305 
0.50	some	acid	destroy	bacterium	Some acid destroys bacteria.	0.93	y	n	m	substance_n1	microorganism_n1	816424  (acid, kill, bacterium)
0.83	most	house	provide	shade	Most houses provide shades.	0.81	y	n	y	building_n1	state_n4	(house, offer, shade)
0.92	most	aardvark	consume	insect	Most aardvarks consume insects.	0.77	y	n	y	animal_n1	insect_n1	(aardvark, eat, insect)

Details of the different fields are given below.

-------
LICENCE
-------
This package is distributed under the Creative Commons Attribution-ShareAlike 4.0 International License (http://creativecommons.org/licenses/by-sa/4.0/legalcode). A copy of this licence is in the PDF file in this directory.

This means you are free to:
1) Share ― copy and redistribute the material in any medium or format
2) Adapt ― remix, transform, and build upon the material
for any purpose, even commercially.
The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
1) Attribution ― You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
2) ShareAlike ― If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
3) No additional restrictions ― You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

----------------
PACKAGE CONTENTS
----------------

README.txt	  - This file
COMBINED-KB.tsv	  - 282594 (Arg1 Relation Arg2) triples related to high school general knowledge and science (see below).
		    This file is a combination of several tuple sources contained in the kb-components folder EXCEPT for 
		    the (more noisy) science-inferred.tsv set, and the animal-negatives.tsv.
		    Note that subsequent to the TACL paper, quantifiers were added to the tuples using a simple Turk task.
relations.txt	  - list of the 1605 Relations used in the tensor
entities.txt	  - list of the 6465 headwords used in the Arg1/Arg2 positions, and their type
types.tsv	  - we selected 49 types (with help from WordNet) to mark the domain/range of triples (see below), plus "Thing" for the remainder.
type-taxonomy.tsv - taxonomic relations between the selected types.
Domain Vocabulary - mar2016.tsv   - the domain vocabulary used to restrict tuple words
Creative Commons - Attribution-ShareAlike 4.0 International - CC BY-SA 4.pdf - Copy of the licence.

----------
TACL
----------
TACL-paper.pdf	- Description of how the KB was generated (Dalvi, B., Tandon, N., Clark, P. "Domain-Targeted, High Precision Knowledge Extraction", TACL, 2017 (to appear))
TACL-kb.tsv	- The original KB described in the TACL paper.


----------------------
KB-COMPONENTS
----------------------
The components of the KB are in the kb-components directory. 
The COMBINED-KB.tsv is the deduplicated union of these KBs EXCEPT for science-inferred.tsv and animal-negatives.tsv. 
   When deduplicating tuples, the entry with the highest qstrength is retained and the provenances concatenated.

animals.tsv		- 19629 tuples where Arg1 or Arg2 is an animal (see types.tsv for list of animals)
animal-negatives.tsv	- 47204 NEGATIVE examples of tuples about animals. Not included in COMBINED-KB.tsv, but may be useful for
			  	KB completion research.
science.tsv		- 217076 tuples about science (The headword of Arg1 or Arg2 is a concrete noun, see entities.tsv)	
science.tsv		- 76924 additional tuples about science, inferred solely from schema mapping rules. These are a little
			  	noiser than the original tuples, and so not included in COMBINED-KB.tsv by default.
parts.tsv		- 31795 parts relations, derived from WordNet3.0. All are assumed to be nearly universal over Arg1 (quantifier = "most", qstrength = 1.00)
partof.tsv		- 7440 partof relations, derived from WordNet3.0. The quantifier strength of (x is-part-of y) = 1/n(x is-part-of *)
isa.tsv			- 8250 isa relations, derived from WordNet3.0. All are assumed to be nearly universal over Arg1 (quantifier = "most", qstrength = 1.00)

----------------------
COLUMNS IN THE KB FILE
----------------------

In aristo-tuples-jan2017.tsv, the columns are:
   QStrength	- The quantification strength of the triple (0-1), where 1 = applies to most members of Arg1, 0 = applies to just a few members of Arg1.
		  The scale is purely a ranking scale (has no probabilistic meaning) - feel free to rescale it as required for your application.
   Quantifier	- Simple qualitative quantifier: if QStrength > 0.5 it is "most", otherwise it is "some".		  			  
   Arg1		- in (Arg1 Pred Arg2) 
   Pred		- in (Arg1 Pred Arg2)
   Arg2		- in (Arg1 Pred Arg2)
   Sentence	- Expression of this tuple as an English sentence.
   Score	- This score is now redundant (superceded by QStrength), but was the either Turk-derived or model-derived quality of the tuple (range 0-1)
   Inferred?	- "n": The tuple was directly extracted from text, WordNet, or produced by KBCompletion. The source sentence(s) id(s) are listed in the Provenance field.
   		  "y": The tuple was inferred using schema mapping rule(s) from other tuple(s). The source tuple(s) are listed in the Provenance field.
		  "m": Mixed - the tuple was both extracted from text and inferred. The source sentences and tuples are listed in the Provenance field.
   Multiword?	- If the Arg1 or Arg2 include a multiword, this is "y", else "n"
   Canonical?	- The tuple is in its canonical (normalized) form. (We retain both the original and canonical forms in this database). 
   		  Non-canonical tuples are also transformed to a canonical form, elsewhere in the database.
   Domain	- The general type of Arg1
   Range	- The general type of Arg2
   Provenance	- KBCompletion - inferred by KB Completion methods.
		  WordNet3.0 - tuple comes from WordNet v3.0.
		  ("cat","eat","food") - tuple was inferred from this tuple using a schema mapping rule (see TACL paper)
		  12413 - tuple was extracted from sentence 12413. Source setnences are available on request.

Comments about the above examples, repeated below:

QStrength	Quantifier	Arg1	Pred	Arg2	Sentence	Score	Inferred?	Multiword?	Canonical?	Domain	Range	Provenance
0.92	most	aardvark	eat	insect	Most aardvarks eat insects.	0.77	n	n	n	animal_n1	insect_n1	830913 
0.92	most	aardvark	consume	insect	Most aardvarks consume insects.	0.77	y	n	y	animal_n1	insect_n1	(aardvark, eat, insect)
0.83	most	grass seed	need	consistent moisture	Most grass seeds need consistent moisture.	0.79	y	y	n	plant_part_n1	state_n4	248630 
0.92	most	house	have	wall	Most houses have walls.	0.84	y	n	n	building_n1	artifact_n1	799741 816067 
0.25	some	panda	live in	zoo	Some pandas live in zoos.	0.75	y	n	n	animal_n1	artifact_n1	484726 
0.50	some	acid	kill	bacterium	Some acid kills bacteria.	1.00	n	n	n	substance_n1	microorganism_n1	880809 608079 670305 
0.50	some	acid	destroy	bacterium	Some acid destroys bacteria.	0.93	y	n	m	substance_n1	microorganism_n1	816424  (acid, kill, bacterium)
0.83	most	house	provide	shade	Most houses provide shades.	0.81	y	n	y	building_n1	state_n4	(house, offer, shade)

 * (aardvark, eat, insect) was extracted from sentence 830913, and was rated as applying to most aardvarks (quantifier 0.92).
 * (aardvark, consume, insect) is the canonical form for (aardvark, eat, insect), inferred from an induced schema rule (animal_n1,eat,insect_n1) -> (animal_n1,consume,insect_n1) 
 * (grass seed, need, consistent moisture) is a multiword tuple
 * (panda, live in, zoo) only applies to some (quantifier 0.25) pandas.
 * (acid, destroy, bacterium) was both extracted (from sentence 816424) and inferred (from a rule applied to (acid, kill, bacterium)).

------------
CONTACT INFO
------------
Contact bhavanad@allenai.org for questions and comments.

