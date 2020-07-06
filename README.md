# bioasqir
bioasq ir module

### Installation
To install this module:

1. check out the code from github

```
git clone git@github.com:masonnlp/bioasqir.git

```

2. Make sure you have pipenv installed -- if you do not see https://pypi.org/project/pipenv/. Pipenv can typically be installed by issuing the following command:

```
pip install pipenv
```

3. Install all the dependencies
```
cd bioasqir
pipenv install
```

4. Download the pubmed dataset from ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/ -- not this is not necessary -- another more efficient is to have someone who alrwady has created this index to share their index with you. But if you must you can follow the following commands (note you must have wget installed on your system -- see https://www.gnu.org/software/wget/)
```
mkdir data2
cd data2
wget --no-parent -r -nd -Pdata2 ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/
```
