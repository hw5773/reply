import sys
import os
import oid

OID = 0
AID = 1
ID = 2
SYM = 3
ANTI = 4
CONTENT = 5

def usage():
    print ("Analyze the top ranking IDs")
    print ("python3 analysis.py <input data>")
    exit(1)

def top_ids(fname, threshold, idx):
    if threshold <= 0:
        print (">>> Error: Threshold should be a positive integer.")
        return None

    if idx != SYM and idx != ANTI:
        print (">>> Error: idx should be SYM or ANTI.")
        return None

    try:
        f = open(fname, "r")
    except:
        print (">>> Error: File not found: %s" % fname)
        return None

    d = {}

    # Elements in the map will be d: id -> [(oid, aid, number, content)]
    for line in f:
        tmp = line.strip().split(", ")
        identity = tmp[ID]
        num = int(tmp[idx])

        if num > threshold or identity in d:
            if identity not in d:
                d[identity] = []
            d[identity].append((oid.oid_to_str[tmp[OID]], tmp[AID], num, tmp[CONTENT]))
    
    f.close()
    return d

def print_result(d, threshold, role):
    if not d:
        print (">>> Error: The list is an error")
        return

    if role != SYM and role != ANTI:
        print (">>> Error: role should be SYM or ANTI.")
        return

    print ("")
    if role == SYM:
        print ("Top IDs with the highest number of \"Sympathy\"")
    else:
        print ("Top IDs with the highest number of \"Anti-sympathy\"")

    for e in d:
        lst = d[e]
        if len(lst) <= 1:
            continue
        s = "%s (%d)> " % (e, len(lst))

        num = 0
        for v in lst:
            if v[2] > threshold:
                num += 1
            s += "(%s, %s, %d, %s), " % (v[0], v[1], v[2], v[3])
        s += ">> %d " % num
        if num <= 1:
            continue

        s += "(%.2f%%) " % (num / len(lst) * 100)
        s = s[0:-1]

        if num == len(lst):
            print (s)
    print ("")

def main():
    if len(sys.argv) != 2:
        usage()

    fname = sys.argv[1]
    sym = top_ids(fname, 30, SYM)
    print_result(sym, 30, SYM)
    anti = top_ids(fname, 30, ANTI)
    print_result(anti, 30, ANTI)

if __name__ == "__main__":
    main()
