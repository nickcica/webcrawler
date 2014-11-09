# WebCrawler from Udacity CS101

#index = [] 

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
    index = []
    while toCrawl:
        page = toCrawl.pop() # Depth First Search
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(toCrawl,get_all_links(content))
            crawled.append(page)
    return index

def add_to_index(index, keyword, url): # --> Done
    for entry in index:
        if entry[0] == keyword: 
            # prevent duplicate url listings
            if not url in entry[1]:
                entry[1].append(url)
                return
    # not found, add new keyword to index
    index.append([keyword,[url]])
    
# Test --> Pass        
#add_to_index(index, 'udacity', 'http://www.udacity.com')
#add_to_index(index, 'computing', 'http://www.amc.org')
#add_to_index(index, 'udacity', 'http://www.npr.org')
#print index

def look_up(index, keyword): # --> Done
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []

def add_page_to_index(index, url, content): # --> Done!
    keywords = content.split()
    for keyword in keywords:
        add_to_index(index, keyword, url)
        
# Test --> Pass
#add_page_to_index(index, 'fake.test', "This is a test")
#add_page_to_index(index, 'real.test', "This is not a test")
#print index
#print look_up(index, 'is')
        
# Test --> Pass!
#seed = 'http://www.udacity.com/cs101x/index.html'
#index = crawl_web(seed)
#print index
#print look_up(index, 'good')

def hash_string(keyword, buckets): # --> Done
    hash = 0
    for char in keyword:
        hash = (hash + ord(char)) % buckets # reduces cost
    return hash 
    
# Test --> Pass
#print hash_string('a',12)
#print hash_string('b',12)
#print hash_string('a',13)
#print hash_string('au',12)
#print hash_string('udacity',12)