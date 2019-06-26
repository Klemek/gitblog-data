# So, you want to have a blog ?

![thumbnail](thumbnail.jpg)
*Photo by [Matthieu Joannon](https://unsplash.com/@matt_j) on Unsplash*

***

As my daily navigation through [Hacker News](https://news.ycombinator.com) tend to increase,  I noticed that most developers doesn't rely on major blog services like Medium. Instead, they use other means to host on their own website their thoughts and, as I was reading a lot articles on this type of platforms, I felt this questionable need to create my own.

> Fine, but is it worth our while ? Do you have so many stories you need to share ?

Let's be frank, at the moment I don't think I am in a position to have people learn something from me, I just entered professional life after all. Nonetheless, I feel I might share some update on projects I've been working on or answers about issues I've been recently struggling with.

So, here we are, with the drive to create a personal blog. After having written the "blog hosting solution" query on Google, just before pressing return, I knew I didn't want to just do a simple `apt-get` and do some config. At that time, I wished to create not only my blog, but my own service, lost in the infiniteness of others, but unique and mine.

## Let's get to work

First let's define what a blog is :
1. A home page with a list of articles
2. A page per article
3. A method to add new articles or edit previous ones

As I wanted simplicity, I imagined a blog running on this 3 ideas :
1. Deliver HTML pages from predefined templates
2. Use a simple language to define the articles' content
3. Use versioning to edit the blog articles

Translated into technologies, my choices can be summarized with :
1. **NodeJS/Express/EJS** for HTML page delivering
2. **Markdown** for article writing
3. **Git/GitHub** for content changes

> Ok, but how is this going to work on your server ? I don't quite get the full picture.

Consider the following :

_Step One :_ You have your local repository `gitblog-data` connected to your online GitHub one and you create a new article under the current date folder like `2019/06/26` where you add a new `index.md` file. On this Markdown document you write your desired content and make a title with the usual single poung sign. You might even want to add a thumbnail with an image simply labelled `thumbnail`.

_Step Two :_ When you have finished writing your article you normally update your online repository. As your git CLI process your `git push origin master`, GitHub will receive the data and trigger a webhook connected to your website endpoint with the correct signature. This will also trigger a `git pull origin master` on the remote data folder and refresh the article list available on your website.

_Step Three :_ Accessing your home page will show you the correct article list parsed into your custom template with correct links to access each. Static resources are also loaded along side your templates in the data folder as the root directory.

_Step Four :_ TODO
