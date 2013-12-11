from traceback import print_exc
from ply.lex import LexError

from .parse import yacc


def testcase(func):
    print("PARSING LINE:", func.__code__.co_firstlineno)

    try:
        print(yacc.parse(func.__doc__))
    except LexError:
        print_exc()


@testcase
def test():
    """
1+!
"""

@testcase
def test():
    """
-- comment
print("Hello, world!") -- comment
"""


@testcase
def test():
    """
1+1*2
"""

@testcase
def test():
    """
1*2+1
"""

@testcase
def test():
    """
1+2+3
"""

@testcase
def test():
    """
:ok = :ok
"""

@testcase
def test():
    """
{1,1} = :atom
"""

@testcase
def test():
    """
{1, 2, 3}
"""

@testcase
def test():
    """
{1: 1}
"""

@testcase
def test():
    """
fun fac(0) -> 1; (N) -> fac(N-1) end
"""

@testcase
def test():
    """
case x of
  1 ->
    :ok;
  2 ->
    :ok
end
"""

@testcase
def test():
    """
T { .x = 1}
"""

@testcase
def test():
    """
T { [1] = 1}
"""


@testcase
def test():
    """
[i for i <- a if i]
"""


