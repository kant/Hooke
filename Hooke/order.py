class Match:
        '''Main class of the match
        Variables
        start = Start of the match
        end = End of the match
        density = A depth map of the distance of the match
        s_start = The start of the match from the source
        s_end = The end of the match from the source
        mean = Find average distance of the match
        source = Source of the Match
        '''
        density = None
        s_start = None
        s_end = None
        source = None

        def __init__(self, start, end):
                self.start = start
                self.end = end
                
        def mean(self):
                if not self.density:
                        print("Warning: No density specified, Skipping...")
                        return
                x = 0
                for y in self.density:
                        x += y
                x = x/len(self.density)
                return x


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

def de_preprocess(matches, dic1, dic2, dist):
        '''Takes the preprocessed match and makes it normal, and takes both dictionaries'''
        output=[]
        for i, cluster in enumerate(matches):
                newcluster = []
                for x in enumerate(cluster):
                        newcluster.append(dic1[x[0]])
                start = newcluster[0]
                end = newcluster[-1]
                mstart = dic2[cluster[0][1]]
                mend = dic2[cluster[-1][1]]
                dens = [None]* (start-end)
                for j,x in newcluster:
                        dens[x-start] = dist[j]
                output.append(start, end, mstart, mend)
        return output, dens

def bilinear(dens):
        '''Linearly aliases the match accuracy for matches between existing ones'''
        for x in dens:
                points = [i for i, y in enumerate(x) if y]
                pairs = []
                y = None
                for z in points:
                        if y:
                                points.append(y,x)
                        y = x
                for y in pairs:
                        interval = round(  (dens[y[1]]-dens[y[0]]) / (y[1]- y[0])  ,2)
                        added = x[y[0]]
                        if y[1]-y[0] > 1:
                                for z in range(1, y[1]-y[0]-1):
                                        added += interval
                                        x[y[0]+z] = added
        return dens

def shingle_final(input, dens):
        '''Makes the matches into the Match class'''
        output = []
        for x in input:
                y = Match(start = x[0], end = x[1])
                y.s_start = x[2]
                y.density = dens
                y.s_end = x[3]
                output.append(y)
        return output