from . import search, extract, compare, order
import time
from concurrent.futures import ThreadPoolExecutor, wait

def tim(times = None):
    '''Times Action'''
    if times:
        times.append(time.time())
    else:
        times = []
        times.append(time.time())
        return times

def read_file(file):
    '''Read and tokenize file using textract
    Takes a file as input, and outputs raw and normalized texts
    If it fails to read, it just runs "read_text"
    '''
    read = search.read(file)
    norread = extract.normalize(read)
    return read, norread

def read_text(text):
    '''Reads and tokenizes text
    Takes a text as input, and outputs raw and normalized texts 
    '''
    read = text.split()
    norread = extract.normalize(read)
    return read, norread

def divide(read):
    '''Divides text, output list of searches'''
    queries = search.div(read)
    return queries

def search_texts(queries):
    '''Searches using google'''
    sources = search.search(queries)
    return sources

def download_texts(sources, threads = 10, max_time = 30, timeout = 10, pdfsupport = False):
    '''Download texts from search using multithreading
    Returns normalized set of texts. The indices match their source
    '''
    nortexts = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for url in sources:
            futures.append(executor.submit(extract.doall, url, timeout, pdfsupport))
        wait(futures, timeout=max_time)
        for x in futures:
            nortexts.append(x.result())
    return nortexts

def levenshtein_compare(norread, nortexts, length = 30, threshhold = 7):
    '''Compares the texts with the input
    Returns unordered set of matches
    '''
    norcom = compare.compare(norread, nortexts, threshold=threshhold,length=length)
    return norcom

def order_results(norcom, sources):
    '''Orders Array of matches
    Returns ordered
    '''
    matchs = norcom
    sources = sources
    m2 = order.source_sort(order.match_elements(matchs) , len(sources))
    m3 = order.check_merges(m2)
    m4 = order.separate_matches(m3)
    matches = order.join_matches(m4)
    return matches

def print_matches(matches, sources, used = None):
    '''Prints
    Returns a list of indices of used sources
    '''
    if not used:
        used = []
    print("\nMatches:")
    used = order.print_matches(matches, sources, used)
    return used

def Textual(input, verbose = True, length = 50, threshhold = 10, threads = 15, max_time = 30, timeout = 10, pdfsupport = True):
    '''Does everything'''
    read, norread = read_file(input)
    queries = divide(read)
    sources = search_texts(queries)
    nortexts = download_texts(sources, threads = threads, max_time = max_time, timeout = timeout, pdfsupport = pdfsupport)
    norcom = levenshtein_compare(norread, nortexts,length = length, threshhold = threshhold)
    matches = order_results(norcom, sources)
    if verbose:
        print_matches(matches, sources)
    return matches

def print_time(times):
    '''Prints Time'''
    print("\nTime taken:")
    for x in range(0, len(times) - 1):
        print(times[x+1]- times[x])
    print("Total:", times[-1] - times[0])

if __name__ == "__main__":
    times = tim()
    Textual("Hooke Written in python, and based on quite a few requirements It is yet to work properly")
    print_time(times)