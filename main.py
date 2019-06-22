import search, extract, compare, order
import time
import copy

##vars
inp = "test/test.txt"
nort = 5
norl = 50
pret = 5
prel = 10
timeout = 10
lang = "english"
pdfsupport = True
##/vars

times = []
times.append(time.time())
##Init ExtractC class
extract = extract.ExtractC(lang)

##Read and divide
read = search.read(inp)
searches = search.div(read)
times.append(time.time())

##Preprocess
norread = extract.normalize(read)
preread = extract.preprocess(norread)
times.append(time.time())

##Search
searchurls = search.search(searches)
nortexts = []
pretexts = []
for url in searchurls:
    nortexts.append( extract.normalize(extract.text(url, timeout, pdfsupport).split()))
    pretexts.append(extract.preprocess(nortexts[-1]))
times.append(time.time())

##Compare
print("\nComparing...")
norcom = compare.compare(norread, nortexts, threshold=nort,length=norl)
precom = compare.compare(preread, pretexts, threshold=pret, length=prel)
times.append(time.time())

##Finish
print("\n",len(searchurls),"Sources compared")
print("\nTextual Matches:")
m1 = order.match_elements(norcom)
m2 = order.source_sort(m1, len(searchurls))
m3 = order.check_merges(m2)
ex = order.print_matches(m3, searchurls)

print("\nIndirect Matches:")
n1 = order.match_elements(precom)
n2 = order.source_sort(m1, len(searchurls))
n3 = order.check_merges(m2)
order.print_matches(n3, searchurls, ex)

times.append(time.time())

# Time
print("\nTime taken:")
for x in range(0, len(times) - 1):
    print(times[x+1]- times[x])
print("Total:", times[-1] - times[0])