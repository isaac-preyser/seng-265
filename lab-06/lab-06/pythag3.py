#!/usr/bin/env python3

import sys
import math

def pythag(a=0, b=0):
    return math.sqrt(a**2 + b**2)

def main():
 
    # parse the command-line arguments
    # print an error and quit if there aren't the right number
    if (len(sys.argv) != 3):
        print("usage: ./pythag3.py a b")
        exit()
    else:
        a = sys.argv[1]
        #print(a)
        b = sys.argv[2]
        #print(b)
    # convert the command line arguments from strings to floats
    a = float(a)
    b = float(b)

    print("Sides ", a, " and ", b, ", hypotenuse ", end="", sep="")
    print("%.4f" % pythag(a, b))


if __name__ == "__main__":
    main()
