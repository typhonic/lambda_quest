#! /usr/bin/env python
"""
open one text file
get a list of modules
"""
import re
import codecs


def main():
    # initialization
    filepath = './'
    filename = 'snippet'
    print 'reading', filename
    lines = read_file(filepath + filename)
    modules = get_module_list(lines)
    print 'found', len(modules), 'modules'


def read_file(filename):
    # read the file - watchout for unicode
    openfile = codecs.open(filename, encoding='UTF-16-LE',
                           mode='r', errors='strict')
    lines = openfile.readlines()
    openfile.close()
    return lines


def get_module_list(lines):
    # get a list from the text file
    # each element of the list is a list of a module definition
    # the first element of the list is the tagname
    # the remaining elements are the lines of the definition
    temp_module = []
    temp_modules = []
    open_bracket_count = 0
    closed_bracket_count = 0
    for line in lines:
        #count the brackets {}
        open_bracket_count = open_bracket_count + len(re.findall('{', line))
        closed_bracket_count = closed_bracket_count + \
                               len(re.findall('}', line))
        module_start = re.search('MODULE TAG="([-\w]+)"', line)
        if module_start:
            # start a new object
            open_bracket_count = 0
            closed_bracket_count = 0
            temp_module = []
            temp_module.append(module_start.group(1))
            temp_module.append(line.rstrip())
        elif len(temp_module) > 0:
            temp_module.append(line.rstrip())
        if open_bracket_count > 0 and \
           open_bracket_count == closed_bracket_count and \
           len(temp_module) > 0:
            temp_modules.append(temp_module)
            # reinitialize these for the next go round
            temp_module = []
            open_bracket_count = 0
            closed_bracket_count = 0
    return temp_modules

main()
