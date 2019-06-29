def match_elements(matches):
    '''Extract match elements'''
    output = []
    for y in matches:
        match, source, text = y
        output.append([match.dist, text, source, match.start, match.end])
    return output

def source_sort(matches, leng):
    '''Orginize by source'''
    output = [[]for k in range(leng)]
    for x in matches:
        output[x[2]].append(x)
    return output

def check_merges(matches):
    '''Checks merging matches'''
    output = []
    for source in matches:
        try:
                results = [(source[0],0)]
                count = 0
                for match in source[1:]:
                        if match[3] > results[-1][0][4]:
                                count += 1
                        results.append((match, count))
                output.append(results)
        except IndexError:
                output.append(None)
    return output

def print_matches(matches, searchurls, ex = []):
    '''Prints Matches'''
    count = 0
    exclude = []
    for source in matches:
            try:
                    if count not in ex:
                        print(len(source),"match (es) from", searchurls[count])
                        exclude.append(count)
            except:
                    pass
            count += 1
    return exclude

def separate_matches(matches):
        '''Separates matches based on last classification'''
        output = []
        for source in matches:
                try:
                        ts = [[] for x in range(source[-1][-1] + 1)]
                        for match in source:
                                ts[match[1]].append(match[0])
                        output.append(ts)
                except:
                        output.append(None)
        return output


def join_matches(matches):
        '''Joins each array of the same match, putting the texts togather and averaging its distance'''
        output = []
        for source in matches:
                ns = []
                try:
                        for match in source:
                                tex = match[0][1][:-1]
                                added = 0
                                for m in match:
                                        added += m[0]
                                        tex.append(m[1][-1])
                                ns.append([added/len(match), tex, match[0][3],match[-1][4]])
                except:
                        ns = None
                output.append(ns)
        return output
