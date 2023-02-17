# Python code to serially count and display top 10 words
import os

counter = {}
for file in os.listdir("data"):
    if file.endswith('.txt'):
        with open(os.path.join('data', file), "r") as text:
            words = text.read().split()
            for word in words:
                if word in counter:
                    counter[word] += 1
                else:
                    counter[word] = 1
                    
counter = sorted(counter.items(), reverse=True, key = lambda x : x[1])
for i in range(min(len(counter), 10)):
    print(f"{counter[i][0]} : {counter[i][1]}")
'''
xpending
xautoclaim
xack
'''