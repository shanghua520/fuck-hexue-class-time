import threading
import time
import requests
import json

mutex = threading.Lock()

logidall = []


def login(username, pwd, appId):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/login', {'username': username, "pwd": pwd}).text
    logininfo = json.loads(reps)
    return logininfo


def getuserinfo(auth_fix):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/GetUserInfo', {'auth_fix': auth_fix}).text
    userinfo = json.loads(reps)
    userinfodata = userinfo['data']
    # print(userinfodata['Name'], userinfodata['ClassName'], userinfodata['MajorName'])


def myscore(auth_fix):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/new/MyScore', {'auth_fix': auth_fix}).text
    scoreinfo = json.loads(reps)
    return scoreinfo


def MyCourse(auth_fix):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/new/MyCourse', {'auth_fix': auth_fix}).text
    Courseinfo = json.loads(reps)
    return Courseinfo


def GetCourseInfo(auth_fix, courseOpenId):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/GetCourseInfo',
                         {'auth_fix': auth_fix, 'courseOpenId': courseOpenId}).text
    CourseInfo = json.loads(reps)
    return CourseInfo


def GetCourseeProcess(auth_fix, courseOpenId):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/GetCourseeProcess',
                         {'auth_fix': auth_fix, 'courseOpenId': courseOpenId}).text
    CourseeProcess = json.loads(reps)
    return CourseeProcess


def GetCellInfo(auth_fix, cellid, isIOS):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/GetCellInfo',
                         {'auth_fix': auth_fix, 'cellid': cellid, 'isIOS': isIOS}).text
    CellInfo = json.loads(reps)
    return CellInfo


def UpdateLogInfo(auth_fix, videoEndTime, logId, CellLogId):
    reps = requests.post(r'http://api.hnscen.cn/mobile/api/UpdateLogInfo',
                         {'auth_fix': auth_fix, 'videoEndTime': videoEndTime, 'cellLogId': CellLogId,
                          'LogId': logId}).text
    return reps


def addke(auth, CourseeProcess):
    state = True
    state1 = False
    if len(logidall) <= 10:
        for i in CourseeProcess['data']:
            for j in i['topics']:
                for k in j['cells']:
                    if k['Name'] == logidall[-1]['Process'][1]:
                        state1 = True
                        continue
                    if state1:
                        try:
                            CellInfo = GetCellInfo(auth, k['Id'], False)
                            logId = CellInfo['logId']
                            dis = {'Process': [k['Id'], k['Name'], k['Process']], 'logID': logId}
                            logidall.append(dis)
                            if len(logidall) >= 10:
                                return
                        except Exception:
                            return


def threaduplogidall(auth, Courseinfo, index):
    while True:
        if len(logidall) == 0:
            break
        CourseeProcess = GetCourseeProcess(auth, Courseinfo['course']['CourseOpenId'])

        if len(logidall) <= 10:
            addke(auth, CourseeProcess)
        # print(CourseeProcess['data'][index]['topics'])
        for i in CourseeProcess['data']:
            for j in i['topics']:
                for k in j['cells']:
                    for g in logidall:
                        if k['Type'] == 1 and k['Name'] == g['Process'][1]:
                            g['Process'][2] = k['Process']
        time.sleep(40)


if __name__ == "__main__":
    # 获取登陆返回的信息
    # 账户名，密码
    logininfo = login('username', 'password', None)
    time.sleep(0.1)
    # auth好像比较重要，每个方法都基本上用到了
    auth = logininfo['auth']
    getuserinfo(auth)
    # 获取所有的课
    Course = MyCourse(auth)
    time.sleep(0.1)
    print('课程列表-----------------------')
    for index, i in enumerate(Course['course']):
        print(index, ':课程名字：' + i['name'] + '  进度：' + str(i['process']) + '%')
    print('请选择课程：')
    index = input()
    # 获取到第index个的courseOpenId通过这个才能获取到所有关于第[index]的课
    Courseinfo = GetCourseInfo(auth, Course['course'][int(index)]['courseOpenId'])
    time.sleep(0.1)
    # 通过courseOpenId获取到所有关于社交礼仪的课
    CourseeProcess = GetCourseeProcess(auth, Courseinfo['course']['CourseOpenId'])
    print('模块列表-----------------------')
    for index, i in enumerate(CourseeProcess['data']):
        print(index, '模块名称：' + i['name'])
    print('请选择模块：')
    index = int(input())
    for a in range(index, len(CourseeProcess['data'])):
        # 需要这个
        CourseeProces = CourseeProcess['data'][a]['topics']
        # 所有要刷的课在这个列表里

        for i in CourseeProces:
            for j in i['cells']:
                if j['Type'] == 2 or j['Type'] == 3 or j['Process'] == 100:
                    continue
                CourseeID = j['Id']
                print('j', j)
                try:
                    CellInfo = GetCellInfo(auth, CourseeID, False)
                    logId = CellInfo['logId']
                    dis = {'Process': [j['Id'], j['Name'], j['Process']], 'logID': logId}
                    logidall.append(dis)
                except Exception:
                    print("one Error")
                    pass

    t1 = threading.Thread(target=threaduplogidall, args=(auth, Courseinfo, int(index)))
    t1.start()
    a = 0
    while True:
        # print(logidall)
        for index, i in enumerate(logidall):
            if i['Process'][2] == 100:
                del logidall[index]
                continue
            logId = i['logID']
            # print(i['Process'][1], i['Process'][2], '%')
            UpdateLogInfo(auth, 1, logId, logId)
            time.sleep(5)
        if len(logidall) == 0:
            print("已经刷完了♪(^∇^*)")
            break
