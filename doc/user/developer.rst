Developer information
######################

About this documentation
===================================

How to generate this documentation
-----------------------------------
In the main directory of the source code (vplants/MAppleT), type::

    python setup.py build_sphinx

or in the ./doc directory, type::

    make html

How to upload it on the web
------------------------------

In the main directory of the source code (vplants/MAppleT), type::

    python setup.py upload_sphinx


Code Quality
============

nosetests
---------
Version 0.9.2 of Stocatree is fully tested with  80 tests in the **./test/** directory. These tests covers the python modules used within the lsystem **stocatree.lpy**. They cover about 98% of the code. The tests may be run using the following commands::

    python setup.py nosetests

::

    Name                                     Stmts   Exec  Cover   Missing
    ----------------------------------------------------------------------
    openalea.stocatree                           4      4   100%   
    openalea.stocatree.apex                     51     51   100%   
    openalea.stocatree.colors                   70     70   100%   
    openalea.stocatree.constants                 4      4   100%   
    openalea.stocatree.fruit                    31     31   100%   
    openalea.stocatree.growth_unit               7      7   100%   
    openalea.stocatree.internode                25     25   100%   
    openalea.stocatree.leaf                     72     72   100%   
    openalea.stocatree.metamer                 185    170    91%   373-388, 398
    openalea.stocatree.output                  219    218    99%   313
    openalea.stocatree.physics                 122    122   100%   
    openalea.stocatree.pipe                      7      7   100%   
    openalea.stocatree.sequences               157    156    99%   291
    openalea.stocatree.srandom                  22     22   100%   
    openalea.stocatree.tools                     1      1   100%   
    openalea.stocatree.tools.read_function      67     67   100%   
    openalea.stocatree.tools.simulation         27     27   100%   
    openalea.stocatree.tools.surface            16     16   100%   
    openalea.stocatree.tree                     32     32   100%   
    openalea.stocatree.wood                      9      9   100%   
    ----------------------------------------------------------------------
    TOTAL                                     1128   1111    98%   
    ----------------------------------------------------------------------
    Ran 80 tests in 19.273s



doctest
-------

In addition, these documentation may contain codes that can be tested using the following command within **./doc/**::

    make doctest 

Alternatively, go to the main directory of the package and type::

    python setup.py build_sphinx -b doctest


Doctest summary
----------------
::

    Document: user/autosum
    ----------------------
    1 items passed all tests:
      55 tests in default
    55 tests in 1 items.
    55 passed and 0 failed.
    Test passed.
    
    Doctest summary
    ===============
       55 tests
        0 failures in tests
        0 failures in setup code
    build succeeded, 2 warnings.


.. sectionauthor:: Thomas Cokelaer
