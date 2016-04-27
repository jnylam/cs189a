#!/usr/bin/python

# webcrawler crawls the World Wide Web and saves the pages it finds to a file.
# Each line in the file consists of two URLs separated by a space character,
# where the second URL is one that the first URL points to.

import re, urllib, string

url = "http://data.iana.org/TLD/tlds-alpha-by-domain.txt"
tld = [string.lower(l[:-1]) for l in urllib.urlopen(url)][1:]
# tld = ["com", "org", "edu", "gov", "uk", "net", "ca", "de", "jp", "au", "us", \
#     "ru", "ch", "it", "nl", "se", "no", "es", "mil", "br", "pl", "in", \
#     "info", "nl", "cn", "ir", "cz", "ua", "eu", "biz", "za", "kr", "gr", \
#     "co", "ro", "tw", "se", "vn", "mx", "ch", "tr", "at", "hu", "be", "tv", \
#     "dk", "me", "ar", "us", "sk", "no", "fi", "id", "xyz", "cl", "by", "nz", \
#     "pt", "ie", "il", "kz", "my", "hk", "cc", "lt", "sg", "io", "su", "pk", \
#     "bg", "th", "lv", "hr", "pe", "rs", "ae", "az", "tk", "si", "ph", "club", \
#     "pro", "ee", "mobi", "asia", "top"]

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
    # true if it is not an empty string, a query string, a tag, email or a
    # file with one of the extensions above
    return not(\
        len(url) == 0 \
        or url == "/" \
        or url[0] == '?' \
        or url[:2] == "/?" \
        or '#' in url \
        or '@' in url \
        or reduce(lambda x,y: x or y, [url[-len(e)-1:] == ("." + e) for e in ext])\
        )

def clean_url(url, prefix=""):
    u, p = url, prefix
    # remove any query string suffix
    url = url.split('?')[0]
    # remove all '/' from url, breaking it into parts
    parts = [string.lower(s) for s in url.split('/') if s != ""]
    # print u, p, parts
    # remove trailing '/' from prefix
    prefix = prefix[:-1] if len(prefix) > 0 and prefix[-1] == '/' else prefix

    # return url if absolute
    if parts[0] == "http:" or parts[0] == "https:":
        return url
    s = parts[0].split('.')
    if len(s) > 1 and s[-1] in tld:
        return "http://" + '/'.join(parts)

    # url is relative, so prepend with prefix, removing any overlap
    if len(parts) > 1:
        prefix_parts = prefix.split('/')
        try:
            i = prefix_parts.index(parts[0])
            prefix = '/'.join(prefix_parts[:i])
        except ValueError:
            pass
    return '/'.join([prefix] + parts)
    # url_prefix = '/'.join(parts[:-1])
    # url_suffix = parts[-1]
    # if len(url_prefix) == 0 or url_prefix == prefix[-len(url_prefix):]:
    #     return prefix + '/' + url_suffix
    # return '/'.join([prefix, url_prefix, url_suffix])

if __name__ == "__main__":
    main()
