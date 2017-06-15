---
title: "Introduction: What is web scraping?"
teaching: 10
exercises: 0
questions:
- "What is web scraping and why is it useful?"
- "What are typical use cases for web scraping?"
objectives:
- "Introduce the concept of structured data"
- "Discuss how data can be extracted from web pages"
- "Introduce the examples that will be used in this lesson"
keypoints:
- "Humans are good at categorizing information, computers not so much."
- "Often, data on a web site is not properly structured, making its extraction difficult."
- "Web scraping is the process of automating the extraction of data from web sites."
---

## What is web scraping?

Web scraping is a technique for **targeted, automated extraction of information from websites**.

For example:

* Online stores will often scour the publicly available pages of their competitors,
  scrape **item names and prices** and then use this information to adjust their own prices. 
* Marketing databases may be compiled by scraping **contact information** such as email
  addresses.

Applications of scraping in research may include:

* tracking trends in the real estate market by scraping data from real estate
  web sites
* collecting online article comments and other discourse for analysis
* gathering data on membership and activity of online organisations

### Behind the web's facade

At the heart of the problem which web scraping solves is that the web is
(mostly) designed for humans.  Very often, web sites are built to display
**structured content** which is stored in a database on a web server.  Yet they
tend to provide content in a way that loads quickly, is useful for someone with
a mouse or a touchscreen, and looks good.  They format the structured content
with templates, surround it with boilerplate content like headers, make parts
of it shown or hidden with the click of a mouse.  Such presentation is often
called **unstructured**.

Web scraping aims to return specific content in a web site to a structured
form: a database, a spreadsheet, an XML representation, etc.

Web designers expect that readers will interpret the content by using prior
knowledge of what a header looks like, what a menu looks like, what a *next
page* link looks like, what a person's name, a location, an email address.
Computers do not have this intuition.

Web scraping therefore involves:

* telling a computer how to navigate through a web site to find required
  content (sometimes called *spidering*); and
* providing *patterns* with which the computer can identify and extract
  required content.

### Not web scraping: structured content on the web

There are, however, many forms of structured content on the web, which are
(ideally) already *machine-readable* (although they may still need
transformation to fit into your database/format of choice). These include:

* Data downloads: some web sites provide their content in structured forms.
  Some names for data formats include Excel, CSV, RSS, XML and JSON.
