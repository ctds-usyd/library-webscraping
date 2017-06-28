---
title: "Visual scraping using browser extensions"
teaching: 45
exercises: 20
questions:
- "How can I get started scraping data off the web?"
- "How can I use CSS selectors to precisely select what data to scrape?"
objectives:
- "Introduce the Chrome Web Scraper extension."
- "Practice scraping data that is well structured."
- "Use XPath queries to refine what needs to be scraped when data is less structured."
keypoints:
- "Data that is relatively well structured (in a table) is relatively easily to scrape."
- "More often than not, web scraping tools need to be told what to scrape."
- "XPath can be used to define what information to scrape, and how to structure it."
- "More advanced data cleaning operations are best done in a subsequent step."
---

# An introduction to visual scrapers

Visual scrapers are tools in which the user can visually select the elements to extract, and the logical order to follow in performing a sequence of extractions. They require little or no code, and assist in designing XPath or CSS selectors.

Visual scraping tools vary in how flexible they are (in comparison to the full expressiveness of coding your own), how easy to use, to what extent they help you identify and debug scraping problems, how easy it is to keep and transfer your scraper to another service, and how costly the service is.
Many visual scrapers require you to pay for their services beyond a small number of trial extractions, may only store your data for a limited time, and may not provide a way for you to take your scraper off their site for reuse or extension.
Some do not allow you to write your own XPath / CSS / regular expression selectors; some only support CSS or XPath but not the other.

