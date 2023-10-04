# Identifying References to Legal Literature in Portuguese Superior Court Decisions - Master's Project Page

![Project's Pipeline](https://github.com/fabio-noga/reference-identification/assets/19254233/25df53c3-91b1-442a-adbf-2f60f857cd7b)

Note: This project has had a major change for readability purposes. Having that in mind beware that some methods, functionalities or usages might not work 100% correctly as they might need to be adapted. With that said, `pipeline_example.py` works correctly and examplifies how the projects behaves (excluding NoSQL)

## Features
* Identify references from authors' names, patterns of reference, and by BERT (LLM);
* Connect to a database, in our case we used NoSql (MongoDB) as the elected choice so it can be seen with its syntaxes;
* From extract reference (or with correctly inputed data), it is possible to generate an quotation to be used in a documents bibliography.

## Usage

Even if this project was made with the itention to identify references in portuguese court, the code is open to be adapted to any language, with proper grammar rules or fed dataset.

It has great results with multiple approaches, as can be seen here:

<img src="https://github.com/fabio-noga/reference-identification/assets/19254233/55344f20-35b2-4d8b-9957-25379e62bbee" width=75% height=75%>

## Project's Document

The official project's document's repository can be found on https://hdl.handle.net/10216/152246

If you want to refer to it you can [see it here](https://www.bibsonomy.org/bibtex/2184b0854d62f7ac461b76be6b1cdb74b/fabio-noga) or use the bib.tex
```
@article{noga2023references,
  abstract = {The decision-making process in the court of law often relies on academic legal writings, with judges referencing legal books, research articles, and other scholarly works. Establishing a citation index based on higher court jurisprudence, organized by thematic research areas, enables the assessment of the scholarly impact of legal professionals like professors, researchers, and graduate students. The automatic identification of citations in texts is a challenging task, involving the recognition of references to legal academic writings, disambiguation of authorship, and varied citation patterns. This dissertation addresses these challenges by proposing a digital infrastructure using non-relational databases, algorithms for reference identification and cleaning, and author attribution.},
  author = {Nogueira, Fabio},
  biburl = {https://www.bibsonomy.org/bibtex/2184b0854d62f7ac461b76be6b1cdb74b/fabio-noga},
  editor = {Silva, Fernando and Guimarães, Maria Raquel},
  keywords = {Architecture Citation Data Extraction Identification Language Mining Natural NoSQL Processing Text Transformer},
  language = {English},
  month = {07},
  pages = 111,
  title = {Identifying References to Legal Literature in Portuguese Superior Court Decisions},
  url = {https://hdl.handle.net/10216/152246},
  year = 2023
}```
