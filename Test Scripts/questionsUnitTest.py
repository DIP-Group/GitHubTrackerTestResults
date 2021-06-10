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

questions_list = ["Are labels used for issue management?",
                    "Is the default set of labels sufficient for issue management?",
                    "Is every contributor active in issue management?",
                    "Is the responsibility of opening and closing issues equally distributed among contributors?",
                    "Are the life times of the issues consistent?",
                    "Are the comments made by the contributors equally distributed among contributors?",
                    "Is commenting used consistently in all issues?",
                    "Are the issues with assigneee completed earlier to compared the ones without assignee?",
                    "What is the ratio of the opened issues grouped under milestone and those not grouped?",
                    "What does the average time between opening and closing the issue?",
                    "What does the average time between opening and closing the milestone?",
                    "Are the comments be posted after the issues are closed or during the process?",
                    "Are the issues grouped under milestone completed earlier compared to the ones not grouped?"]

selectionArray=questions_list
answers_list=[]
def calculate_questions(Repo):
    global selectionArray
    
    global answers_list
    answers_list = []

    open_issues = Repo.get_issues(state = "open")
    closed_issues = Repo.get_issues(state = "closed")

    for item in selectionArray:
        if (item == "Are labels used for issue management?"):
            labelName = []
            labelCount = 0
            Total_open_issues=[]
            Total_closed_issues=[]
            for issue in open_issues:
                Total_open_issues.append(issue)
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            
            total_issues = Total_open_issues + Total_closed_issues

            for issue in total_issues:
                total_labels = issue.get_labels()
                for label in total_labels:
                    if(label != None):
                        labelCount += 1
            totalIssues = len(total_issues)
            control = totalIssues/2

            if labelCount >= control:
                answer = "Yes, labels are important for this repository."
                answers_list.append([item, "Yes"])
            else:
                answer = "No, labels are NOT important for this repository."
                answers_list.append([item, "No"])

        elif (item == "Is the default set of labels sufficient for issue management?"):
            control = 0
            defaultLableSet = ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"]
            labelName = []
            for label in Repo.get_labels():
                labelName.append(label.name)
            for tempLabel in labelName:
                if tempLabel not in defaultLableSet:
                    control = control + 1
 
            if control > 0:
                answer = "No, default set of labels is NOT sufficient for issue management"
                answers_list.append([item, "No"])
            else:
                answer = "Yes, default set of labels is sufficient for issue management"
                answers_list.append([item, "Yes"])

        
        elif (item == "Is every contributor active in issue management?"):
            
            open_issue_comment_writer = []
            open_issue_contributors = []
            closed_issue_comment_writer = []
            closed_issue_contributors = []
            all_issue_comment_writer = []
            all_issue_contributors = []
            
            
            for issue in open_issues:
                for comment in issue.get_comments():
                    open_issue_comment_writer.append(comment.user.login)
            
            for issue in open_issues:
                open_issue_contributors.append(issue.user.login)
                
            for issue in closed_issues:
                for comment in issue.get_comments():
                    closed_issue_comment_writer.append(comment.user.login)
            
            for issue in closed_issues:
                open_issue_contributors.append(issue.user.login)
                
            all_issue_comment_writer.extend(open_issue_comment_writer)    
            all_issue_comment_writer.extend(closed_issue_comment_writer)
            all_issue_contributors.extend(open_issue_contributors)
            all_issue_contributors.extend(closed_issue_contributors)
            answer = ""
            for i in all_issue_contributors:
                flag = 0
                for j in all_issue_comment_writer:
                    if(i==j):
                        flag=1
                if(flag==0):
                    answer = "No, not every contributor active in issue management"
                    answers_list.append([item, "No"])
                    break
                    
            if(answer==""):
                answer = "Yes, every contributor active in issue management"
                answers_list.append([item, "Yes"])

        elif (item == "Is the responsibility of opening and closing issues equally distributed among contributors?"):#buna bir bakalım
            open_issue_openers = []
            closed_issue_openers = []
            all_issue_openers = []
            open_issue_closers = []
            closed_issue_closers = []
            all_issue_closers = []
            all_issue_openers_and_closers = []
            #issue openers
            for issue in open_issues:
                open_issue_openers.append(issue.user.login)

            for issue in closed_issues:
                closed_issue_openers.append(issue.user.login)
               
            all_issue_openers.extend(open_issue_openers)
            all_issue_openers.extend(closed_issue_openers)
            total_opening_an_issue = len(all_issue_openers)
            unique_list = []
            for x in all_issue_openers:
                if x not in unique_list:
                    unique_list.append(x)
                    
            #issue closers    
            for issue in open_issues:
                if(issue.closed_by!=None):
                    open_issue_closers.append(issue.closed_by.login)

            for issue in closed_issues:
                if(issue.closed_by!=None):
                    closed_issue_closers.append(issue.closed_by.login)
               
            all_issue_closers.extend(open_issue_closers)
            all_issue_closers.extend(closed_issue_closers)
            total_closing_an_issue = len(all_issue_closers)
            for x in all_issue_closers:
                if x not in unique_list:
                    unique_list.append(x)        
                    
            
            number_of_contributors = len(unique_list)
            
            all_issue_openers_and_closers.extend(all_issue_openers)
            all_issue_openers_and_closers.extend(all_issue_closers)
            
            distribution_of_opening_and_closing_issue = (total_opening_an_issue+total_closing_an_issue) / number_of_contributors
            
            for contributor in unique_list:
                contribution_count = all_issue_openers_and_closers.count(contributor)
                if(((contribution_count-distribution_of_opening_and_closing_issue)<2) and ((distribution_of_opening_and_closing_issue-contribution_count)<2)):
                    answer = "Yes,the responsibility of opening and closing issues is equally distributed among contributors"
                else:
                    answer = "No,the responsibility of opening and closing issues is NOT equally distributed among contributors" 
                    break
            if(answer=="Yes,the responsibility of opening and closing issues is equally distributed among contributors"):
                answers_list.append([item, "Yes"])
            elif(answer=="No,the responsibility of opening and closing issues is NOT equally distributed among contributors" ):
                answers_list.append([item, "No"])  
            

        elif (item == "Are the life times of the issues consistent?"):
            issues=[]
            duration_list=[]
            for issue in closed_issues:
                created = issue.created_at
                closed = issue.closed_at
                duration = closed - created
                duration_list.append(duration)
            Mean_duration=0
            for x in duration_list:
                Mean_duration = Mean_duration + x.days
            Mean_duration = Mean_duration/len(duration_list)

            lower_bound = Mean_duration-7
            if(lower_bound<0):
                lower_bound=0
            upper_bound = Mean_duration +7

            count=0
            for i in duration_list:
                if (float(i.days)>=lower_bound and float(i.days)<=upper_bound):
                    count = count +1
            lenght = len(duration_list)

            
            if ((count/lenght)>=0.8):
                answer = "Yes, life times of the issues are consistent for this Repo"
                answers_list.append([item, "Yes"])
            else:
                answer = "No, life times of the issues are not consistent for this Repo"
                answers_list.append([item, "No"])

        elif (item == "Are the comments made by the contributors equally distributed among contributors?"):

            open_issue_contributors = []
            closed_issue_contributors = []
            all_issue_contributors = []
            opened_issues_total_comments=0
            closed_issues_total_comments=0
            number_of_total_comment=0

            for issue in open_issues:
                opened_issues_total_comments = opened_issues_total_comments + issue.comments
                
            for issue in closed_issues:
                closed_issues_total_comments = closed_issues_total_comments + issue.comments
                
            number_of_total_comment =  opened_issues_total_comments + closed_issues_total_comments
            
            for issue in open_issues:
                open_issue_contributors.append(issue.user.login)
            
            for issue in closed_issues:
                open_issue_contributors.append(issue.user.login)
                
            all_issue_contributors.extend(open_issue_contributors)
            all_issue_contributors.extend(closed_issue_contributors)
            
            unique_list = []
            for x in all_issue_contributors:
                if x not in unique_list:
                    unique_list.append(x)
            
            number_of_contributors = len(unique_list)
            
            distribution_of_comments = number_of_total_comment/number_of_contributors
            
            open_issue_comment_writer = []
            closed_issue_comment_writer = []
            all_issue_comment_writer = []
            
            
            for issue in open_issues:
                for comment in issue.get_comments():
                    open_issue_comment_writer.append(comment.user.login)
            
                
            for issue in closed_issues:
                for comment in issue.get_comments():
                    closed_issue_comment_writer.append(comment.user.login)

                
            all_issue_comment_writer.extend(open_issue_comment_writer)    
            all_issue_comment_writer.extend(closed_issue_comment_writer)
            answer=""
            
            for writer in all_issue_comment_writer:
                count = 0
                for ele in all_issue_comment_writer:
                    if (ele == writer):
                        count = count + 1
                count = count - 1
                if(distribution_of_comments!=count):
                    answer = "No,the comments made by the contributors NOT equally distributed among contributors"
                    answers_list.append([item, "No"])
                    break
                if(answer!=""):
                    break
            
            if(answer==""):
                answer = "Yes,the comments made by the contributors equally distributed among contributors"
                answers_list.append([item, "Yes"])
                    
        
        elif (item == "Is commenting used consistently in all issues?"):
            check = 0

            for i in open_issues:
                if(i.comments == 0):
                    check = 1
            if(check ==1 ):
                answer = "No, commenting is NOT used consistently in all issues"
                answers_list.append([item, "No"])
            else:
                for i in closed_issues:
                    if(i.comments == 0):
                        check = 1
        
                if(check ==1 ):
                    answer = "No, commenting is NOT used consistently in all issues"
                    answers_list.append([item, "NO"])
                else:
                    answer = "Yes, commenting is used consistently in all issues"
                    answers_list.append([item, "Yes"])
            

        elif (item == "Are the issues with assigneee completed earlier to compared the ones without assignee?"):
            issue_number=0
            with_assignee=0
            without_assignee=0
            without_assignee_time=0
            with_assignee_time=0
            total_issues = []
            for i in closed_issues:
                issue_number+=1
                if(i.assignee == None):
                    without_assignee +=1
                    
                    without_assignee_time += (i.closed_at.timestamp() - i.created_at.timestamp())
                else:
                    with_assignee +=1
                    with_assignee_time += i.closed_at.timestamp() - i.created_at.timestamp()
            
            average_with_assignee = with_assignee_time / with_assignee
            average_without_assignee = without_assignee_time / without_assignee
            
            if(average_with_assignee > average_without_assignee):
                answer = "No, issues without assignees has been completed earlier"
                answers_list.append([item, "No"])
            else:
                answer = "Yes, issues with assignees has been completed earlier"
                answers_list.append([item, "Yes"])


        elif (item == "What is the ratio of the opened issues grouped under milestone and those not grouped?"):
            open_issue_number = 0
            with_milestone_number = 0
            without_milestone_nnumber = 0
            
            open_issues_milestone_none = Repo.get_issues(state="open",milestone="none")
            
            for i in open_issues:
                open_issue_number +=1 
            for i in open_issues_milestone_none:
                without_milestone_nnumber +=1
            with_milestone_number = open_issue_number - without_milestone_nnumber
            if(without_milestone_nnumber == 0 and with_milestone_number !=0):
                percentage = 100
            if(without_milestone_nnumber == 0 and with_milestone_number ==0):
                percentage = 0
            if(without_milestone_nnumber != 0):    
                percentage = (with_milestone_number / without_milestone_nnumber) * 100

            answers_list.append([item, percentage])


        elif (item == "What does the average time between opening and closing the issue?"):
            Total_closed_issues=[]
            duration = []
            Avg_duration = 0
            for issue in closed_issues:
                Total_closed_issues.append(issue)
            for issue in Total_closed_issues:
                opened = issue.created_at
                closed = issue.closed_at
                temp_duration = closed - opened
                duration.append(temp_duration)
            for x in duration:
                Avg_duration = Avg_duration + x.days
            Avg_duration = Avg_duration/len(Total_closed_issues)
            
            answers_list.append([item, Avg_duration])

        elif (item == "What does the average time between opening and closing the milestone?"):
            Total_closed_milestones=[]
            duration = []
            closed_milestones = Repo.get_milestones(state='closed')
            Avg_duration = 0
            for milestone in closed_milestones:
                Total_closed_milestones.append(milestone)
            for issue in Total_closed_milestones:
                opened = milestone.created_at
                closed = milestone.due_on
                temp_duration = closed - opened
                duration.append(temp_duration)
            for x in duration:
                Avg_duration = Avg_duration + x.days
            Avg_duration = Avg_duration/len(Total_closed_milestones)

            answers_list.append([item, Avg_duration])


        elif (item == "Are the comments be posted after the issues are closed or during the process?"):
            open_total_comments = 0
            before_closed_comments = 0
            after_closed_comments = 0
            for issue in open_issues:
                comments = issue.comments
                open_total_comments += comments
            for issue in closed_issues:
                total_closed_comments = issue.comments
                comments2 = issue.get_comments(since=issue.closed_at)
                for comment in comments2:
                    after_closed_comments += len(comment)
                    before_closed_comments += (total_closed_comments - after_closed_comments)

            before_closed_comments += open_total_comments

            if(before_closed_comments >= after_closed_comments):
                answer = "No, the comments are generally posted during the process for this Repo."
                answers_list.append([item, "No"])
            else:
                answer = "Yes, the comments are generally posted after the issues are closed for this Repo."
                answers_list.append([item, "Yes"])


        elif (item == "Are the issues grouped under milestone completed earlier compared to the ones not grouped?"):
            Total_milestones=[]
            Total_Issues=[]
            grouped = []
            notgrouped = []

            opened_milestones = Repo.get_milestones(state='open')
            closed_milestones = Repo.get_milestones(state='closed')

            for milestone in opened_milestones:
                Total_milestones.append(milestone)
            for milestone in closed_milestones:
                Total_milestones.append(milestone)

            for issue in closed_issues:
                Total_Issues.append(issue)
            
            for issue in Total_Issues:
                if issue.milestone in Total_milestones:
                    grouped.append(issue)
                else:
                    notgrouped.append(issue)

            grouped_time = 0
            notgrouped_time = 0

            for elem in grouped:
                opened = elem.created_at
                closed = elem.closed_at
                temp_duration = closed - opened
                grouped_time += temp_duration.days
            grouped_time = grouped_time / len(grouped)

            for elem in notgrouped:
                opened = elem.created_at
                closed = elem.closed_at
                temp_duration = closed - opened
                notgrouped_time += temp_duration.days
            notgrouped_time = notgrouped_time / len(notgrouped)

            if(grouped_time >= notgrouped_time):
                answer = "Yes, the issues grouped under milestone completed earlier compared to the ones not grouped."
                answers_list.append([item, "Yes"])
            else:
                answer = "No, the issues not grouped under milestone completed earlier compared to the ones grouped."
                answers_list.append([item, "No"])

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
    get_repo_test("https://github.com/DIP-Group/GithubTracker")

    repo=load_repo_from_file("GithubTracker.pkl")

    testResult=[]
    calculate_questions(repo)
    testResult.append(Test_Function(0,str,"No"))
    testResult.append(Test_Function(1,str,"Yes"))
    testResult.append(Test_Function(2,str,"No"))
    testResult.append(Test_Function(3,str,"No"))
    testResult.append(Test_Function(4,str,"No"))
    testResult.append(Test_Function(5,str,"No"))
    testResult.append(Test_Function(6,str,"No"))
    testResult.append(Test_Function(7,str,"No"))
    testResult.append(Test_Function(8,int,100))
    testResult.append(Test_Function(9,float,36.0))
    testResult.append(Test_Function(10,float,7.0))
    testResult.append(Test_Function(11,str,"No"))
    testResult.append(Test_Function(12,str,"Yes"))

    counter = 1
    for element in testResult:
        print("Question Calculation {}:".format(counter))
        if(element):
            print("Test Success")
        else:
            print("Test Failed")
        counter += 1