In designing this lesson, we have chosen to emphasise free solutions that give you ultimate control of the scraper and its data.
As of June 2017, we have only found a few visual scraping tools that are [Free Open-Source Software](https://en.wikipedia.org/wiki/Free_and_open-source_software), including [webscraper.io's Web Scraper Chrome extension](http://webscraper.io/) and [Portia](https://scrapinghub.com/portia/).
While there are numerous advantages to Portia, we found it relatively difficult to install and ran into bugs (though it calls itself a Beta, so bugs are to be expected).
In comparison to refined commercial tools, Web Scraper's user experience leaves much to be desired, but it is a flexible tool and a useful introduction to scraping without coding.

# Using the Web Scraper Chrome extension

We are finally ready to do some web scraping. Let's go to the index of
[UNSC resolutions](http://www.un.org/en/sc/documents/resolutions/) in our Chrome browser.

To use the Web Scraper, we need to open the Developer Tools as in the previous episode (right click on the page and choose _Inspect Element_ is often the simplest way in). In the Developer Tools, you should find a tab entitled _Web Scraper_. Activate the tab, click _Create new sitemap_ below it and then _Create sitemap_, as numbered in the following:

![Creating a new sitemap]({{ page.root }}/fig/web-scraper-create.png)

(If the Developer Tools were not docked at the bottom of your web browser window (usually they are), you will need to [dock them there](https://stackoverflow.com/questions/10023640/how-to-reposition-chrome-developer-tools).)

_Sitemap_ is essentially the Web Scraper extension's name for a scraper. It is a sequence of rules for how to extract data by proceeding from one extraction to the next. We'll name the sitemap "unsc-resolutions", set the start page as `http://www.un.org/en/sc/documents/resolutions/`, and click _Create Sitemap_.

Before we start constructing the sitemap, let's try to understand the structure of a complete sitemap.

## The selector graph: here's one we made earlier

A Web Scraper sitemap consists of a collection of selectors each of which may identify:

* specific content to extract;
* elements of the page containing content to extract (e.g. a result in a list of search results, each of which contains multiple specific pieces of content, like title, URL and summary); or
* a link to follow and continue scraping from.

Each selector (except a special one called `_root`) has a parent selector defining the context in which each selector is to be applied. For example, the following shows a visual representation ("Selector graph") of the final scraper we will build for the UNSC resolutions:

![Selector graph for UNSC resolutions]({{ page.root }}/fig/web-scraper-unsc-graph.png)

Here `_root` represents the starting URL, the home page of UNSC resolutions. From it, the scraper gets a link to each `year` page. For each year, it extracts a set of `resolution` elements. For each `resolution` element, it extracts a single `symbol`, a single `date`, a single `title`, and a single `url`.

Since the years are linked from the start page, `_root` is the parent of the `year` selector. Since resolutions can only be extracted once on a year page, `year` is the parent selector of `resolution`. Similarly, since a symbol is extracted for each resolution, `resolution` is the parent selector of `symbol`. Etc.

## Navigating from root to year pages

At this point, we have the Web Scraper tool open at the `_root` with an empty list of child selectors.

![An empty list of selectors at root]({{ page.root }}/fig/web-scraper-empty-selector-list.png)

Click _Add new selector_. We will add the selector that takes us from the index to each year page. Let's give it the id `year`. Its type is _Link_. We want to get multiple year links from the root, so we will check the Multiple box below.

Under _Selector_, have tools for building a CSS selector. Rightmost (highlighted blue below) is a text box where we can enter a CSS selector. The _Select_ button gives us a tool for visually selecting elements on the page to construct a CSS selector. _Element Preview_ highlights on the page those elements that would be selected by the specified selector. _Data Preview_ pops up a sample of the data that would be extracted by the specified selector.

![Adding a year selector]({{ page.root }}/fig/web-scraper-year-selector.png)

Let's start by entering the selector `a`, which will match all `<a>` (hyperlink) elements in the page. Click _Element Preview_ and all links in the page you are viewing will blush. (You must be talking about them!) Click _Data Preview_ and we'll see that from the set of links we can construct a table consisting of the text and the link URL (plus a couple of administrative details).

We only want to capture year links, not all links, in the page. We could construct the CSS selector by inspecting the page's source or element tree. Instead we will use Web Scraper's _Select_ feature.

Click _Select_. A small selection tool will appear above the Developer Tools, hovering over the UNSC page. Hover your mouse over one of the year links and it should be highlighted in green:

![Using the Select popup feature]({{ page.root }}/fig/web-scraper-select-popup.png)

Click one of the year links. A very specific CSS selector such as `tr:nth-of-type(3) td:nth-of-type(1) a` will be filled in on the left of the selection tool, and the year you clicked will be reddened to indicate that it is included in the proposed selector. Click one of the other (unselected) year links and the CSS selector should be adjusted to include it. Keep clicking years until all of them are selected. (If you make a mistake, or if -- unfortunately -- Web Scraper refuses to let you select all the links you desire, click the _Select_ button in the main Web Scraper tool to start again.) The final selector should be `td a`, which will select every link (`<a>`) element anywhere inside a table cell (`<td>`) element anywhere in the page. Click _Done Selecting_ and the identified selector will appear in the text box where we entered `a` before.

We do not require the scraper to delay before selecting each year, nor do we need to change the parent selector (`_root` is correct). So click _Save Selector_. This returns us to the list of selectors that are children of `_root`. Now we have one: the `year` selector.

### Running the scraper

What happens if we run the scraper as it is now? To do so, click _Sitemap (unsc-resolutions)_ to get a drop-down menu, and click Scrape as shown:

![Using the Select popup feature]({{ page.root }}/fig/web-scraper-dropdown-scrape.png)

The scrape pane gives us some options about how slowly Web Scraper should perform its scraping to avoid overloading the web server with requests and to give the web browser time to load pages. We are fine with the defaults, so click _Start scraping_. A window will pop up, where the scraper is doing its browsing. The list of year links will be scraped, and the window will close, as the scraping is complete! We can see a table of `year` and `year-href` values to show us that our very simple scraper has worked! The _Export data as CSV_ entry on the drop-down menu will even bring the scraped data into Excel.

Click _Sitemap (unsc-resolutions)_ to get the drop-down menu again, and _Selectors_ will return you to the root selectors. Note that you can click _Data preview_ for a quick and dirty alternative to actually running the scrape.

## Scraping data for each year

Clicking the `year` ID will take you to _its_ child selectors; there are none. It will not take you to an example year page, so you will have to click a year link yourself, say 2016, to design its child selectors as they only apply in the context of each year.

We will now create a selector which captures each element containing data for a single resolution, i.e. each selected item should be a row of the table.

* id: `resolution`
* type: Element
* multiple: checked
* parent selector: `year`
* selector: ???

The selector for rows is, in this case, a bit tricky, for two reasons:

1. The table heading is also a row, but doesn't contain resolution data, so a simple expression like `<tr>` which captures all table rows will not suffice. We cannot use CSS2 Selectors to say that we'd only like rows containing more than one `<td>` cell (though we could do this kind of thing with XPath). We can, however, use CSS2 selectors to get all but the first using an advanced version of `:nth-child` or `:nth-of-type`.
2. Using the visual _Select_ tool, it is hard to select a row in entirety, as clicking anywhere in a table will select a cell `<td>` element or something within it.


# OLD


We are interested in downloading this list to a spreadsheet, with columns for names and
constituencies. Do do so, we will use the Scraper extension in the Chrome browser
(refer to the [Setup](setup/) section for help installing these tools).

## Scrape similar

With the extension installed, we can select the first row of the House of Commons members
list, do a right click and choose "Scrape similar" from the contextual menu:

![Screenshot of the Scraper contextual menu]({{ page.root }}/fig/scraper-contextmenu.png)

Alternatively, the "Scrape similar" option can also be accessed from the Scraper extension
icon:

![Screenshot of the Scraper menu]({{ page.root }}/fig/scraper-menu.png)

Either operation will bring up the Scraper window:

![Screenshot of the Scraper main window]({{ page.root }}/fig/scraper-ukparl-01.png)

We recognize that Scraper has generated XPath queries that corresponds to the data we had
selected upon calling it. The Selector (highlighted in red in the above screenshot)
 has been set to `//tbody/tr[td]` which selects
all the rows of the table, delimiting the data we want to extract.

In fact, we can try out that query using the technique that we learned in the previous
section by typing the following in the browser console:

~~~
$x("//tbody/tr[td]")
~~~
{: .source}

returns something like

~~~
<- Array [672]
~~~
{: .output}

which we can explore in the console to make sure this is the right data.

Scraper also recognized that there were two columns in that table, and has accordingly
created two such columns (highlighted in blue in the screenshot), 
each with its own XPath selector, `*[1]` and `*[2]`.

To understand what this means, we have to remember that XPath queries are relative to the
current context node. The context node has been set by the Selector query above, so
those queries are relative to the array of `tr` elements that has been selected.

We can replicate their effect by trying out 

~~~
$x("//tbody/tr[td]/*[1]")
~~~
{: .source}

in the console. This should select only the first column of the table. The same goes for the
second column.

But in this case, we don't need to fiddle with the XPath queries too much, as Scraper was able to deduce
them for us, and we can use the export functions to either create a Google Spreadsheet with the
results, or copy them into the clipboard in Tab Separated Values (TSV) format for pasting into
a text document, a spreadsheet or Open Refine.

There is one bit of data cleanup we might want to do, though. If we paste the data copied from Scraper
into a text document, we see something like this:

~~~
Name	Constituency
A	back to top
                                 Abbott, Ms Diane                                 (Labour)                             	Hackney North and Stoke Newington
                                 Abrahams, Debbie                                 (Labour)                             	Oldham East and Saddleworth
~~~
{: .output}

This is because there are a lot of unnecessary white spaces in the HTML that's behind that table, which
are being captured by Scraper. We can however tweak the XPath column selectors to take advantage of the
`normalize-space` XPath function:

~~~
normalize-space(*[1])
normalize-space(*[2])
~~~

![Screenshot of the Scraper window showing the Column selectors]({{ page.root }}/fig/scraper-ukparl-02.png)

We now need to tell Scraper to scrape the data again by using our new selectors, this is done by clicking
on the "Scrape" button. The preview will not noticeably change, but if we now copy again the results
and paste them in our text editor, we should see

~~~
Name	Constituency
A	back to top
Abbott, Ms Diane (Labour)	Hackney North and Stoke Newington
Abrahams, Debbie (Labour)	Oldham East and Saddleworth
Adams, Nigel (Conservative)	Selby and Ainsty
~~~
{: .output}

which is a bit cleaner.

> ## Scrape the list of Ontario MPPs
> Use Scraper to export the list of [current members of the Ontario Legislative Assembly](http://www.ontla.on.ca/web/members/members_current.do?locale=en)
> and try exporting the results in your favourite spreadsheet or data analysis
> software.
>
> Once you have done that, try adding a third column containing the URLs that are underneath
> the names of the MPPs and that are leading to the detail page for each parliamentarian.
>
> Tips:
> 
> * To add another column in Scraper, use the little green "+" icon in the columns list.
> * Look at the source code and try out XPath queries in the console until you find what
>   you are looking for.
> * The syntax to select the value of an attribute of the type `<element attribute="value">`
>   is `element/@attribute`.
> * The `concat()` XPath function can be use to concatenate things.
>
> > ## Solution
> > 
> > Add a third column with the XPath query
> > 
> > ~~~
> > *[1]/a/@href
> > ~~~
> > {: .source}
> >
> > ![Screenshot of the Scraper window on the Ontario MPP page]({{ page.root }}/fig/scraper-ontparl-01.png)
> > 
> > This extracts the URLs, but as luck would have it, those URLs are relative to the list
> > page (i.e. they are missing `http://www.ontla.on.ca/web/members/`). We can use the
> > `concat()` XPath function to construct the full URLs:
> >
> > ~~~
> > concat('http://www.ontla.on.ca/web/members/',*[1]/a/@href)
> > ~~~
> > {: .source}
> >
> > ![Screenshot of the Scraper window on the Ontario MPP page]({{ page.root }}/fig/scraper-ontparl-02.png)
> >
> {: .solution}
{: .challenge}



## Custom XPath queries

Sometimes, however, we do have to do a bit of work to get Scraper to select the data elements
that we are interested in.

Going back to the example of the Canadian Parliament we saw in the introduction,
there is a page on the same website that [lists the mailing addresses](http://www.parl.gc.ca/Parliamentarians/en/members/addresses) of all
parliamentarians. We are interested in scraping those addresses.

If we select the addresses for the first MP and try the "Scrape similar" function...

![Screenshot of the Scraper context menu being used on an address block]({{ page.root }}/fig/scraper-canparl-01.png)

Scraper produces this:

![Screenshot of the Scraper window trying to scrape addresses]({{ page.root }}/fig/scraper-canparl-02.png)

which does a nice job separating the address elements, but what if instead we want a table of
the addresses of all MPs? Selecting multiple addresses instead does not help. Remember what we said
about computers not being smart about structuring information? This is a good example. We humans
know what the different blocks of texts on the screen mean, but the computer will need some help from
us to make sense of it.

We need to tell Scraper what exactly to scrape, using XPath.

If we look at the HTML source code of that page, we see that individual MPs are all within `ul`
elements:

~~~
(...)
<ul>
   <li><h3>Aboultaif, Ziad</h3></li>
   <li>
      <span class="addresstype">Hill Office</span>
      <span>Telephone:</span>
      <span>613-992-0946</span>
      <span>Fax:</span>            
      <span>613-992-0973</span>
   </li>
   <li>
         <ul>       
            <li><span class="addresstype">Constituency Office(s)</span></li>
            <li>                            
               <span>8119 - 160 Avenue (Main Office)</span>
               <span>Suite 204A</span>
               <span>Edmonton, Alberta</span>
               <span>T5Z 0G3</span>
               <span>Telephone:</span> <span>780-822-1540</span>
               <span>Fax:</span> <span>780-822-1544</span>                                    
               <span class="spacer"></span>
            </li>                         
      </ul>
   </li>                                   
</ul>   
(...)
~~~
{: .output}

So let's try changing the Selector XPath in Scraper to

~~~
//body/div[1]/div/ul
~~~
{: .source}

and hit "Scrape". We get something that is closer to what we want, with one line per MP, but
the addresses are still all in one block of unstructured text:

![Screenshot of the Scraper window trying to scrape addresses]({{ page.root }}/fig/scraper-canparl-03.png)

Looking closer at the HTML source, we see that name and addresses are separated by `li` elements
within those `ul` elements. So let's add a few columns based on those elements:

~~~
./li[1] -> Name
./li[2] -> Hill Office
./li[3] -> Constituency
~~~
{: .source}

This produces the following result:

![Screenshot of the Scraper window scraping addresses]({{ page.root }}/fig/scraper-canparl-04.png)

The addresses are still one big block of text each, but at least we now have a table for all MPs
and the addresses are separated.

> ## Scrape the Canadian MPs' phone numbers
> Keep working on the example above to add a column for the Hill Office phone number
> and fax number for each MP.
>
>
> > ## Solution
> > 
> > Add columns with the XPath query
> > 
> > ~~~
> > ./li[2]/span[3] -> Hill Office Phone
> > ./li[2]/span[5] -> Hill Office Fax
> > ~~~
> > {: .source}
> >
> > ![Screenshot of the Scraper window on scraping MP phone numbers]({{ page.root }}/fig/scraper-canparl-05.png)
> >
> {: .solution}
{: .challenge}
