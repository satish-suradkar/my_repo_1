#!/usr/bin/python
"""This script prompts a user to enter a file name or director
name to count the frequency of character and word"""

import sys

def get_file(filename):
    """file read"""
    print filename

def main():
    """main function"""
    filename = sys.argv[1]
    get_file(filename)

if __name__ == "__main__":
    main()
