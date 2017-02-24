Title: How I built this Blog using Pelican
Date: 2016-5-19 11:15
Tags: how-to, python, pelican, blog, website
Category: How-to
Slug: how-i-built-this-blog
Author: zhoudshu

I have wanted to run a personal blog for a long time. Because I am family with Python, thus, I am prior to choose python blog framework. At first I chosed the [__mezzanine__](http://mezzanine.jupo.org) which is best Django CMS. I installed this system and had used it for several weeks. I find that this system is not easy to be installed, managed, maintained, migrated, furthemore, it is slowly accessed for saving data to database.

Finally I finded the static blog technology by [staicgen WebSite](https://www.staticgen.com). I choose the Python Language system Pelican which is the best Python tool for static blog

## What is Pelican?
Pelican is a static-site generation tool that abstracts a massive amount of the HTML/CSS generation for you, and lets you write your post in Markdown or reST or whatever markup your little heart desires. It has a rich community offering dozens of cool plugins and custom-built themes, all simple to edit to your tastes, right down to the raw HTML, CSS, and JS.

To top it all off, because Pelican creates static sites, you can host your website for *__absolutely free__* on Github Pages. No server maintenance, no hosting fees, no fuss.

## Setting up your environment

First off, Pelican is well documented. Read the docs [here](http://docs.getpelican.com/en/latest/quickstart.html) - they are great.

Things you'll need to run Pelican

* Python
* Pelican
* Markdown (if that's your thing)
* Fabric, probably, for automation

Woo! That's it. Assuming you have Python 2.7.x or 3.3.x, just run the following:

```bash
$ pip install pelican markdown fabric
```

## Create my Blog
You Can use pelican's quickstart method to build the default website. We'll get around to applying themes in a bit. Use the `pelican-quickstart` command and follow the prompts

```bash
$ pelican-quickstart
```
But I find one good blog website [beneathdata](http://beneathdata.com), I am very like it, and this website is open source. So I clone one backup from [tylerhartley git repository](https://github.com/tylerhartley/beneathdata.git). Thank tylerhartley very much. I modified three images and pelicanconf.py，and my blog is built. it is so easy.

## Applying a theme

with `pelican-bootstrap3` being far and away my favorite and best documented. To apply a theme, it's this easy - get yourself a copy of the repo, stick it somewhere (maybe in your project folder), and then point Pelican to it in your pelicanconf.py script with the setting:

```python
THEME = '/path/to/theme'
```
It is **THAT** easy. 

## Github Pages

First. Build one repository

First you'll need to decide if you want to use a Github user page or project page. The only real difference is default Github url - username.github.io for user pages and username.github.io/projectname for projects.  

To get started with GH Pages, follow the instructions [here](https://pages.github.com/). Once you have your repo created, clone it and create a branch. I called mine source. 

Second. Upload static file to repository

```bash
$ cd output
$ git init
$ git remote add origin https://github.com/username/username.github.com.git
$ git add .
$ git commit -m "the first version of blog"
$ git push origin master

```
Happy blogging.
