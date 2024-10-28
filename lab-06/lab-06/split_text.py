#!/usr/bin/env python3

import sys

def main():

    # Write your code here.  Refer to the hints provided
    # in the lab PDF.
    if(len(sys.argv) != 2):
        print('usage: ./split_text.py [string]')
    else:
        str = sys.argv[1]
        words = str.split(',')
        
        for w in words:
            print(w)
        
if __name__ == "__main__":
    main()
