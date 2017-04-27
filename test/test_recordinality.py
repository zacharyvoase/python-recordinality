import os

from recordinality import Recordinality


example_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.txt')
example_count = len(set(open(example_file).read().strip().splitlines()))


TRIALS = 100


def test_smoke():
    results = 0
    for trial in range(TRIALS):
        sketch = Recordinality(size=256)
        with open(example_file) as example:
            for line in example:
                if line.strip():
                    sketch.add(line.strip().encode('utf-8'))
        results += sketch.cardinality()
    mean_guess = results / TRIALS
    error = abs(mean_guess - example_count) / float(example_count)
    print("guess: {}, actual: {} (error: {:.4f})".format(
        mean_guess,
        example_count,
        error))
    assert error <= 0.05, "Unacceptable error (>5%)"
