import multiprocessing
import os
from collections import Counter, defaultdict

def count_words(file):
    with open(os.path.join("text", file), "r") as wordfile:
        words = wordfile.read().split()
        print(f"Number of words in {file} is {len(words)}")
        return Counter(words)

def count_all_files():
    all_files = defaultdict(int)
    with multiprocessing.Pool() as pool:
        for data in pool.map(count_words, os.listdir('text')):
            for k, v in data.items():
                all_files[k] += v
    


if __name__ == "__main__":
    count_all_files()
