# Project: Pagerank

The PageRank algorithm is a vital algorithm used commonly in many popular search algorithms, such as Google, to rank webpages based on their order of priority (This algorithm was done as part of CS50 Introduction to AI using python course online on HarvardX).

## Core features
* **Random Surfer Model:** Simulates user browsing behavior using weighted probability distribution.
* **Iterative Mathematical Solver:** Converges on exact algebraic rankings using Markov state equations.
* **Corpus Crawling:** Dynamically extracts links from sets of raw HTML documents.

### Example Output
```text
PageRank Results from Sampling (n = 10000)
  1.html: 0.2201
  2.html: 0.5698
  3.html: 0.2101
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.5695
  3.html: 0.2103
```
**NOTE:** The output displays the likelihood of a user landing at each of the 3 HTML files (example files) as a probability ranging from 0 - 1 

## Main libraries used for program
* `random` - Used for structural weighted choice simulations.
* `re` - Regular expressions for parsing text.
* `os` & `sys` - Interacting with local filesystems and command-line arguments.

