#! /usr/bin/env python3

import sys, csv

def main():
    
    #  Read the words from sys.stdin
    #  Keep only the unique words
    #  Print them in sorted order.
    
    
     
    inp = sys.stdin.read()
    lines = inp.splitlines()
    arr = []
    for line in lines:
        words = line.split(',')
        for w in words:
            if w not in arr:
                arr.append(w)
    arr.sort()
    for w in arr:
        print(w)

if __name__ == "__main__":
    main()
