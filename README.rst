========
badmatch
========

Erlang-like pattern matching for CPython VM


Code Examples
=============


Hello, world!
-------------

.. code::

    -- this is comment
    print("Hello, world!").


Factorial
---------

.. code::

    fun factorial
    (0) ->
        1
    (int{} = N)
      when N > 0 ->
        N * factorial(N-1)


Quicksort
---------

.. code::

    fun qsort
    ([]) ->
        []
    (:[H|T]) ->
        :{A, B} = partition(fun (E) -> E > H end, T)
        qsort(A) + [H] + qsort(B)


Syntax
======


comment

.. code::

    -- comment here
    print("Hello, world!") -- comment here


atom

.. code::

    atom = :ok


built-in container types

.. code::

    tuple = :{1, 2, 3}
    set = {1, 2, 3}
    dict = {1:1, 2:2}
    empty_dict = {:}
    list = [1,2]


match tuple, same as Erlang

.. code::

    -- tuple
    :{:ok, x} = :{:ok, 1}
    1 = x


match other object

.. code::

    T{.year=year, .month=month, .day=day} = date.today()
    date = T

    list{[0]=1} = [1,2,3]

    dict{["a"]=1} = {"a": 1, "b": 2}


matching iterator

.. code::

    :[1|T] = [1,2,3]


replace some field to create new object, as erlang record syntax.
mostly for namedtuple

.. code::

    a = SomeNamedTuple(x=1)
    b = #a{x=2}


assignment

.. code::

    a.b <= 1


import

.. code::

    import x
    import y <- a.b.c


list comprehension

.. code::

    [2,3] = [ e for e <- [1,2,3] when e > 1 ]


special tokens

.. code::

    case for end fun import of when
    and or not
    band bor inv
    -- " ' : # ( ) [ ] { }
    = <= =< -> >= =:= =/= > <
    + - * / **
