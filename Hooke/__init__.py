from . import search, extract, compare, order
import time
from concurrent.futures import ThreadPoolExecutor, wait

class Hooke:
    def __init__(self, timb = None, lang = None):
        # Inits
        if timb:
            self.timb = True
            self.times = []
            self.tim()
        if lang:
            self.extract = extract.ExtractC(lang)

    def tim(self):
        if self.timb:
            self.times.append(time.time())

    def read_text(self, input):
        #Read and tokenize
        self.read = search.read(input)
        self.norread = self.extract.normalize(self.read)
        self.tim()

    def search_texts(self):
        #Divides and Search
        searches = search.div(self.read)
        self.searchurls = search.search(searches)
        self.tim()
    
    def download_texts(self, threads = 10, max_time = 30, timeout = 10, pdfsupport = False):
        #Download
        nortexts = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for url in self.searchurls:
                futures.append(executor.submit(self.extract.doall, url, timeout, pdfsupport))
            wait(futures, timeout=max_time)
            for x in futures:
                nortexts.append(x.result())
        self.nortexts = nortexts
        self.tim()

    def compare_texts(self, length = 50, threshhold = 10):
        #Compare
        self.norcom = compare.compare(self.norread, self.nortexts, threshold=threshhold,length=length)
        self.tim()

    def order_results(self):
        #Order Array
        matchs = self.norcom
        searchurls = self.searchurls
        m2 = order.source_sort(order.match_elements(matchs) , len(searchurls))
        m3 = order.check_merges(m2)
        m4 = order.separate_matches(m3)
        self.matches = order.join_matches(m4)
        self.tim()

    def print_matches(self, results = None, searchurls = None):
        #Prints
        print("\nMatches:")
        self.used = order.print_matches(self.matches, self.searchurls)
        self.tim()

    def Textual(self,input, lang = "english", length = 50, threshhold = 10, timb = True, threads = 15, max_time = 30, timeout = 10, pdfsupport = True):
        # Does everything
        self.__init__(timb, lang)
        self.read_text(input)
        self.search_texts()
        self.download_texts(threads = threads, max_time = max_time, timeout = timeout, pdfsupport = pdfsupport)
        self.compare_texts(length = length, threshhold = threshhold)
        self.order_results()

    def time(self):
        # Time
        print("\nTime taken:")
        for x in range(0, len(self.times) - 1):
            print(self.times[x+1]- self.times[x])
        print("Total:", self.times[-1] - self.times[0])


if __name__ == "__main__":
    hk = Hooke()
    hk.Textual()
    hk.print_matches()
    hk.time()