#!/usr/bin/python
"""This script prompts a user to enter a file name or director
name to count the frequency of character and word"""
import logging
import os
import argparse
import re
import json
import subprocess
from collections import defaultdict


FINAL_DICT = defaultdict(dict)
JSON_VAR = ""


def get_file(filename):
    """file get"""
    logging.info(" in get_file() ")
    #print os.path.abspath(filename)
    if not os.path.exists(filename):
        logging.info("{} file not found ".format(filename))
        exit()
    if os.path.isfile(filename):
        read_file(filename)
    if os.path.isdir(filename):
        read_dir(filename)
    logging.info(" out get_file() ")


def read_dir(path):
    """reading files from directory """
    for sub_dir in os.listdir(path):
        file_path = os.path.join(path, sub_dir)
        if os.path.isdir(file_path):
            read_dir(file_path)
        else:
            read_file(file_path)


def read_file(filename):
    """read file"""
    #ftype = os.popen("file {}".format(filename)).read()
    ftype = subprocess.check_output(['file','{}'.format(filename)])
    #print filename, " ", ftype
    if re.search(r"ASCII text", str(ftype)):
        logging.info("in read_file()")
        count_word_dict = dict()
        count_char_dict = dict()
        text_file = open(filename)
        line_list = text_file.read().splitlines()
        for line in line_list:
            word_list = line.split()
            for word in word_list:
                if word in count_word_dict:
                    count_word_dict[word] += 1
                    for char in word:
                        if char in count_char_dict:
                            count_char_dict[char] += 1
                        else:
                            count_char_dict[char] = 1
                else:
                    count_word_dict[word] = 1
                    for char in word:
                        if char in count_char_dict:
                            count_char_dict[char] += 1
                        else:
                            count_char_dict[char] = 1
        if JSON_VAR:
            FINAL_DICT[filename]['words'] = count_word_dict
            FINAL_DICT[filename]['character'] = count_char_dict
        else:
            print "#### fileName : \n", filename
            print "#### Words    : \n", count_word_dict
            print "#### Character: \n", count_char_dict
    else:
        logging.info("{} file is not text file".format(filename))
    logging.info("out read_file()")


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file or directory name to count frequency of words and character")
    parser.add_argument("--log", help="it's a logger", choices=["INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"], default='INFO')
    parser.add_argument("--format", help="to get in json", choices=["text", "json"], default='text')
    args = parser.parse_args()
    loglevel = args.log
    file_name = args.filename
    global JSON_VAR
    JSON_VAR = args.format
    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(filemode='w', level=numeric_level)
    logging.info("started main program")
    if JSON_VAR and "JSON" != JSON_VAR.upper():
        JSON_VAR = 0
    get_file(file_name)
    if JSON_VAR:
        with open('result.json', 'w') as readj:
            json.dump(FINAL_DICT, readj)

        with open('result.json', 'r') as readj:
            final_dict1 = json.dumps(json.load(readj))
        print final_dict1
    logging.info("finished main program")


if __name__ == "__main__":
    main()




