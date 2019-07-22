# So, you want to create your own blog?

![thumbnail](./thumbnail.jpg)
*Photo by [Matthieu Joannon](https://unsplash.com/@matt_j) on Unsplash*

***

As my daily navigation through [Hacker News](https://news.ycombinator.com) tends to increase,  I noticed that most developers don't rely on major blog services like Medium. Instead, they use other means to host their thoughts on their own website  and, as I was reading a lot articles on these types of platforms, I felt this questionable need to create my own.

> Fine, but is it worth our while? Do you have so many stories you need to share?

Let's be frank, at the moment I don't think I am in a position to have people learn something from me, I just entered professional life after all. Nonetheless, I feel I might share some update on projects I've been working on or answers about issues I've been recently struggling with.

So, here we are, with the drive to create a personal blog. After having written the "blog hosting solution" query on Google, just before pressing return, I knew I didn't want to just do a simple `apt-get` and do some config. At that time, I wished to create not only my blog, but my own service, lost in the infiniteness of others, but unique and mine.

**Let's get to work**

First, let's define what a blog is:
1. A home page with a list of articles
2. A page per article
3. A method to add new articles or edit previous ones

As I wanted simplicity, I imagined a blog running on these 3 ideas:
1. Deliver HTML pages from predefined templates
2. Use a simple language to define the articles' content
3. Use versioning to edit the blog articles

Translated into technologies, my choices can be summarized with:
1. **NodeJS/Express/EJS** for HTML page delivering
2. **Markdown** for article writing
3. **Git/GitHub** for content changes

> Ok, but how is this going to work on your server? I don't quite get the full picture.

Consider the following:

**Step One:**  
You have your local repository `gitblog-data` connected to your online GitHub one and you create a new article under the current date folder like `2019/06/26` where you add a new `index.md` file. On this Markdown document you write your desired content and make a title with the usual single pound sign (#). You might even want to add a thumbnail with an image simply labelled `thumbnail`.

**Step Two:**  
When you have finished writing your article you normally update your online repository. As your git CLI process your `git push origin master`, GitHub will receive the data and trigger a webhook connected to your website endpoint with the correct signature. This will also trigger a `git pull origin master` on the remote data folder and refresh the article list available on your website.

**Step Three:**  
Accessing your home page will show you the correct article list incorporated into your custom template with correct links to access each. Static resources are also loaded along side your templates in the data folder as the root directory.

**Step Four:**  
At the article's URL, you can find it formatted from Markdown to HTML then fitted into a template that, for example, adds a footer or a "share this article" button.

**Step Five:**  
Now you now want to change some image or fix a typo in your article. You can simply access and edit from your local repository, or even better: directly from GitHub in file edition where you can preview your Markdown changes (This article is written using this method)

And there you go, a simple yet complete tool to share your thought on your own server. At least on paper. 3 days of work and ~700 lines of code (not including unit tests) later I had this project up and running: [GitBlog.md](https://github.com/Klemek/GitBlog.md/) featuring:

* Markdown to HTML rendering with [Showdown](http://showdownjs.com/)
* Fully customizable templates and view engine
* RSS feed endpoint
* Secured Git webhook endpoint
* Code highlighting with server-side [Prism](https://prismjs.com/)
* LaTeX math equations with server-side [MathJax](https://www.mathjax.org/)
* UML diagrams with server-side [PlantUML](plantuml.com/)

All of it running on a small yet powerful NodeJS server.

> Nice, but will this tool be used by others or is it just yours?

I don't really care. I made it with a lot of configuration possibilities, so others might want to use it for its simplicity. You may want to tell me its design is not that eye-catching yet it's only a reflect of my own need of minimalism (and lack of designing skills). You can imagine a full bootstrapped version with animations and stuff and it would be totally doable with this project.

Anyway, I will use it personally as mentioned earlier and I hope to count you as my few yet meaningful readers.

[![Hacker News](https://img.shields.io/badge/dynamic/json.svg?color=green&style=for-the-badge&label=Hacker%20News&query=score&suffix=%20points&url=https%3A%2F%2Fhacker-news.firebaseio.com%2Fv0%2Fitem%2F20285234.json)
![Comments](https://img.shields.io/badge/dynamic/json.svg?color=orange&style=for-the-badge&label=Comments&query=descendants&url=https%3A%2F%2Fhacker-news.firebaseio.com%2Fv0%2Fitem%2F20285234.json)](https://news.ycombinator.com/item?id=20285234)
