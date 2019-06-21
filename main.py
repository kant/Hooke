import search, extract, compare
import time
import copy

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
m1 = []
for y in norcom:
    match, source, text = y
    m1.append([match.dist, text, source, match.start, match.end])

m2 = [[]for k in range(len(searchurls))]
for z in m1:
        m2[z[2]].append(z)

m3 = []
print(len(m2))
for z in m2:
        try:
                results = [(z[0],0)]
                count = 0
                for match in z[1:]:
                        if match[3] > results[-1][0][4]:
                                count += 1
                        results.append((match, count))
                m3.append(results)
        except IndexError:
                m3.append(None)

count = 0
for source in m3:
        try:
                print(source[-1][-1] + 1,"match(es) from", searchurls[count])
        except:
                pass
        count += 1

# Time
for x in range(0, len(times) - 1):
    print(times[x+1]- times[x])