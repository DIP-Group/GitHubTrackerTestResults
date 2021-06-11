# -*- coding: utf-8 -*-

# -- Sheet --

# System testing

import csv
import pytest
import pickle
from github import Github

def systemTest():
    with open('OutputMetrics.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    for line in data:
        for element in line:
            if(element=='NULL'):
                print("Test Failed")
                print("OutputMetrics has a NULL value")
                return False
    print("Test Passed")
    return True

def systemTest2():
    with open('OutputAnswers.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    for line in data:
        for element in line:
            if(element=='NULL'):
                print("Test Failed")
                print("OutputAnswers has a NULL value")
                return False
    print("Test Passed")
    return True

def parse_url(url):
    new_url = url
    repo_url = new_url.split('/')
    if (len(repo_url) < 5 or len(repo_url) > 5):
        raise (Exception("Sorry, İnvalid Url PLease enter the url of the main github page..."))
    repo_url = repo_url[3] + '/' + repo_url[4]
    return repo_url

def load_repo_from_file(file):
    with open(file, 'rb') as config_dictionary_file:
        # Step 3
        repo = pickle.load(config_dictionary_file)

    return repo


if __name__ == "__main__":
    print("System Test Part 1 (Metrics):")
    a = systemTest()
    print("System Test Part 2 (Questions):")
    b = systemTest2()
    if a==True and b==True:
        print("System Test is succeeded!")
    else:
        print("System Test is failed!")



