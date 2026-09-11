import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    all_pages = list(corpus.keys())
    n = len(all_pages)

    # Base probability: every page gets an equal share of (1 - damping_factor)
    base_prob = (1 - damping_factor) / n

    links = corpus[page]

    # If the page has no outgoing links, treat it as linking to all pages equally
    if not links:
        for p in all_pages:
            distribution[p] = 1 / n
        return distribution

    # Probability added to each linked page from the damping factor
    link_prob = damping_factor / len(links)

    for p in all_pages:
        distribution[p] = base_prob
        if p in links:
            distribution[p] += link_prob

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {page: 0 for page in corpus}

    # First sample: choose a page at random
    current = random.choice(list(corpus.keys()))
    counts[current] += 1

    # Remaining samples: use transition model
    for _ in range(n - 1):
        model = transition_model(corpus, current, damping_factor)
        pages = list(model.keys())
        weights = [model[p] for p in pages]
        current = random.choices(pages, weights=weights, k=1)[0]
        counts[current] += 1

    # Normalise counts to probabilities
    ranks = {page: count / n for page, count in counts.items()}
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)

    # Start with equal rank for every page
    ranks = {page: 1 / n for page in corpus}

    # Build a helper: for each page, which pages link TO it?
    # Also treat pages with no links as linking to every page.
    def links_to(target):
        """Yield every page that has a link pointing to target."""
        for page, links in corpus.items():
            if not links:
                # No links → pretend it links to every page
                yield page
            elif target in links:
                yield page

    while True:
        new_ranks = {}

        for page in corpus:
            # Sum of PageRank contributions from all pages that link here
            link_sum = sum(
                ranks[incoming] / (len(corpus[incoming]) if corpus[incoming] else n)
                for incoming in links_to(page)
            )
            new_ranks[page] = (1 - damping_factor) / n + damping_factor * link_sum

        # Check for convergence: no rank changed by more than 0.001
        if all(abs(new_ranks[p] - ranks[p]) < 0.001 for p in ranks):
            break

        ranks = new_ranks

    return ranks


if __name__ == "__main__":
    main()