* APIs: many major sources and distributors of content provide software
  developers with a [web-based Application Programming
  Interface](https://en.wikipedia.org/wiki/Web_API) to query and download their
  often dynamic data in a structured format.  APIs tend to differ from each
  other in design, so some new development tends to be required to get data
  from each one. Most require some authentication like a username and password
  before access is granted (even when it is granted for free).
* semantic web knowledge bases: web sites providing structured knowledge, of
  which [WikiData](http://wikidata.org) is a good example. These tend to be
  structured as [OWL](https://en.wikipedia.org/wiki/Web_Ontology_Language)
  ontologies, and can often be queried through
  [SPARQL](https://en.wikipedia.org/wiki/SPARQL) endpoints or downloaded as
  large data collections.
* microformats: some web sites may overlay their visual content with [specially
  schematised labels](http://schema.org) for certain kinds of knowledge, such
  as publication metadata (title, author, publication date), contact details or
  product reviews.  While web sites using microformats are by far in the
  minority, where they are, specialised extraction tools do not need to be
  developed.

Before scraping a web site, it is always a good idea to check whether a
structured representation of the same content is provided.

### Not web scraping: information extraction

Although it may sometimes be included under the rubric of web scraping, we are
not going to cover tasks that target content in free text.  Such tasks, known
by the name *information extraction* may seek a list of organisations
mentioned, or may try to interpret a textual description of an event to build
structure records of, say, casualties in national disasters or business
acquisitions.  Related technology in text interpretation may try to determine
if an author used positive or negative language.  Related technology in
information extraction may try to aggregate content found in differently
formatted tables across many web sites (or academic papers).

These are real technologies, but not within scope of web scraping. In contrast
to these, web scraping usually expects content to be consistently formatted,
and extractable with very high precision (the extracted content is very clean
of errors) and recall (the extracted content is complete from the pages
visited).

## Example: scraping government websites for contact addresses

In this lesson, the examples that we will use all involve extracting contact information
from government websites listing the members of various constituencies. A practical example
of why this information would be useful could be an advocacy group wishing to making it easier
for citizens to contact their representatives about a particular issue. 

Let's start by looking at the current list of members of the Canadian parliament, which is available
on the [Parliament of Canada website](http://www.parl.gc.ca/Parliamentarians/en/members).

This is how this page appears in November 2016:

![Screenshot of the Parliament of Canada website]({{ page.root }}/fig/canparl.png)

There are several features (circled in the image above) that make the data on this page easier to work with.
The search, reorder, refine features and display modes hint that the data is actually stored in a (structured)
database before being displayed on this page. The data can be readily downloaded as a Comma-Separated Values (CSV)
file or XML, which allows anyone to load this data in their own database, spreadsheet or computer program to
reuse it.

Even though the information displayed in the view above isn't labeled, a person visiting this site with some
knowledge of Canadian geography and politics is quickly able to figure out what information pertains to the 
name of the politicians, the geographical area or the political party they represent. This is because human
beings are usually good at using context and prior knowledge to quickly categorize information.

Computers, on the other hand, can't do this unless we provide them with more information.
Fortunately, if we look at the source HTML code of this page, we see that the information displayed is actually
organized inside labeled elements:

~~~
(...)
<div>
    <a href="/Parliamentarians/en/members/Ziad-Aboultaif(89156)"> 
        <img alt="Photo - Ziad Aboultaif - Click to open the Member of Parliament profile" title="Photo - Ziad Aboultaif - Click to open the Member of Parliament profile" src="http://www.parl.gc.ca/Parliamentarians/Images/OfficialMPPhotos/42/AboultaifZiad_CPC.jpg" class="picture" />
        <div class="full-name">
		    <span class="honorific"><abbr></abbr></span>
            <span class="first-name">Ziad</span>
            <span class="last-name">Aboultaif</span>
        </div>
    </a>
    <div class="caucus-banner" style="background-color:#002395"></div>
    <div class="caucus">Conservative</div>
    <div class="constituency">Edmonton Manning</div>
    <div class="province">Alberta</div>        
</div>
(...)
~~~
{: .output}

Thanks to these labels, we could relatively easily instruct a computer to look for all parliamentarians from
Alberta and list their names and caucus information.

> ## Structured vs unstructured data
>
> When presented with information, human beings are good at quickly categorizing it and extracting the data
> that they are interested in. For example, when we look at a magazine rack, provided the titles are written
> in a script that we are able to read, we can rapidly figure out the titles of the magazines, the stories they
> contain, the language they are written in, etc. and we can probably also easily organize them by topic, 
> recognize those that are aimed at children, or even whether they lean toward a particular end of the
> political spectrum. Computers have a much harder time making sense of such _unstructured_ data unless
> we specifically tell them what elements data is made of, for example by adding labels such as
> _this is the title of this magazine_ or _this is a magazine about food_. Data in which individual elements
> are separated and labelled is said to be _structured_.
>
{: .callout}

Let's look now at the current list of members for the [UK House of Commons](https://www.parliament.uk/mps-lords-and-offices/mps/). 

![Screenshot of the UK House of Commons website]({{ page.root }}/fig/ukparl.png)

This page also displays a list of names, political and geographical affiliation. There is a search box and
a filter option, but no obvious way to download this information and reuse it.

Here is the code for this page:

~~~
(...)
<table>
    <tbody>
        (...)
        <tr id="ctl00_ctl00_(...)_trItemRow" class="first">
            <td>Aberavon</td>
            <td id="ctl00_ctl00_(...)_tdNameCellRight">
                <a id="ctl00_ctl00_(...)_hypName" href="http://www.parliament.uk/biographies/commons/stephen-kinnock/4359">Kinnock, Stephen</a>(Labour)
            </td>
        </tr>
        (...)
    </tbody>
</table>
(...)
~~~
{: .output}

We see that this data has been structured for displaying purposes (it is arranged in rows inside
a table) but the different elements of information are not clearly labeled.

What if we wanted to download this dataset and, for example, compare it with the Canadian list of MPs
to analyze gender representation, or the representation of political forces in the two groups?
We could try copy-pasting the entire table into a spreadsheet or even manually
copy-pasting the names and parties in another document, but this can quickly become impractical when
faced with a large set of data. What if we wanted to collect this information for every country that
has a parliamentary system?

Fortunately, there are tools to automate at least part of the process. This technique is called
_web scraping_. 

>
> "Web scraping (web harvesting or web data extraction) is a computer software technique of 
> extracting information from websites."
> (Source: [Wikipedia](https://en.wikipedia.org/wiki/Web_scraping))
>

This technique is closely related to _web indexing_ which is what search engines like Google do
to build the database that is queried when users are searching. The difference is that web indexing
(using tools typically called "bots" or "crawlers") aims to visit _all_ web sites recursively,
following all links (unless blocked), index all data and store the result in a database and repeat
every so often to keep their index current.

Web scraping, on the other hand, is a more focused technique, typically targeting one web site at a
time to extract unstructured information and put it in a structured form for reuse.

In this lesson, we will continue exploring the examples above and try different techniques to extract
the information they contain. But before we launch into web scraping proper, we need to look
a bit closer at how information is organized in an HTML document and how to build queries to access
a specific subset of that information.

## Tools and techniques for scraping

A number of tools have been developed to help build web scrapers.  These differ
in capability/expressiveness and in their usability without programming.
Several of the available tools are associated with services which host the
scraper and run it for a fee.
We present the following tools:

* [Scrapy](https://scrapy.org/) is a general framework for developing scrapers
  in the Python programming language.  Its vast flexibility is matched by
  substantial technical barriers to entry.
* [Portia](https://scrapinghub.com/portia/) is a visual scraping tool built on
  the Scrapy framework. It is free open-source software, such that you (or IT
  support staff) can easily launch your own Portia instance to develop and run
  scrapers. It still requires some technical knowledge about the structure of a
  scraper and how to specify patterns for extracting specific content.
* [Grepsr](https://www.grepsr.com) provides an extension for the Chrome
  Browser, which delivers an extremely intuitive interface for building
  scrapers with minimal technical knowledge. Although it demands a fee for any
  substantial scraping project, its simplicity was outlying in our review of
  available scraping tools, and serves us well as an introduction to the
  scraping task.

We will now drill down into scraping proceeding from the simplest tool the most
intricate.

# References

* [Web Scraping (Wikipedia)](https://en.wikipedia.org/wiki/Web_scraping)
* [The Data Journalism Handbook: Getting Data from the Web](http://datajournalismhandbook.org/1.0/en/getting_data_3.html)
