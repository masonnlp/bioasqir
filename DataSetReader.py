"""
This module implements the class DataSetReader which contains
 the implementation of code to read the BioAsq dataset
"""
import hashlib
import io
import json
from zipfile import ZipFile
from typing import List
import bigjson
import ijson
import pandas as pd
from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import BOOLEAN, ID, NUMERIC, TEXT, Schema
from whoosh.qparser import QueryParser
import xml.etree.ElementTree as ET
import gzip


class DataReader:
    """
    BioASQ dataset reader
    """

    def __init__(self):
        pass

    def read(self):
        with ZipFile("data/allMeSH_2020.zip") as zfile:
            j = bigjson.load(zfile)


fname = "data/allMeSH_2020.zip"
f2 = "data/allMeSH_2020.json"
f3 = "allMeSH_2020.json"
d = DataReader()


class Article:
    # seem to be 14,913,938 articles

    def fromDict(data: dict):
        journal = data["journal"]
        mesh_major = data["meshMajor"]
        year = data["year"]
        abstract_text = data["abstractText"]
        pmid = data["pmid"]
        title = data["title"]
        return Article(pmid, title, journal, year, abstract_text, mesh_major)

    def __init__(self, pmid: str, title: str, journal: str,
                 year: str, abstract_text: str, mesh_major: List[str]):
        self.journal = journal
        self.mesh_major = mesh_major
        self.year = year
        self.abstract_text = abstract_text
        self.pmid = pmid
        self.title = title


def count_articles():
    pmids = set()
    zf = ZipFile(fname)
    count = 0
    with zf.open(f3, "r") as f:
        txt = io.TextIOWrapper(f, encoding="latin1", newline=None)
        articles = ijson.items(txt, "articles.item")
        for article in articles:
            art = Article(article)
            pmids.add(art.pmid)
            count += 1
            if count % 1000000 == 0:
                print(count, len(pmids))
        print('article count=', count)
    print('pmids', len(pmids))


def check_element_types():
    zf = ZipFile(fname)
    prefixes = set()
    events = set()
    with zf.open(f3, "r") as f:
        txt = io.TextIOWrapper(f, encoding="latin1", newline=None)
        parser = ijson.parse(txt)
        for prefix, event, value in parser:
            if prefix not in prefixes:
                print('prefix', prefix)
                prefixes.add(prefix)
            if event not in event:
                print('event', event)
                events.add(event)

def get_topic_counts():
    mesh_majors = set()
    zf = ZipFile(fname)
    count = 0
    with zf.open(f3, "r") as f:
        txt = io.TextIOWrapper(f, encoding="latin1", newline=None)
        articles = ijson.items(txt, "articles.item")
        for article in articles:
            art = Article(article)
            count += 1
            if count % 1000000 == 0:
                print(count, len(mesh_majors))
            for mesh_major in art.mesh_major:
                mesh_majors.add(mesh_major)
        print('article count=', count)
    print('mesh_majors', len(mesh_majors))
    for i in mesh_majors:
        print("  ", i)


def check_if_all_pmids_present():
    pmids = get_unique_pmids_8b()
    zf = ZipFile(fname)
    count = 0
    with zf.open(f3, "r") as f:
        txt = io.TextIOWrapper(f, encoding="latin1", newline=None)
        articles = ijson.items(txt, "articles.item")
        for article in articles:
            art = Article(article)
            if art.pmid in pmids:
                pmids.remove(art.pmid)
            count += 1
            if count % 1000000 == 0:
                print(count, len(pmids))
        print('article count=', count)
    print('pmids', len(pmids))
    return pmids

def get_unique_pmids_8b():
    with open('data/training8b.json', 'r') as jfile:
        pmids = set()
        j = json.load(jfile)
        questions = j['questions']
        for question in questions:
            docs = question['documents']
            for pmid in map(lambda x: x.split('/')[4], docs):
                pmids.add(pmid)
        return pmids

def process_pubmed_article_xml(txt):
    root = ET.fromstring(txt)
    pmid = root.findtext('.//PMID')
    title = root.findtext('.//ArticleTitle')
    abstract_text = root.findtext('.//AbstractText')
    journal = root.findtext('.//Title')
    year = root.findtext('.//PubDate/Year')
    mesh_major = list(map(lambda x: x.text, root.findall(".//DescriptorName")))
    return Article(pmid, title, journal, year, abstract_text, mesh_major)

def process_xml_frag():
    fname = 'data2/pubmed20n1017.xml.gz'
    with gzip.open(fname, 'rt') as f:
        count = 0
        pubmed_article_txt = ""
        record = False
        while True:
            line = f.readline()
            if not line:
                break
            if '<PubmedArticle>' in line:
                record = True
            if record:
                pubmed_article_txt += line
            if '</PubmedArticle>' in line:
                count += 1
                record = False
                process_pubmed_article_xml(pubmed_article_txt)
                pubmed_article_txt = ""
        print("lines", count)


