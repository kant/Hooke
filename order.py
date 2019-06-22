def match_elements(matches):
    #Extract match elements
    output = []
    for y in matches:
        match, source, text = y
        output.append([match.dist, text, source, match.start, match.end])
    return output

def source_sort(matches, leng):
    #Orginize by source
    output = [[]for k in range(leng)]
    for x in matches:
        output[x[2]].append(x)
    return output

def check_merges(matches):
    #Checks merging matches
    output = []
    for z in matches:
        try:
                results = [(z[0],0)]
                count = 0
                for match in z[1:]:
                        if match[3] > results[-1][0][4]:
                                count += 1
                        results.append((match, count))
                output.append(results)
        except IndexError:
                output.append(None)
    return output

def print_matches(matches, searchurls, ex = []):
    #Prints Matches
    count = 0
    exclude = []
    for source in matches:
            try:
                    if count not in ex:
                        print(source[-1][-1] + 1,"match (es) from", searchurls[count])
                        exclude.append(count)
            except:
                    pass
            count += 1
    return exclude