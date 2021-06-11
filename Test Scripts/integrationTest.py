# -*- coding: utf-8 -*-

# -- Sheet --

# System testing
import csv
import pytest
import pickle
from github import Github

def parse_url(url):
    new_url = url
    repo_url = new_url.split('/')
    if (len(repo_url) < 5 or len(repo_url) > 5):
        raise (Exception("Sorry, İnvalid Url PLease enter the url of the main github page..."))
    repo_url = repo_url[3] + '/' + repo_url[4]
    return repo_url

def load_repo_from_file(file):
    with open(file, 'rb') as config_dictionary_file:
        repo = pickle.load(config_dictionary_file)
    return repo

def get_repo_test(url):
    new_url=parse_url(url)
    github = Github()
    repo = github.get_repo(new_url)
    if(repo==None):
        print("Integration Test Failed")
    if(repo):
        print("Integration Test Successfull")
    name=repo.name
    name = str(name)
    with open(name+'.pkl', 'wb') as output:
        pickle.dump(repo, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    get_repo_test("https://github.com/DIP-Group/GithubTracker")



