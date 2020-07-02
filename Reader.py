"""
This module reads to bioasq dataset
TODO: add index deletion and checking utility methods
TODO: clean up documentations
TODO: add id based lookups
"""
import json
import shutil
import pandas as pd
import os
import os.path
from whoosh import index
import hashlib
from whoosh.fields import Schema, TEXT, BOOLEAN, ID, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
import zipfile
import typing
import bigjson


class Reader:
    """
    Read the zipped BioASQ data set
    """

    def __inti__():
        pass

    def read():
        with Zipfile("data/allMeSH_2020.zip", "r") as zfile:
            j = bigjson.load(zfile)


