# WebCrawler from Udacity CS101

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
    
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links
        
def crawl_web(seed):
    toCrawl = [seed]
    crawled = []
    while toCrawl:
        page = toCrawl.pop() # Depth First Search
        if page not in crawled:
            union(toCrawl,get_all_links(get_page(page)))
            crawled.append(page)
    return crawled
            
#links = get_all_links(get_page('http://www.udacity.com/cs101x/index.html'))
#print links
seed = 'http://www.udacity.com/cs101x/index.html'
print crawl_web(seed)