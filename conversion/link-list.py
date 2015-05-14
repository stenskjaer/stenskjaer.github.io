#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import csv

def __main__():
    try:
        dir = sys.argv[1]
    except IndexError:
        exit("Out of range. Input the directory")

    slide_dir = "slides/echo/"
    files_and_titles = []
    for f in os.listdir(dir):
        clean_name = os.path.basename(f)[:-4]
        filename = os.path.join(slide_dir, clean_name) + ".html"
        if f.endswith('.csv'):
            with open(os.path.join(dir, f)) as f:
                reader = csv.reader(f)
                title = reader.next()[0].replace('--', '–')
        else:
            title = f

        files_and_titles.append((filename, title))

    # Here we start the list
    print("<ul>")
    for file, title in files_and_titles:
        print("    <li><a href=\"{0}\">{1}</a></li>".format(file, title))
    print("</ul>")

if __name__ == "__main__":
    __main__()

