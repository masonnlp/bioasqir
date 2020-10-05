from PubmedReader import PubmedReader
from PubmedIndexer import PubmedIndexer
import lxml.etree as ET

def formatTree(filename):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(filename, parser)
    tree.write(filename, pretty_print=True)

def extract_and_write(filename, results, question_id, query):
    """
    Extract information from IR system and write to XML file. Format is:
    <Result PMID=1>
       <Journal>Title of journal</Journal>
       <Year>Year published</Year>
       <Title>Title of article</Title>
       <Abstract>Abstract (~couple of sentences/a paragraph)</Abstract>
       <MERS>tag1</MERS>
       <MERS>tag2</MERS>
    </Result>
    :param filename: Name of the XML file used in the QA system
    """
    origTree = ET.parse(filename)
    root = origTree.getroot()
    # parser = ET.XMLParser(remove_blank_text=True)
    # root = ET.parse(filename, parser).getroot()

    Q = root.find("Q")
    IR = Q.find("IR")

    # Find the IR element to write to
    questions = root.findall("Q")
    for question in questions:
      if question.get("id") == question_id:
        IR = question.find("IR")
        # Create a subelement for each part of the result (there can be many)
        for pa in results:
          queryUsed = ET.SubElement(IR, "QueryUsed")
          queryUsed.text = query
          result = ET.SubElement(IR, "Result")
          result.set("PMID", pa.pmid)
          journal = ET.SubElement(result, "Journal")
          journal.text = pa.journal
          year = ET.SubElement(result, "Year")
          year.text = pa.year
          title = ET.SubElement(result, "Title")
          title.text = pa.title
          abstract = ET.SubElement(result, "Abstract")
          abstract.text = pa.abstract_text
          for mesh in pa.mesh_major:
              mesh_major = ET.SubElement(result, "MeSH")
              mesh_major.text = mesh
      tree = ET.ElementTree(root)
      tree.write(filename, pretty_print=True)

def main():
    # TODO: Figure out how to use already indexed index (indexdir)

    # pubmed_indexer = PubmedIndexer()
    # pubmed_indexer.mk_index()
    # results = pubmed_indexer.search('flu')
    # print(results)

    # Index ALL the pubmed data (~4-5 million documents)
    # reader = PubmedReader()
    # articles = reader.process_xml_frags('data2', max_article_count=5000000)
    # pubmed_indexer.index_docs(articles, limit=5000000)

    # TODO: Fix KeyError: 'year' problem
    pubmed_indexer = PubmedIndexer()
    pubmed_indexer.mk_index('indexdir2', overwrite=True)
    reader = PubmedReader()
    articles = reader.process_xml_frags('data2', max_article_count=5000)
    pubmed_indexer.index_docs(articles, limit=5000)

    origTree = ET.parse("test.XML")
    root = origTree.getroot()

    for question in root.findall('Q'):
        # Question ID to write IR results to the appropriate question
        qid = question.get("id")

        qp = question.find("QP")

        # If there is no query, use the original question
        if qp.find("Query").text:
            query = qp.find("Query").text
        else:
            query = question.text

        results = pubmed_indexer.search(query)
        extract_and_write("test.XML", results, qid, query)

if __name__ == "__main__":
    main()