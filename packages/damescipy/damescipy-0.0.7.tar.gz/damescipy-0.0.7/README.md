<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. Check Test</a></li>
<li><a href="#sec-2">2. Pypi</a></li>
</ul>
</div>
</div>

Learning Scipy from Tests by David Arroyo Menéndez

# Check Test<a id="sec-1" name="sec-1"></a>

-   Execute all tests:

    $ nosetests3 tests

-   Execute one file:

    $ nosetests3 tests/test_basics.py

-   Execute one test:

    $ nosetests3 tests/test_basics.py:TestBasics.test_descriptives

# Pypi<a id="sec-2" name="sec-2"></a>

-   To install from local:

$ pip install -e .

-   To install create tar.gz in dist directory:

$ python3 setup.py register sdist

-   To upload to pypi:

$ twine upload dist/damescipy-0.1.tar.gz

-   You can install from Internet in a python virtual environment to check:

$ python3 -m venv /tmp/ds
$ cd /tmp/ds
$ source bin/activate
$ pip3 install damescipy