import search, extract, compare
import time

##vars
inp = "test.txt"
nort = 5
norl = 50
pret = 0
prel = 50
timeout = 10
lang = "english"
##/vars

times = []
times.append(time.time())
# Init ExtractC class
extract = extract.ExtractC(lang)

# Read and divide
read = search.read(inp)
searches = search.div(read)
times.append(time.time())

# Preprocess
norread = extract.normalize(read)
preread = extract.preprocess(norread)
times.append(time.time())

# Search
searchurls = search.search(searches)
nortexts = []
pretexts = []
for url in searchurls:
    nortexts.append( extract.normalize(extract.text(url, timeout).split()))
    pretexts.append(extract.preprocess(nortexts[-1]))
times.append(time.time())

#Compare
norcom = compare.compare(norread, nortexts, threshold=nort,length=norl)
precom = compare.compare(preread, pretexts, threshold=pret, length=prel)
times.append(time.time())

#Finish
sources = []
for y in norcom:
    match, source, text = y
    print(match)
    if source not in sources:
        sources.append(source)

print(sources)
for source in sources:
    print(searchurls[source])
for x in range(0, len(times) - 1):
    print(times[x+1]- times[x])