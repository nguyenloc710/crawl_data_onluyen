import json
import time
from selenium.webdriver.support import expected_conditions as EC
import MySQLdb
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Firefox()
driver.get("https://app.onluyen.vn")

def tokenAuther():
    url = 'https://oauth.onluyen.vn/api/account/login'

    headers = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    payload = {
        "phoneNumber": "84967067839",
        "password": "123456789",
        "rememberMe": True,
        "socialType": "Email",
        "userName": "84967067839"
    }

    res = requests.post(url, data=json.dumps(payload), headers=headers)

    detail = json.loads(res.content)
    Authorization = 'Bearer ' + detail['access_token']

    return Authorization

def loginAccount(): #Đăng nhập tài khoản
    username = driver.find_element(By.ID, "username")
    username.send_keys("84967067839")
    password = driver.find_element(By.ID, "password")
    password.send_keys("123456789")
    password.send_keys(Keys.RETURN)

def goToLink(): #Đi đến link Kiểm tra toán
    driver.find_element(By.XPATH, "//div[@class='subject-title' and text()='Tiếng Anh']").click()

def gotoPractices(topic):
    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-content']")))
    driver.execute_script("document.getElementsByClassName('item-content')[" + str(topic) + "].click()")
def gotoProblems(topic):
    # try:
    print(topic)
    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-content']")))
    driver.execute_script("document.getElementsByClassName('item-content')[" + str(topic) + "].click()")
    # except:
    #     WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-content']")))
    #     driver.execute_script("document.getElementsByClassName('item-content')[" + str(topic) + "].click()")

def lengthPractices():
    if len(driver.find_elements(By.XPATH,"//div[@class='item-content']")) > 0:
        return len(driver.find_elements(By.XPATH,"//div[@class='item-content']"))
    return len(driver.find_elements(By.XPATH,"//div[@class='item-content']"))
def lengthProblems():
    if len(driver.find_elements(By.XPATH, "//div[@class='item-content']")) > 0:
        return len(driver.find_elements(By.XPATH, "//div[@class='item-content']"))
    return len(driver.find_elements(By.XPATH, "//div[@class='item-content']"))

def resultOrStart():
    if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Xem kết quả']"))) or WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Bắt đầu']"))):
        try:
            driver.find_element(By.XPATH,"//div[text()='Xem kết quả']").click()
        except:
            driver.find_element(By.XPATH,"//div[text()='Bắt đầu']").click()

def connect_db():
    return MySQLdb.connect("localhost","root","25251325","self_study_math_12")

def findQuestion(questionNumber):
    sqlFind = "SELECT * FROM math_12 where questionNumber = %s"
    valFind = (questionNumber,)
    cur.execute(sqlFind, valFind)
    return cur.fetchone()
def findAnswerOne(questionNumber):
    sqlFindAnswers = "SELECT * FROM answers where questionNumber = %s"
    valFindAnswers = (questionNumber,)
    cur.execute(sqlFindAnswers, valFindAnswers)
    return cur.fetchone()
def findAnswerAll(questionNumber):
    sqlFindAnswers = "SELECT * FROM answers where questionNumber = %s"
    valFindAnswers = (questionNumber,)
    cur.execute(sqlFindAnswers, valFindAnswers)
    return cur.fetchall()
def resDetail(url):
    return json.loads(requests.get(url, headers=HEADER).content)

def getUrl():
    return driver.current_url


def addMath_12(id, questionNumber, problems, practices, json_math, anwser):
    sqlMath = ("INSERT INTO math_12(id,questionNumber,problems,practices,json_math,anwser)"
               "VALUES (%s,%s,%s,%s,%s,%s)")
    valMath = (id, str(questionNumber), str(problems), str(practices), str(json_math),str(anwser))
    cur.execute(sqlMath, valMath)
    return db_connection.commit()

def addAnwser(id,questionNumber,indexId,answer):
    sqlAnswer = ("INSERT INTO answers(id,questionNumber,indexId,answer)"
                 "VALUES (%s,%s,%s,%s)")
    valAnswer = (id, str(questionNumber), indexId, answer)
    cur.execute(sqlAnswer, valAnswer)
    return db_connection.commit()

def caseOneAnswer(option):
    if option == 0 :
        return driver.execute_script("document.getElementsByClassName('question-option-label float-left')['0'].click()")
    if option == 1:
        return driver.execute_script("document.getElementsByClassName('question-option-label float-left')['1'].click()")
    if option == 2:
        return driver.execute_script("document.getElementsByClassName('question-option-label float-left')['2'].click()")
    if option == 3:
        return driver.execute_script("document.getElementsByClassName('question-option-label float-left')['3'].click()")

def clickAnswerQuestion():
    return driver.find_element(By.XPATH, "//button[text()=' Trả lời']").click()
