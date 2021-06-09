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
        raise (Exception("Sorry, Invalid Url Please enter the url of the main github page..."))
    repo_url = repo_url[3] + '/' + repo_url[4]
    return repo_url

def load_repo_from_file(file):
    with open(file, 'rb') as config_dictionary_file:
        # Step 3
        repo = pickle.load(config_dictionary_file)

    return repo

def get_repo_test(url):
    new_url=parse_url(url)
    github = Github()

    repo = github.get_repo(new_url)

    name=repo.name
    name = str(name)

    with open(name+'.pkl', 'wb') as output:
        pickle.dump(repo, output, pickle.HIGHEST_PROTOCOL)

import statistics

main_list = ["Total Opened Issues", "Total Closed Issues", "Difference between opened and closed issues",
                 "Distribution score of issues on contributors", "Number of label types", "Label usage frequency",
                 "Total amount of contributors", "Total number of assignees on specific Repo",
                 "Total number of comments", "Avg. Comment Length", "Total number of used labels",
                 "Mean time to response the issues.", "Total amount of Milestones", "Total Opened Milestones",
                 "Total Closed Milestones"]

# Answer için değiştirlecek
selectionArray=main_list
answers_list=[]
def calculate_metrics(Repo):
    global selectionArray
    global answers_list


    for item in selectionArray:
        if (item == "Total Opened Issues"):
            Total_open_issues=[]
            open_issues = Repo.get_issues(state='open')
            for issue in open_issues:
                Total_open_issues.append(issue.title)
            
            answers_list.append([item, len(Total_open_issues)])
        
        elif (item == "Total Closed Issues"):
            Total_closed_issues=[]
            closed_issues = Repo.get_issues(state='closed')
            for issue in closed_issues:
                Total_closed_issues.append(issue.title)
            
            answers_list.append([item, len(Total_closed_issues)])
        
        elif (item == "Difference between opened and closed issues"):
            temp = []
            Total_open_issues=[]
            Total_closed_issues=[]
            open_issues = Repo.get_issues(state='open')
            for issue in open_issues:
                Total_open_issues.append(issue)
            closed_issues = Repo.get_issues(state='closed')
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            temp = abs(len(Total_open_issues)-len(Total_closed_issues))

            answers_list.append([item, temp])

        elif (item == "Distribution score of issues on contributors"):
            contrArray = []
            openedIssueUserArray = [] 
            repo_contributors = Repo.get_contributors()
            for repo_contributor in repo_contributors:
                if (repo_contributor,0) not in contrArray:
                    contrArray.append([repo_contributor,0])
            Total_issues=[]
            open_issues = Repo.get_issues(state='open')
            for issue in open_issues:
                Total_issues.append(issue)
            closed_issues = Repo.get_issues(state='closed')
            for issue in closed_issues:
                Total_issues.append(issue)

            for issue in Total_issues:
                for cont in contrArray:
                    if(cont[0] in issue.assignees):
                        cont[1] += 1
            sample = []
            for cont in contrArray:
                sample.append(cont[1])

            stdeviation = statistics.stdev(sample)
            meann = statistics.mean(sample)
            
            result = stdeviation/meann
            answers_list.append([item, result])

        elif (item == "Number of label types"):
            control1 = 0
            control2 = 0
            defaultLableSet = ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"]
            labelName = []
            for label in Repo.get_labels():
                labelName.append(label.name)
            for tempLabel in labelName:
                if tempLabel not in defaultLableSet:
                    control1 = control1 + 1
                else:
                    control2 = control2 + 1

            answers_list.append([item, control1+control2])


        elif (item == "Label usage frequency"):
            labelName = []
            labelCount = 0
            Total_issues=[]
            open_issues = Repo.get_issues(state='open')
            for issue in open_issues:
                Total_issues.append(issue)
            closed_issues = Repo.get_issues(state='closed')
            for issue in closed_issues:
                Total_issues.append(issue)

            for issue in Total_issues:
                total_labels = issue.get_labels()
                for label in total_labels:
                    if(label != None):
                        labelCount += 1
            totalIssues = len(Total_issues)
            
            control = totalIssues/2
            answers_list.append([item, int((labelCount/totalIssues)*100)])
            
        
        elif (item == "Total amount of contributors"):
            contrArray = []
            openedIssueUserArray = [] 
            repo_contributors = Repo.get_contributors()
            for repo_contributor in repo_contributors:
                if repo_contributor.id not in contrArray:
                    contrArray.append(repo_contributor.id)
            contr_num = len(contrArray)

            answers_list.append([item, contr_num])


        elif (item == "Total number of assignees on specific Repo"):
            issues=Repo.get_issues()
            assignee = []
            for item2 in issues:
                x = item2.assignees
                for member in x:
                    assignee.append(member)
            assignee = len(list(dict.fromkeys(assignee)))

            answers_list.append([item, assignee])


        elif (item == "Total number of comments"):
            open_issues = Repo.get_issues(state='open')
            closed_issues = Repo.get_issues(state='closed')
            open_total_comments = 0
            closed_total_comments = 0
            for issue in open_issues:
                comment_no = issue.comments
                open_total_comments += comment_no
            comment_no = 0
            for issue in closed_issues:
                comment_no= issue.comments
                closed_total_comments += comment_no

            answers_list.append([item, open_total_comments + closed_total_comments])


        elif (item == "Avg. Comment Length"):
            total = 0
            temp_comment = 0
            count = 0
            labels = []
            sizes = []
            for issue in Repo.get_issues():
                comments = issue.get_comments()
                temp = 0
                counter = 0
                for comment in comments:
                    for character in comment.body:
                        temp = temp + 1
                    
                    counter = counter + 1
                    labels.append(counter)
                    sizes.append(temp)
                    
                if temp != 0:
                    temp_comment = temp_comment + temp/counter
                else:
                    temp_comment = 0
                count = count + 1
            total = temp_comment/count

            answers_list.append([item, total])


        elif (item == "Total number of used labels"):
            Total_issues = []
            labelTwins = []
            open_issues = Repo.get_issues(state='open')
            for issue in open_issues:
                Total_issues.append(issue)
            closed_issues = Repo.get_issues(state='closed')
            for issue in closed_issues:
                Total_issues.append(issue)
            for issue in Total_issues:
                labels = issue.get_labels()
                for label in labels:
                    labelTwins.append((label.name))

            answers_list.append([item, len(labelTwins)])

        # Mean time i Gün bazında hesaplıyor (Mean Response u Issue nün oluşturulduğu tarihten en son update edildiği zamana kadar alıyorum (Acaba kapatıldığı güne kadar mı alınmalı))
        elif (item == "Mean time to response the issues."):
            Total_closed_issues=[]
            response_time = []
            labels = []
            sizes = []
            closed_issues = Repo.get_issues(state='closed')
            Mean_response = 0
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            counter = 1
            for issue in Total_closed_issues:
                created=issue.created_at
                updated = issue.updated_at
                closed = issue.closed_at
                response = updated-created
                duration = closed - created
                response_time.append(response)
                labels.append(counter)
                counter += 1
            for x in response_time:
                Mean_response = Mean_response + x.days
                sizes.append(x.days)
            Mean_response = Mean_response/len(response_time)

            answers_list.append([item, Mean_response])


        elif (item == "Total amount of Milestones"):
            open_milestones = Repo.get_milestones(state='open')
            close_milestones = Repo.get_milestones(state='closed')
            open_milestones_list=[]
            closed_milestones_list = []
            for milestone in open_milestones:
                open_milestones_list.append(milestone)           
            for milestone in close_milestones:
                closed_milestones_list.append(milestone)

            answers_list.append([item, len(open_milestones_list) + len(closed_milestones_list)])

        elif (item == "Total Opened Milestones"):
            open_milestones = Repo.get_milestones(state='open')
            open_milestones_list=[]
            for milestone in open_milestones:
                open_milestones_list.append(milestone)

            answers_list.append([item, len(open_milestones_list)])

        elif (item == "Total Closed Milestones"):
            close_milestones = Repo.get_milestones(state='closed')
            closed_milestones_list = []
            for milestone in close_milestones:
                closed_milestones_list.append(milestone)

            answers_list.append([item, len(closed_milestones_list)])

        else:
            print("Error...")
        

