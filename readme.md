# TF-IDF Texts Statical Analysis

Primitive [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) and Sigma analysis written on
Python, which outputs the results to the convenient XLSX spreadsheet for article-by-article
analysis. 

TF-IDF analysis allows to detect the most "important" words in the given text of some text corpus 
(set of articles, etc). These "important" words are those which occur in the given document more 
than in any other document.

While TF-IDF analysis is useful for a set of articles, Sigma analysis is useful to analyze the most 
"important" words in the single, usually big document (books, documents, etc).

Preview
-------

TF-IDF applied to some news articles text corpus:

![Excel Spreadsheet](https://user-images.githubusercontent.com/4989256/31280494-2f061e40-aab5-11e7-93b2-60f7a9341121.png)

Sigma method applied to the book "The Hunger Games":

![Excel Spreadsheet](https://user-images.githubusercontent.com/4989256/31403036-974b030a-ae00-11e7-8e6a-398e5bc5d3ae.png)

Usage
-----

1. Install Python 3, clone the repository, enter repository directory with `cd edu-tf-idf`.
2. Install required dependencies: `pip3 install -r requirements.txt`.
3. Place texts to analyze in `/texts` directory (there are a couple already).
4. Run the analyzer with `py tf-idf.py` command.

Example
-------

##### TF-IDF: Run the program (by default, picks texts from `texts/news`):

```bash
py tf-idf.py
```

Result:

```text
Reading texts...
Done! Computing TF-IDF ranks...
Progressing text 2225/2225
Done! Writing results...
Writing worksheet 2225/2225
Done!
```

Output goes to `tf-idf.xlsx` file ready for analysis.

##### Sigma method (by default, picks texts from `texts/books`):

```bash
py sigma.py
```

Result goes to `sigma.xlsx` file.

License
-------

[MIT](license) © [Nikita Savchenko](https://nikita.tk)
