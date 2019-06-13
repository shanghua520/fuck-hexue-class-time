import json
import time
import requests

import main


# 获取某个课的作业列表
def GetHomeworkList(auth, courseOpenId):
    reps = requests.post('http://api.hnscen.cn/mobile/api/GetHomeworkList',
                         {'auth_fix': auth, 'courseOpenId': courseOpenId}).text
    print(reps)
    homeworklistInfo = json.loads(reps)
    return homeworklistInfo


# 获取作业详情
def GetHomeworkInfo(auth, homeworkId):
    reps = requests.post('http://api.hnscen.cn/mobile/api/GetHomeworkInfo',
                         {'auth_fix': auth, 'homeworkId': homeworkId}).text
    homeworkInfo = json.loads(reps)
    return homeworkInfo


# 获取作业信息
def getPaper(UserId, WorkId):
    print(WorkId)
    reps = requests.get(
        'http://api.hnscen.cn/mobile/api/getPaper', params={'UserId': UserId, 'WorkId': WorkId}).text
    homeworkContextInfo = json.loads(reps)
    return homeworkContextInfo


def SplicingAnswer(answer):
    strAnswer = ''
    for i in answer:
        if i == '0':
            strAnswer += 'A'
        if i == '1':
            strAnswer += 'B'
        if i == '2':
            strAnswer += 'C'
        if i == '3':
            strAnswer += 'D'
    return strAnswer


if __name__ == "__main__":
    # 获取登陆返回的信息
    logininfo = main.login('username', 'password', None)
    time.sleep(0.1)
    # auth好像比较重要，每个方法都基本上用到了
    print(logininfo)
    auth = logininfo['auth']
    main.getuserinfo(auth)
    # 获取所有的课
    Course = main.MyCourse(auth)
    time.sleep(0.1)
    print('课程列表-----------------------')
    for index, i in enumerate(Course['course']):
        print(index, ':课程名字：' + i['name'] + '  进度：' + str(i['process']) + '%')
    print('请选择课程：')
    index = input()
    homeworkList = GetHomeworkList(auth, Course['course'][int(index)]['courseOpenId'])
    for index, i in enumerate(homeworkList['data']):
        print(index, '作业名称：' + i['Name'])
    print('请选择作业：')
    index = input()
    print(homeworkList['data'][int(index)]['Id'])
    homeworkId = homeworkList['data'][int(index)]['Id']
    homeworkInfo = GetHomeworkInfo(auth, homeworkId)
    print(homeworkInfo)
    print(logininfo['userId'])
    homeworkContext = getPaper(logininfo['userId'], homeworkId)
    print(homeworkContext)
    for index, i in enumerate(homeworkContext['Paper']['BigQuestions']):
        print(i['Title'])
        title = i['Title']
        for index1, j in enumerate(i['StuQuestions']):
            if title == '判断题':
                answer = 'A' if j['Answer'] == '1' else 'B'
                print('判断题目：' + j['Title'] + ' 答案：' + answer)
            if title == '单选题':
                answer = j['Answer']
                if answer == '0':
                    answer = 'A'
                if answer == '1':
                    answer = 'B'
                if answer == '2':
                    answer = 'C'
                if answer == '3':
                    answer = 'D'
                print('单选题目：' + j['Title'] + ' 答案：' + answer)
            if title == '多选题':
                answer = j['Answer']
                lisAnswer = str(answer).split(',')
                print('多选题目：' + j['Title'] + ' 答案：' + SplicingAnswer(lisAnswer))
