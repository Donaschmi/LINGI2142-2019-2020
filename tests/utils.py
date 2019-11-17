#!/usr/bin/env python3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_results(succeed, failed, nbre):
    ratio = (succeed / (succeed + failed)) * 100
    print("Ran ping test for", nbre, "routers :")
    print("Success : " , succeed)
    print("Fail : " , failed)
    print("Ratio : " , ratio , "%")

def trim_from_start(text, char):
    for i in range(0, len(text)):
        if text[i] == char:
            return text[i:]
    return text

def trim_from_end(text, char):
    str_len = len(text)
    j = 0
    for i in range(str_len - 1, -1, -1):
        if text[i] == char:
            return text[:-j]
        j += 1

    return text
