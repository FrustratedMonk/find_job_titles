# from __future__ import unicode_literals
import pytest

from find_job_titles import FinderAcora, FinderPyaho

# using test titles to reduce test time for acora
TEST_TITLES = ['Senior Vice President', 'Vice President', 'President',
               'President & CEO']
# disabled testing both as they deal with unicode differently in py27
#FINDERS = [FinderAcora(TEST_TITLES), FinderPyaho()]
FINDERS = [FinderPyaho(TEST_TITLES)]


@pytest.fixture(params=FINDERS)
def finder(request):
    return request.param


def test_some_matches(finder):
    fds = [x.match for x in finder.finditer('I am the Senior Vice President')]
    assert fds == ['Senior Vice President']

    fds = [x.match for x in finder.finditer('I am the Senior Vice President asdf')]
    assert fds == ['Senior Vice President']

    fds = [x.match for x in finder.finditer('Senior Vice President I am')]
    assert fds == ['Senior Vice President']


def test_no_matches(finder):
    assert not finder.findall('defo no matches in here')


def test_position(finder):
    fds = [x.start for x in finder.findall('at the end: Vice President')]
    assert fds == [12]

    fds = [x.start for x in finder.findall(
        'in the middle Vice President of sentence')]
    assert fds == [14]

    fds = [x.start for x in finder.findall('Vice President at the beginning')]
    assert fds == [0]


def test_overlapping(finder):
    fds = [x.match for x in finder.findall('Vice President & CEO')]
    assert fds == ['Vice President', 'President & CEO']


def test_overlaps(finder):
    # leading
    FinderClass = type(finder)
    finder = FinderClass(titles=['a', 'ab', 'abc'])
    fds = [x.match for x in finder.finditer('xxxabcde')]
    assert fds == ['abc'], fds
    fds = [x.match for x in finder.finditer('xxxabc')]
    assert fds == ['abc'], fds
    fds = [x.match for x in finder.finditer('abc')]
    assert fds == ['abc'], fds

    # trailing
    finder = FinderClass(titles=['abc', 'bc', 'b'])
    fds = [x.match for x in finder.finditer('xxxabcde')]
    assert fds == ['abc'], fds
    fds = [x.match for x in finder.finditer('xxxabc')]
    assert fds == ['abc'], fds

    # middling
    finder = FinderClass(titles=['abcd', 'bc'])
    fds = [x.match for x in finder.finditer('xxxabcd')]
    assert fds == ['abcd'], fds
    fds = [x.match for x in finder.finditer('xxxabcde')]
    assert fds == ['abcd'], fds

    # cross overlap
    finder = FinderClass(titles=['abc', 'bcd'])
    fds = [x.match for x in finder.finditer('xxxabcd')]
    assert fds == ['abc', 'bcd'], fds
    fds = [x.match for x in finder.finditer('xxxabcde')]
    assert fds == ['abc', 'bcd'], fds
    fds = [x.match for x in finder.finditer('abcd')]
    assert fds == ['abc', 'bcd'], fds

    # no overlap
    finder = FinderClass(titles=['abc', 'efg'])
    fds = [x.match for x in finder.finditer('xxxabcdefg')]
    assert fds == ['abc', 'efg'], fds

    # no match
    finder = FinderClass(titles=['abc', 'efg'])
    fds = [x.match for x in finder.finditer('xxx')]
    assert fds == [], fds

    # empty string
    finder = FinderClass(titles=['abc', 'efg'])
    fds = [x.match for x in finder.finditer('')]
    assert fds == [], fds
