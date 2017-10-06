# TF_IDF Texts Statical Analysis

Primitive [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) analysis written on Python.

Usage
-----

1. Install Python 3, clone the repository, enter repository directory with `cd edu-tf-idf`.
2. Install required dependencies: `pip3 install -r requirements.txt`.
3. Place texts to analyze in `/texts` directory (there are a couple already).
4. Run the analyzer with `py index.py` command.

Example
-------

Run the program:

```bash
py index.py
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

License
-------

[MIT](license) © [Nikita Savchenko](https://nikita.tk)