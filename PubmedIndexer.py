"""
This module indexes the Pubmed dataset using Woosh
"""
import os
import os.path
import shutil
from whoosh import index
from whoosh.fields import Schema, TEXT, IDLIST, ID, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from PubmedReader import PubmedReader


class PubmedIndexer:
    """
    PubmedIndexer
    TODO flush out docustring
    """

    def __init__(self):
        """
        default construstor for now
        """
        pass

    def mk_index(self, indexpath="indexdir", overwrite=False):
        """
        creates an index for IR operations
        """
        if os.path.exists(indexpath):
            if overwrite:
                shutil.rmtree(indexpath)
        if not os.path.exists(indexpath):
            os.mkdir(indexpath)
        self.pubmed_article_schema = Schema(
            pmid=ID(stored=True),
            title=TEXT(stored=True),
            journal=TEXT(stored=True),
            mesh_major=IDLIST(stored=True),
            year=NUMERIC(stored=True),
            abstract_text=TEXT(stored=True, analyzer=StemmingAnalyzer()))
        self.pubmed_article_ix = index.create_in("indexdir", self.pubmed_article_schema)

    def rm_index(self, indexpath="indexdir"):
        if os.path.exists(indexpath):
            os.rmdir(indexpath)

    def index_docs(self, articles, limit=10000000):
        """"
        indexes documents
        TODO: add handling LockError
        TODO: add handling test for LockError
        """
        print("adding documents")
        pubmed_article_writer = self.pubmed_article_ix.writer()
        count = 0
        for article in articles:
            count += 1
            if count > limit:
                break
            pubmed_article_writer.add_document(
                pmid=article.pmid,
                title=article.title,
                journal=article.journal,
                mesh_major=article.mesh_major,
                year=article.year,
                abstract_text=article.abstract_text)

        pubmed_article_writer.commit()
        print("commiting index, added", count, "documents")

    def query_pubmed_articles(self, query=u"nederduits"):
        """
        simple method to query index
        """
        res = []
        qp = QueryParser("abstract_text", schema=self.pubmed_article_schema)
        q = qp.parse(query)
        with self.pubmed_article_ix.searcher() as s:
            results = s.search(q)
            for result in results:
                res.append(result)
                print(result)
            return res

    def print_results(results):
        """
        simple utility method to print search results to the console
        also serves as sample code to use in other modules to
        access search results
        """
        for result in results:
            print(result)

def test_main():
    """
    main testing method
    TODO: make it more exhaustive
    """
    pubmed_indexer = PubmedIndexer()
    pubmed_indexer.mk_index(overwrite=True)
    reader = PubmedReader()
    articles = reader.process_xml_frags('data2', max_article_count=3000)
    pubmed_indexer.index_docs(articles)
    pubmed_indexer.query_pubmed_articles("DICER1")

