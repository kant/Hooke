import search, extract, compare

##vars
inp = "test.txt"
nort = 1
norl = 7
pret = 0
prel = 10
timeout = 10
##/vars

norread = search.read(inp)
preread = extract.preprocess(extract.normalize(norread))[0]
search = search.search(norread)
ex = extract.text(search, timeout=timeout)
nortexts = extract.normalize(ex)
pretext = extract.preprocess(nortexts)
norcom = compare.compare(norread, nortexts, threshold=nort,length=norl)
precom = compare.compare(preread, pretext, threshold=pret, length=prel)

print(norcom, precom)