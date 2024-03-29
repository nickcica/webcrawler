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
    '''crawl_web(seed) --> index, graph
    
    Takes the seed page and creates an index
    and graph.
    
    '''
    toCrawl = [seed]
    crawled = []
    index = {}
    graph = {} # <url>:[list of pages it links to]
    while toCrawl:
        page = toCrawl.pop() # Depth First Search
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(toCrawl,outlinks)
            crawled.append(page)
    return index, graph

def add_to_index(index, keyword, url): # --> Done
    if keyword in index:
        index[keyword].append(url)
    else:
        # not found, add new keyword to index
        index[keyword] = [url]
    
# Test --> Pass        
#add_to_index(index, 'udacity', 'http://www.udacity.com')
#add_to_index(index, 'computing', 'http://www.amc.org')
#add_to_index(index, 'udacity', 'http://www.npr.org')
#print index

def look_up(index, keyword): # --> Done
    if keyword in index:
        return index[keyword]
    return None

def add_page_to_index(index, url, content): # --> Done!
    '''add_page_to_index(index, url, content)
    
    Adds page to index.
    '''
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
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
    '''hash_string(str, int) --> returns int
    
    Takes a str and int and converts each character int the str 
    into an int, then takes a modulous of that int by the input int.
    Returns a hash value.
    
    >>> hash_string('test', 12)
    4
    '''
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
    
def make_hashtable(nbuckets):
    '''make_hashtable(int) --> return list
    
    Takes an integer and creates an x amount of list.
    These will implemented in our hash table called
    buckets
    
    >>> make_hashtable(5)
    [[],[],[],[],[]]
    '''
    # example one line solution:
    # return [[] for i in xrange(nbuckets)]
    hashtable = []
    for _ in range(0, nbuckets):
        hashtable.append([])
    return hashtable
    
def hashtable_get_bucket(hashtable, keyword):
    '''hashtable(hashtable, keyword) --> return list
    
    Takes two inputs and outputs the bucket where the
    keyword could occur.
    
    >>>hashtable_get_bucket()
    
    '''
    return hashtable[hash_string(keyword, len(hashtable))]
    
def hashtable_add(hashtable, keyword, value):
    '''hashtable_add_bucket(hashtable, keyword, value) --> return list
    
    Adds the keyword to the hashtable (in the correct bucket),
    with the associated value.
    
    >>>hashtable_add(table, 'Bill', 17)
    [[], [], [['Bill', 17]], [], []]
    '''
    hashtable_get_bucket(hashtable,keyword).append([keyword, value])
    
# Test --> Pass
#table = make_hashtable(5)
#hashtable_add(table,'Bill', 17)
#hashtable_add(table,'Coach', 4)
#hashtable_add(table,'Ellis', 11)
#hashtable_add(table,'Francis', 13)
#hashtable_add(table,'Louis', 29)
#hashtable_add(table,'Nick', 2)
#hashtable_add(table,'Rochelle', 4)
#hashtable_add(table,'Zoe', 14)
#print table

def hashtable_lookup(hashtable, keyword):
    '''hashtable_lookup(hashtable, keyword) --> value
    
    Takes two inputs, a hashtable and a key (string),
    and outputs the value associated with the key.
    
    '''
    for entry in hashtable_get_bucket(hashtable, keyword):
        if entry[0] == keyword:
            return entry[1]
    return None
    
# Test --> Pass
#table = [[['Ellis', 11], ['Francis', 13]], [], [['Bill', 17], ['Zoe', 14]],
#[['Coach', 4]], [['Louis', 29], ['Nick', 2], ['Rochelle', 4]]]
#print hashtable_lookup(table, 'Francis')
#print hashtable_lookup(table, 'Louis')
#print hashtable_lookup(table, 'Zoe')

def hashtable_update(hashtable, keyword, value):
    '''hashtable_update(hashtable, keyword, value) --> list
    
    Updates the value associate with the keyword.
    If the keyword is already in the table, change the 
    value to the new value. Otherwise, add a new entry 
    for the key and value.
    
    '''
    # think of bucket = hashtable_get_bucket(hashtable, keyword)
    for entry in hashtable_get_bucket(hashtable, keyword):
        if entry[0] == keyword:
            entry[1] = value
            return hashtable
    hashtable_get_bucket(hashtable, keyword).append([keyword, value])
    return hashtable

# Test --> Pass        
#table = [[['Ellis', 11], ['Francis', 13]], [], [['Bill', 17], ['Zoe', 14]],
#[['Coach', 4]], [['Louis', 29], ['Nick', 2], ['Rochelle', 4]]]
#hashtable_update(table, 'Bill', 42)
#hashtable_update(table, 'Rochelle', 94)
#hashtable_update(table, 'Zed', 68)
#print table

def compute_ranks(graph):
    d = 0.8 # damping factor
    numLoops = 10
    ranks = {}
    nPages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / nPages
    for i in range(0, numLoops):
        newRanks = {}
        for page in graph:
            newRank = (1 - d) / nPages
            for node in graph:
                if page in graph[node]:
                    newRank = newRank + (d * ranks[node])/(len(graph[node])) # outlinks
            newRanks[page] = newRank
        ranks = newRanks
    return ranks
    
# Test
#index, graph = crawl_web('https://www.udacity.com/cs101x/urank/index.html')
#ranks = compute_ranks(graph)
#print ranks

def lucky_search(index, ranks, keyword):
    '''
    that takes as input an index, a ranks dictionary 
    (the result of compute_ranks), and a keyword, and 
    returns the one URL most likely to be the best site 
    for that keyword. If the keyword does not appear in 
    the index, lucky_search should return None.
    '''
    pages = look_up(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    return best_page