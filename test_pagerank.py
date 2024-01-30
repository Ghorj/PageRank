from pagerank import *

def test_transition_model():
    corpus_ex = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    expected_output = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}
    assert transition_model(corpus=corpus_ex, page="1.html", damping_factor=0.85) == expected_output

def test_sample_pagerank():
    ...

def test_iterate_pagerank():
    ...
    