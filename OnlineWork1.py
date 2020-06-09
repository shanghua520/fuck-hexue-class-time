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


def SaveObjectQuestion(Id, data):
    reps = requests.post('http://api.hnscen.cn/mobile/api/SaveObjectQuestion', {'Id': Id, 'data': str(data)})


def SaveWork(Id, data, CourseOpenId, PaperId):
    reps = requests.post('http://api.hnscen.cn/mobile/api/SaveWork',
                         {'Id': Id, 'data': str(data), 'Type': 2, 'CourseOpenId': CourseOpenId, 'IsSubmitWithoutAll': 1,
                          'PaperId': PaperId})
    return reps


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
    index = int(input())
    for windex in range(index, len(Course['course'])):
        courseOpenId = Course['course'][windex]['courseOpenId']
        homeworkList = GetHomeworkList(auth, courseOpenId)
        for index, i in enumerate(homeworkList['data']):
            print(index, '作业名称：' + i['Name'])
            # print('请选择作业：')
            # index = int(input())
            print(homeworkList['data'][index]['Id'])
            homeworkId = homeworkList['data'][index]['Id']
            print(homeworkId)
            homeworkInfo = GetHomeworkInfo(auth, homeworkId)
            print(logininfo['userId'])
            homeworkContext = getPaper(logininfo['userId'], homeworkId)
            PaperId = homeworkContext['Paper']['Id']
            PaperPaperId = homeworkContext['Paper']['PaperId']
            data = []
            for index, i in enumerate(homeworkContext['Paper']['BigQuestions']):
                print(i['Title'])
                for index1, j in enumerate(i['StuQuestions']):
                    AnswerRes = {
                        "Bindex": index,
                        "Qindex": index1,
                        "StuAnswer": j['Answer'],
                        "IsAssignmented": 1
                    }
                    SaveObjectQuestion(PaperId, AnswerRes)
                    data.append(AnswerRes)
            print(SaveWork(PaperId, data, courseOpenId, PaperPaperId).text)
