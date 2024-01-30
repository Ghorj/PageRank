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
    # corpus: dict mapping a page name to a set of pages linked to by that page
    # page: str representing which page the random surfer is currently on
    # damping_factor: float representing the damping factor to be used when generating probabilities

    # returns: dict with one key per page in the corpus

    # each key maps the probability that a random surfer would choose that page next
    # the values should add up to 1

    # random factor
    random_factor = (1 - damping_factor) / len(corpus)

    # initiate solution (every key has at least probability = random_factor)
    solution = {key: random_factor for key in corpus}

    # check each web
    for web in solution:

        # if that web is linked from page
        if web in corpus[page]:
            solution[web] += damping_factor / len(corpus[page])

    # return solution
    return solution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # corpus: dict mapping a page name to a set of pages linked by it
    # damping_factor: float to be used by the transition model
    # n: int representing the number of samples that should be generated

    # returns: dict with one key per page in the corpus

    # each key should be mapped to a value representing the estimated PageRank
    # estimated PageRank: proportion of all samples that correspond to that page
    # the value in the dict should add up to 1
    # assume n will be at least 1

    # initialise sample list
    sample = []

    # initiate options and ponderation list
    options = list(corpus.keys())

    # initiate dictionary containing solution
    solution = {key: 0 for key in options}
    
    # first sample should be generated by choosing a page at random
    choice = random.choice(options) 
    sample.append(choice)

    if n > 1:
        for _ in range(n - 1):
            # for each of the remaining samples, the next should be generated from the transition model
            # pass the previous sample to the transition_model to get probabilities for the next sample
            model = transition_model(corpus, choice, damping_factor)

            # get options and probabilities
            # the zip function returns the dictionary's key-value pairs
            # we use the * operator to unpack the tuple into separate variables
            options, ponderation = zip(*model.items())

            # apparently random.choices gives you more than one option. we only need one
            choice = random.choices(options, ponderation)[0]

            # add the new website to the sample list
            sample.append(choice)

    # count the number of times each page appears in the sample
    for item in sample:
        solution[item] += 1
            
    # normalise the counts
    total_samples = len(sample)

    for key in solution:
        solution[key] /= total_samples

    # return the solution
    return solution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # accepts a corpus of web pages and a damping factor
    # calculate PageRanks based on the iteration formula
    # return PageRank accurate to within 0.001

    # corpus: dict mapping a page name to a set of pages linked to by that page
    # damping_factor: float representing the damping factor

    # returns: a dict with one key per page in the corpus
    # each key should be mapped to a value (PageRank). The values should add 1

    # the function should begin assigning each page a rank of 1 / N (N total pages)
    old_pagerank = {key: float(1 / len(corpus)) for key in corpus}
    new_pagerank = {key: 0.0 for key in corpus}
    
    # the function should repeatedly calculate new rank values based on the current values
        
    # random_factor represents the user choosing a random website (not linked to previous)
    random_factor = (1 - damping_factor) / len(corpus)

    # infinite loop until convergence
    while True:

        # for each page 
        for page in old_pagerank:
            addition = 0.0
          
            for web in corpus:
                if page in corpus[web]:
                    addition += old_pagerank[web] / len(corpus[web])

                # if web has no links
                # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
                if not corpus[web]:
                    addition += old_pagerank[web] / len(corpus)
           
            # if there are no links to that page
            if addition == 0:
                addition = 1 / len(corpus)

            new_pagerank[page] = (random_factor + damping_factor * addition)
        
        # this process should repeat until no PageRank value changes by more than 0.001
        convergence = all(abs(new_pagerank[page] - old_pagerank[page]) < 0.001 for page in new_pagerank)

        # if it converges, break the loop
        if convergence:
            break
        
        # if it doesn't converge, iterate again starting with the values in new_pagerank
        else:
            old_pagerank = new_pagerank.copy()

    return new_pagerank


if __name__ == "__main__":
    main()
