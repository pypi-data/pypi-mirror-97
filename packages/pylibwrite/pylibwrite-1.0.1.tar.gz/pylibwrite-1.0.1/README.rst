==================
pylibwrite
==================

OverView
==========

A library that creates a requirements.txt file using only the libraries listed in the python file directly below it．

作業環境下(カレントディレクトリ)にあるpythonファイルに記載されている外部パッケージのみを抽出してrequirements.txtを作成するライブラリ．

Sample
===========

sample python file ::

    import os
    import sys
    import json
    import re
    import math
    import requests
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime
    import time
    import japanize_matplotlib
    import pandas as pd
    from tomato import tomatoaaaaaaaaas
    # import sadaa
    # from sdadda
    import sqlite3
    import email

result(gen-requirements.txt) ::

    japanize-matplotlib
    requests
    numpy
    tomato
    pandas
    matplotlib

Tools Version
================

:Python: 3.7.6
:pip: 20.2.4

How to Install and Run
=========================

1. PYPI

    $ pip install pylibwrite

2. Get the code from the repository and execute it.

    $ git clone https://github.com/Villager-B/pylibwrite.git

    $ cd pylibwrite

    $ pip install .

    $ pylibwrite

    create gen-requirements.txt

Please help me
========================

Currently, libraries such as bs4 are rewritten using :code:`pylibwrite/convert_libname.json`.

I'm sure there are other libraries that don't work as well. 

Please let me know.

:Libraries that are currently supported: 

.. csv-table::
    :header: "lib name", "package name"
    :widths: 15, 40

    "japanize_matplotlib","japanize-matplotlib"
    "bs4","beautifulsoup4"

Development Procedure
========================

1. Checkout.
2. Follow the steps below to install .

    pip install -e .