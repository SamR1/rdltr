# rdltr

[![PyPI version](https://img.shields.io/pypi/v/rdltr.svg)](https://pypi.org/project/rdltr/)
[![Downloads](https://pepy.tech/badge/rdltr)](https://pepy.tech/project/rdltr)
[![Python Version](https://img.shields.io/badge/python-3.6+-brightgreen.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-1.1.1-brightgreen.svg)](http://flask.pocoo.org/)
[![Vue Version](https://img.shields.io/badge/vue-2.6.11-brightgreen.svg)](https://vuejs.org/)  
[![code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) 
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier) 
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/70a84eefaea5413abf464a053abf9d19)](https://www.codacy.com/app/SamR1/rdltr)
[![Coverage Status](https://coveralls.io/repos/github/SamR1/rdltr/badge.svg?branch=master)](https://coveralls.io/github/SamR1/rdltr?branch=master)<sup><sup>1</sup></sup>
[![pipeline status](https://gitlab.com/SamR1/rdltr/badges/master/pipeline.svg)](https://gitlab.com/SamR1/rdltr/commits/master)

----

**rdltr** is a _read-it later_ web application: save articles for later reading.  
Categories and tags can be used to classify articles.  

It is also possible to add articles from [FreshRSS](https://freshrss.org/).  
A Firefox add-on is available: [SamR1/rdltr-addon](https://github.com/SamR1/rdltr-addon), allowing
 to add article from browser side.  
➡️ see [documentation](https://samr1.github.io/rdltr/index.html) for installation instructions and features.  

![application screenshot](https://raw.githubusercontent.com/SamR1/rdltr/master/docsrc/source/_images/screenshot.png)

Initially a small project to learn Vue (with Flask)<sup>2</sup>, **rdltr** uses 
**[readability-lxml](https://github.com/buriy/python-readability)** to parse HTML 
content.

---

Notes:  
_1. test coverage: only for Python_  
_2. application structure inspired by this tutorial: [Full-stack single page application with Vue.js and Flask](https://codeburst.io/full-stack-single-page-application-with-vue-js-and-flask-b1e036315532)_  
