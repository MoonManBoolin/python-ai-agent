#!/usr/bin/env python

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


def tests():
    print("----------------TESTING FILE_INFO FUNCTIONS----------------")
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
    print("----------------TESTING FILE_CONTENT FUNCTIONS----------------")
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print("----------------TESTING LORUM IPSUM FILE----------------")
    print(get_file_content("calculator", "lorem.txt"))
tests()