HEADER = {
    "Authorization": tokenAuther(),
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
URLFIRST = 'https://api-elb.onluyen.vn/api/practice/questions/detail/'

#DB
db_connection = connect_db()
cur = db_connection.cursor()
id_math = 146
id_answer = 238
#Login
loginAccount()
time.sleep(3)
#
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='subject-title']")))
goToLink()#go link Toan
time.sleep(2)
linkMath = driver.current_url
print(linkMath)
for x in range(1, lengthPractices()):
    time.sleep(3)
    practices = driver.execute_script("return document.getElementsByClassName('item-name')["+ str(x) +"].innerText")
    print("Chương : ", practices)
    print("go")
    gotoPractices(x)
    for y in range(0,  lengthProblems()):
        print("y = ",y)
        time.sleep(3)
        gotoProblems(y)
        list_self_problems_url = driver.current_url
        problems = driver.execute_script("return document.getElementsByClassName('item-name')[" + str(y) + "].innerText ")
        print("Bài luyên tập : ", problems)
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, "//button[text()='Tiếp tục ']").click()
        except:
            try:
                driver.find_element(By.XPATH, "//button[text()='Bắt đầu ']").click()
            except:
                driver.find_element(By.XPATH, "//button[text()='Làm lại ']").click()
        time.sleep(3)
        try:
            driver.find_element(By.XPATH, "//button[text()=' Câu tiếp theo']").click()
        except:
            while True:
                getUrl()
                urlList = getUrl().split('/')
                urlAddFirst = urlList[6] + '/' + urlList[7]
                doneUrlFirst = URLFIRST + urlAddFirst
                detailFirst = resDetail(doneUrlFirst)
                questionNumber = detailFirst['dataStandard']['questionNumber']
                print("Id câu hỏi :", questionNumber)
                print("Câu đề bài : ", detailFirst)
                if len(driver.find_elements(By.XPATH,"//label[text()='Đúng']")) > 0:
                    print("Case : 1")
                    myresult = findQuestion(questionNumber)
                    if myresult == None:
                        driver.find_element(By.XPATH,"//label[text()='Đúng']").click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print('Trả lời')
                        time.sleep(2)
                        urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                        detail = resDetail(urlLabel + urlList[7])
                        print("Câu trả lời : ", detail)
                        try:
                            addMath_12(id_math, questionNumber, problems, practices, detailFirst, detail)
                            id_math += 1
                            print("Done Add Math")
                        except Exception as a:
                            print("Fail Add Math")
                            print(a)
                        for index, x in enumerate(detail['answerFreeText']):
                            try:
                                addAnwser(id_answer, str(questionNumber), index, x)
                                print("Done Add Answer")
                                id_answer += 1
                            except Exception as a:
                                print("Fail Add Answer")
                                print(a)
                    else:
                        print("else")
                        myresultAnswers = findAnswerAll(questionNumber)
                        for index, x in enumerate(myresultAnswers):
                            if int(x[0]) == 1:
                                driver.find_elements(By.XPATH, "//label[text()='Đúng']")[index].click()
                            else:
                                driver.find_elements(By.XPATH, "//label[text()='Sai']")[index].click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print('Trả lời')
                        time.sleep(2)
                elif len(driver.find_elements(By.XPATH,"//label//img")) > 0:
                    print("Case : 2")
                    myresult = findQuestion(questionNumber)
                    if myresult == None:
                        driver.find_element(By.XPATH,"//label//img").click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                        urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                        detail = resDetail(urlLabel + urlList[7])
                        print("Câu trả lời : ", detail)
                        try:
                            addMath_12(id_math, questionNumber, problems, practices, detailFirst, detail)
                            id_math += 1
                            print("Done Add Math")
                        except Exception as a:
                            print("Fail Add Math")
                            print(a)
                        for index, x in enumerate(detail['answerFreeText']):
                            print(x)
                            try:
                                addAnwser(id_answer, str(questionNumber), index, x)
                                print("Done Add Answer")
                                id_answer += 1
                            except Exception as a:
                                print("Fail Add Answer")
                                print(a)
                    else:
                        print("else")
                        myresultAnswers = findAnswerOne(questionNumber)
                        driver.find_elements(By.XPATH,"//label//img")[(int(myresultAnswers[0])-1)].click()
                        time.sleep(2)
                        driver.find_element(By.XPATH, "//button[text()=' Trả lời']").click()
                        time.sleep(2)
                elif len(driver.find_elements(By.XPATH, "//input[@autocomplete='off']")) > 0:
                    print("Case : 3")
                    myresult = findQuestion(questionNumber)
                    if myresult == None:
                        driver.find_element(By.XPATH, "//input[@autocomplete='off']").send_keys("1")
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                        urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                        detail = resDetail(urlLabel + urlList[7])
                        print("Câu trả lời : ", detail)
                        try:
                            addMath_12(id_math, questionNumber, problems, practices, detailFirst, detail)
                            id_math += 1
                            print("Done Add Math")
                        except Exception as a:
                            print("Fail Add Math")
                            print(a)
                        for index, x in enumerate(detail['answerFreeText']):
                            print(x)
                            try:
                                addAnwser(id_answer, str(questionNumber), index, x)
                                print("Done Add Answer")
                                id_answer += 1
                            except Exception as a:
                                print("Fail Add Answer")
                                print(a)
                    else:
                        print("else")
                        myresultAnswers = findAnswerAll(questionNumber)
                        print("Câu trả lời : ",myresultAnswers)
                        print("Id câu hỏi : ",myresultAnswers[0][3])
                        if len(myresultAnswers)>1:
                            for index,x in enumerate(myresultAnswers):
                                driver.find_element(By.XPATH, "//input[@id='mathplay-answer-"+str(index+1)+"']").send_keys("" + x[0] + "")
                        else:
                            driver.find_element(By.XPATH, "//input[@autocomplete='off']").send_keys("" + myresultAnswers[0][0] + "")
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                elif len(driver.find_elements(By.XPATH,"//div[@id='one-left']")) > 0:
                    print("Case : 4")
                    myresult = findQuestion(questionNumber)
                    if myresult == None:
                        driver.find_element(By.XPATH, "//div[@id='one-left']").click()
                        driver.find_element(By.XPATH, "//div[@id='one-right']").click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                        urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                        detail = resDetail(urlLabel + urlList[7])
                        print("Câu trả lời : ", detail)
                        try:
                            addMath_12(id_math, questionNumber, problems, practices, detailFirst, detail)
                            id_math += 1
                            print("Done Add Math")
                        except Exception as a:
                            print("Fail Add Math")
                            print(a)
                        for index, x in enumerate(detail['answerFreeText']):
                            print(x)
                            try:
                                addAnwser(id_answer, str(questionNumber), index, x)
                                print("Done Add Answer")
                                id_answer += 1
                            except Exception as a:
                                print("Fail Add Answer")
                                print(a)
                    else:
                        print("else")
                        myresultAnswers = findAnswerAll(questionNumber)
                        print(myresultAnswers)
                        print("Id câu hỏi : ",myresultAnswers[0][3])
                        print(myresultAnswers)
                        for index,x in enumerate(myresultAnswers):
                            try:
                                driver.find_element(By.XPATH,"//div[@class='group1']//div[@value='"+str(int(int(x[0]) / 10))+"']").click()
                                driver.find_element(By.XPATH,"//div[@class='group2']//div[@value='"+str(int(x[0]) % 10)+"']").click()
                            except:
                                driver.find_element(By.XPATH, "//div[@class='float-left']//div[@value='" + str(int(int(x[0]) / 10)) + "']").click()
                                driver.find_element(By.XPATH, "//div[@class='float-right']//div[@value='" + str(int(x[0]) % 10) + "']").click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                else:
                    print("Case : 5")
                    myresult = findQuestion(questionNumber)
                    if myresult == None:
                        driver.find_element(By.XPATH,"//label").click()
                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                        urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                        detail = resDetail(urlLabel + urlList[7])
                        print("Câu trả lời : ", detail)
                        try:
                            addMath_12(id_math, questionNumber, problems, practices, detailFirst, detail)
                            id_math += 1
                            print("Done Add Math")
                        except Exception as a:
                            print("Fail Add Math")
                            print(a)
                        for index, x in enumerate(detail['answerFreeText']):
                            print(x)
                            try:
                                addAnwser(id_answer, str(questionNumber), index, x)
                                print("Done Add Answer")
                                id_answer += 1
                            except Exception as a:
                                print("Fail Add Answer")
                                print(a)
                    else:
                        print("else")
                        myresultAnswers = findAnswerAll(questionNumber)
                        print(myresultAnswers)
                        # driver.find_element(By.XPATH,"//label[@for='mathplay-answer-" + myresultAnswers[0] + "']").click()
                        try:
                            for index,x in enumerate(myresultAnswers):
                                driver.find_element(By.XPATH, "//label[@for='mathplay-answer-"+myresultAnswers[index][0]+"']").click()
                        except:
                            try:
                                driver.find_element(By.XPATH, "//label[@for='mathplay-answer-"+myresultAnswers[index][0][-1]+"']").click()
                            except:
                                driver.find_element(By.XPATH, "//label").click()

                        time.sleep(2)
                        clickAnswerQuestion()
                        print("Trả lời")
                        time.sleep(2)
                try:
                    driver.find_element(By.XPATH, "//button[text()=' Câu tiếp theo']").click()
                    print("Câu tiếp theo")
                except:
                    driver.find_element(By.XPATH, "//button[text()=' Kết thúc']").click()
                    print("Kết thúc")
                    time.sleep(2)
                    driver.find_element(By.XPATH, "//button[text()='Thoát ra ']").click()
                    print("Thoát ra")
                    break
                time.sleep(4)
        if y < lengthProblems()-1:
            print("load")
            driver.get(list_self_problems_url)
        else:
            break
    driver.get(linkMath)
    time.sleep(2)