from Hooke import search, extract, compare, order
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

def Textual(input, verbose = True, length = 20, threshhold = 5, threads = 15, max_time = 30, timeout = 10, pdfsupport = True):
    '''Does a textual search of the input'''
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

class Nlp(compare.nlp):
    '''Full inheritance from compare.nlp'''

def shingle(input,k):
    '''Shingle the input in k length ngrams'''
    output = compare.shingle(input, k)
    return output

def shingle_compare(input):
    '''Uses Chebyshev distance to compare the texts
    Takes input, the texts, the gap between matches, and the minimum size fo the clusters.
    Returns set of matches and a dictionary of the distance of each point
    '''
    output = compare.shin_matches(input)
    output = compare.cluster(input)
    dist = compare.get_dist(output)
    return output, dist

def shingle_order(input, dic1, dist, dic2):
    '''Does the ordering'''
    output, dens = order.de_preprocess(input, dic1, dist, dic2)
    dens = order.bilinear(dens)
    output = order.shingle_final(output, dens)
    return output

def pre_search(norread, stopwords=None):
    '''Makes a google search of the text without stop words'''
    if not stopwords:
        stopwords = Nlp().stopwords
    norread = [x for x in norread if x not in stopwords]
    output = ""
    for x in norread:
        output = output + " " + x
    output = divide(output)
    return search_texts(output)

def Shingled(input, lang, min, gap, shingle_size, threads = 10, pdfsupport = True):
    '''Does a complete search of the input using nlp'''
    nlp = Nlp(lang)
    read, norread = read_file(input)
    sources = search(divide(read))
    sources.append([x for x in pre_search(norread, Nlp.stopwords) if x not in sources])
    nortexts = download_texts(sources, threads = threads, pdfsupport = pdfsupport)
    preread = nlp.preprocess(norread)
    pretexts = nlp.bulk_preprocess(nortexts, threads = threads)


if __name__ == "__main__":
    times = tim()
    Textual("In information theory, linguistics and computer science, the Levenshtein distance is a string metric for measuring the difference between two sequences. Informally, the Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other")
    print_time(times)
