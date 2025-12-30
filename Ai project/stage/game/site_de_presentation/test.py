#!/usr/bin/env python3

import math
import sys

def usage() :
    print("USAGE")
    print("   ./104neutrinos n a h sd")
    print("DESCRIPTION")
    print("   n\tnumber of values")
    print("   a\tarithmetic mean")
    print("   h\tharmonic mean")
    print("   sd\tstandard deviation")

def calculate(n, arithmetic, sd, value) :
    if n <= 0 :
        exit(84)
    variance = ((n - 1) * sd ** 2 + (value - arithmetic) ** 2) / n
    std_deviation = math.sqrt(variance)
    return std_deviation

def root_mean(n, new_n, a, value, sd) :
    den = n * (pow(sd, 2) + pow(a, 2)) + pow(value, 2)
    if new_n == 0:
        exit(84)
    root_1 = den / new_n
    root = math.sqrt(root_1)
    return root

def harmonic(h, new_n, value, n) :
    if new_n == 0:
        exit(84)
    res_1 = n / h
    res_2 = res_1 + (1 / value)
    res = new_n / res_2
    return res

def function(n, a, h, sd) :
    if n <= 0 :
        exit(84)
    new_n = n 
    while True :
        value = input("Enter next value: ")
        if value == "END":
            exit(0)
        try:
            value = float(value)
        except ValueError:
            exit(84)

        if value <= 0 :
            exit(84)

        sd = calculate(new_n, a, sd, value) 
        root = root_mean(new_n, new_n + 1, a, value, sd)
        arithmetic = ((a * new_n) + value) / (new_n + 1)
        harm = harmonic(h, new_n + 1, value, new_n)
        h = harm
        a = arithmetic
        new_n += 1

        print(f"    Number of values:\t{new_n:.0f}")
        print(f"    Standard deviation:\t{sd:.2f}")
        print(f"    Arithmetic mean:\t{arithmetic:.2f}")
        print(f"    Root mean square:\t{root:.2f}")
        print(f"    Harmonic mean:\t{harm:.2f}\n")

def main() :
    if len(sys.argv) == 2 :
        if sys.argv[1] == "-h" :
            usage()
    else:
        if len(sys.argv) == 5:
            try:
                n = int(sys.argv[1])
                a = float(sys.argv[2])
                h = float(sys.argv[3])
                sd = float(sys.argv[4])
                if n <= 0:
                    exit(84)
                function(n, a, h, sd)
            except ValueError:
                exit(84)
        else:
            exit(84)

if __name__ == "__main__" :
    main()