#!/usr/bin/python

# webcrawler crawls the World Wide Web and saves the pages it finds to a file.
# Each line in the file consists of two URLs separated by a space character,
# where the second URL is one that the first URL points to.

import re, urllib

def main():
    print "Enter file to save to.."
    textfile = file(raw_input("> "),'wt')
    print "Enter the URL you wish to crawl.."
    myurl = raw_input("> ")
    print "Enter the depth of the crawl..."
    depth = input("> ")
    crawl(clean_url(myurl), depth, set(), textfile)
    textfile.close()

def crawl(url, depth, visited, textfile):
    visited.add(url)
    print url
    if depth == 0:
        return
    for u in scrape(url):
        textfile.write(url + " " + u +'\n')
        if u not in visited:
            crawl(u, depth-1, visited, textfile)

def scrape(url):
    # collect the URLs listed on the webpage at the specified url
    text = urllib.urlopen(url).read()
    raw_urls = re.findall('''<a href=["'](.*?)["']''', text, re.I)
    # filter out urls to non-webpages, rewrite the rest in proper format
    return [clean_url(r, url) for r in raw_urls if is_page(r)]

ext = ["dmg", "zip", "png", "svg", "jpg", "jpeg", "gif",\
    "ppt", "pptx", "doc", "docx",\
    "pdf", "txt", "asc", "go", "c", "cpp", "h", "py"]

def is_page(url):
    # true if points to a webpage rather than a tag, email or non-html file
    return len(url) > 0 \
        and '#' not in url \
        and '@' not in url \
        and reduce(lambda x,y: x and y, [url[-len(e)-1:] != ("." + e) for e in ext])

def clean_url(url, prefix="http://"):
    # url may be relative, in which case, prepend it with prefix
    if url[-1] == '/':
        url = url[:-1]
    if url[:7] == "http://" or url[:8] == "https://":
        return url
    if prefix[-1] == '/':
        prefix = prefix[:-1]
    if len(url) > 0 and url[0] == '/':
        url = url[1:]
    return prefix + '/' + url if len(url) > 0 else prefix

if __name__ == "__main__":
    main()
