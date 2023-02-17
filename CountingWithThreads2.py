import pathlib
from multiprocessing import Pool
from collections import Counter


def word_count_map(file):
	wc = {}
	with open(file, mode='r', newline='\r') as f:
		words = f.read().split()
		wc = Counter(words)
	return wc

if __name__ == '__main__':
    wc_final = {}
    with Pool(1) as mexecutor:
        items = [f for f in pathlib.Path('text/').glob("*.txt")]
        for wc in mexecutor.imap_unordered(word_count_map, items):
            for w in wc:
                wc_final[w] = wc_final.get(w, 0) + wc[w]
    wc_final = sorted(wc_final.items(), key = lambda x : x[1], reverse=True)
    for i in range(min(10, len(wc_final))):
        print(f"{wc_final[i][0]} : {wc_final[i][1]}")