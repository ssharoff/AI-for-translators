import collections
import requests
import math
import re
try:
    from google.colab import drive
    gdrive="/content/corpus/"
    drive.mount(gdrive)
except:
    gdrive="."

dirname = gdrive+"/MyDrive/corpus-en/"

def processfile(fname):
    file_count = 0
    for sentence in open(fname).readlines():
        for word in sentence.split(" "):
            file_count += 1
            word = re.sub("[^a-z-]+","",word)
            dictionary[word] += 1
    return file_count

corpus_count = 0
dictionary = collections.defaultdict(int)

file_count = processfile(fname)
print(f"{file_count} words in {fname}")
    corpus_count += file_count

reference=requests.get("https://sshharoff.github.io/frqc/bnc-clean2.tsv").text
reference_dict = {}
d_count=0
for l in reference.split("\n"):
    values = l.split("\t")
    if len(values)>4:
        (word,frqraw,frqrobust,frqcap,frqdoc)=values
        d_count += int(frqraw)
        if not word in reference_dict:
            reference_dict[word] = int(frqrobust)

def keyness(a,b,c,d):
    ll = 0
    if a/c > b/d: # b/d is the reference corpus, we are not interested in overuse there
        e1 = c*(a+b)/(c+d)
        e2 = d*(a+b)/(c+d)
        ll = 2*((a*math.log(a/e1))+(b*math.log(b/e2)))
    return ll

kewords={}
threshold=10.83
for word in dictionary:
    if word in reference_dict:
        ll = keyness(dictionary[word],reference_dict[word],corpus_count,d_count)
        if ll>threshold:
            ipm1 = 1e6 * dictionary[word]/corpus_count
            ipm2 = 1e6 * reference_dict[word]/d_count
            print(f"{word}\t{ipm1:.2f}\t{ipm2:.2f}\t{ll:.2f}")