def Test_Function(index,control_type,value):
    global answers_list

    item=answers_list[index]
    item=item[1]

    if(item):
        if(type(item)==control_type):
            if(item==value):
                pass
            else:
                return False
        else:
           return False 
    else:
        return False
    return True


if __name__ == "__main__":
    """
    systemTest()
    systemTest2()
    get_repo_test("https://github.com/DIP-Group/GithubTracker")
    """
    repo=load_repo_from_file("GithubTracker.pkl")

    #3,6,3,0.1649572197684645,9,22,4,4,2,6.666666666666667,2,52.166666666666664,4,3,1
    testResult=[]
    calculate_metrics(repo)
    testResult.append(Test_Function(0,int,3))
    testResult.append(Test_Function(1,int,6))
    testResult.append(Test_Function(2,int,3))
    testResult.append(Test_Function(3,float,0.1649572197684645))
    testResult.append(Test_Function(4,int,9))
    testResult.append(Test_Function(5,int,22))
    testResult.append(Test_Function(6,int,4))
    testResult.append(Test_Function(7,int,4))
    testResult.append(Test_Function(8,int,2))
    testResult.append(Test_Function(9,float,6.666666666666667))
    testResult.append(Test_Function(10,int,2))
    testResult.append(Test_Function(11,float,52.166666666666664))
    testResult.append(Test_Function(12,int,4))
    testResult.append(Test_Function(13,int,3))
    testResult.append(Test_Function(14,int,1))

    counter = 1
    for element in testResult:
        print("Metric Calculation {}:".format(counter))
        if(element):
            print("Test Success")
        else:
            print("Test Failed")
        counter += 1


