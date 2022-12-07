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
from selenium.webdriver.common.action_chains import ActionChains

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

def gotoPractices(topic):
    time.sleep(2)
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-index subject-math-color']")))
        driver.execute_script("document.getElementsByClassName('item-index subject-math-color')["+str(topic)+"].click()")
    except:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-index subject--color']")))
        driver.execute_script("document.getElementsByClassName('item-index subject--color')[" + str(topic) + "].click()")
def gotoProblems(topic):
    try:
        print(topic)
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-index subject-math-color']")))
        driver.execute_script("document.getElementsByClassName('item-index subject-math-color')[" + str(topic) + "].click()")
    except:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-index subject--color']")))
        driver.execute_script("document.getElementsByClassName('item-index subject--color')[" + str(topic) + "].click()")

def lengthPractices():
    if len(driver.find_elements(By.XPATH,"//div[@class='item-index subject-math-color']")) > 0:
        return len(driver.find_elements(By.XPATH,"//div[@class='item-index subject-math-color']"))
    return len(driver.find_elements(By.XPATH,"//div[@class='item-index subject--color']"))
def lengthProblems():
    if len(driver.find_elements(By.XPATH, "//div[@class='item-index subject-math-color']")) > 0:
        return len(driver.find_elements(By.XPATH, "//div[@class='item-index subject-math-color']"))
    return len(driver.find_elements(By.XPATH, "//div[@class='item-index subject--color']"))

def resultOrStart():
    if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Xem kết quả']"))) or WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Bắt đầu']"))):
        try:
            driver.find_element(By.XPATH,"//div[text()='Xem kết quả']").click()
        except:
            driver.find_element(By.XPATH,"//div[text()='Bắt đầu']").click()

def connect_db():
    return MySQLdb.connect("localhost","root","25251325","crawl_data")

def findQuestion(questionNumber):
    sqlFind = "SELECT * FROM data_self_training where question_number = %s"
    valFind = (questionNumber,)
    cur.execute(sqlFind, valFind)
    return cur.fetchone()
def findAnswerOne(questionNumber):
    sqlFindAnswers = "SELECT * FROM answers where question_number = %s"
    valFindAnswers = (questionNumber,)
    cur.execute(sqlFindAnswers, valFindAnswers)
    return cur.fetchone()
def findAnswerAll(questionNumber):
    sqlFindAnswers = "SELECT * FROM answers where question_number = %s"
    valFindAnswers = (questionNumber,)
    cur.execute(sqlFindAnswers, valFindAnswers)
    return cur.fetchall()
def resDetail(url):
    return json.loads(requests.get(url, headers=HEADER).content)

def getUrl():
    return driver.current_url


def addDataQuestion(id, grade, subject, practices, problems, level, data_question, data_answer, question_number):
    sql = ("INSERT INTO data_self_training(id, grade, subject, practices, problems, level, data_question, data_answer, question_number)"
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    val = (id, grade, str(subject), str(practices), str(problems), level, str(data_question), str(data_answer), question_number)
    cur.execute(sql, val)
    return db_connection.commit()

def addAnwser(id,questionNumber,index_id,answers):
    sql = ("INSERT INTO answers(id,question_number,index_id,answers)"
                 "VALUES (%s,%s,%s,%s)")
    val = (id, str(questionNumber), index_id, answers)
    cur.execute(sql, val)
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
    try:
        return driver.find_element(By.XPATH, "//button[text()=' Trả lời']").click()
    except:
        return driver.find_element(By.XPATH, "//button[text()=' Trả lời ']").click()

HEADER = {
    "Authorization": tokenAuther(),
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
URLFIRST = 'https://api-elb.onluyen.vn/api/practice/questions/detail/'

#DB
db_connection = connect_db()
cur = db_connection.cursor()
id_data = 1692
id_answer = 742
# grade = 1
grade = 1
#Login
loginAccount()
time.sleep(3)
#
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='subject-title']")))

driver.get("https://app.onluyen.vn/practices")
time.sleep(4)
lengthSubject = driver.execute_script("return document.getElementsByClassName('subject-block').length")
for a in range(1, lengthSubject):
    time.sleep(3)
    subject = driver.execute_script("return document.getElementsByClassName('subject-title')["+str(a)+"].innerText")
    print("Subject : ", subject)
    driver.execute_script("document.getElementsByClassName('subject-block')["+str(a)+"].click()")
    time.sleep(2)
    lengthPractices = driver.execute_script("return document.getElementsByClassName('item-name').length")
    list_self_practice_url = driver.current_url
    print(list_self_practice_url)
    if lengthPractices > 0:
        for b in range(5, lengthPractices) :
            time.sleep(1)
            print(b)
            print(range(0, lengthPractices))
            practices = driver.execute_script("return document.getElementsByClassName('item-name')["+str(b)+"].innerText")
            print("Practices : ",practices)
            driver.execute_script("document.getElementsByClassName('item-name')["+str(b)+"].click()")
            time.sleep(1)
            lengthProblems = driver.execute_script("return document.getElementsByClassName('item-name').length")
            linkData = driver.current_url
            for c in range(1, lengthProblems) :
                problems = driver.execute_script("return document.getElementsByClassName('item-name')[" + str(c) + "].innerText")
                print("Problems : ", problems)
                driver.execute_script("document.getElementsByClassName('item-name')[" + str(c) + "].click()")
                time.sleep(1)
                try:
                    driver.find_element(By.XPATH, "//button[text()='Tiếp tục ']").click()
                except:
                    try:
                        driver.find_element(By.XPATH, "//button[text()='Bắt đầu ']").click()
                    except:
                        driver.find_element(By.XPATH, "//button[text()='Làm lại ']").click()
                time.sleep(3.5)
                try:
                    driver.find_element(By.XPATH, "//button[text()=' Câu tiếp theo']").click()
                except:
                    while True:
                        getUrl()
                        urlList = getUrl().split('/')
                        urlAddFirst = urlList[6] + '/' + urlList[7]
                        doneUrlFirst = URLFIRST + urlAddFirst
                        data_question = resDetail(doneUrlFirst)
                        print(data_question)
                        try:
                            questionNumber = data_question['dataStandard']['questionNumber']
                            levelQuestion = data_question['dataStandard']['levelQuestions']
                        except:
                            questionNumber = data_question['dataMaterial']['listStep'][0]['questionNumber']
                            levelQuestion = data_question['dataMaterial']['listStep'][0]['typeAnswer']
                            print(questionNumber)
                        print("Id câu hỏi :", questionNumber)
                        print("Data Question : ", data_question)
                        print("Level Question : ",levelQuestion)
                        time.sleep(2)
                        if len(driver.find_elements(By.XPATH,"//input[@autocomplete='off' and @type='text']")) > 0 :
                            print("Case : 3")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//input[@autocomplete='off' and @type='text']").send_keys("1")
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion, data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                if len(myresultAnswers) > 1:
                                    for index, x in enumerate(myresultAnswers):
                                        driver.find_element(By.XPATH, "//input[@id='mathplay-answer-" + str(
                                            index + 1) + "']").send_keys("" + x[3] + "")
                                else:
                                    driver.find_element(By.XPATH, "//input[@autocomplete='off']").send_keys(
                                        "" + myresultAnswers[0][3] + "")
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//label[@class='form-check-label']")) > 0 :
                            print("Case : 5")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//label[@class='form-check-label']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                try:
                                    for index, x in enumerate(myresultAnswers):
                                        driver.find_element(By.XPATH,"//label[@for='mathplay-answer-" + myresultAnswers[index][3] + "']").click()
                                except:
                                    try:
                                        driver.find_element(By.XPATH,"//label[@for='mathplay-answer-" + myresultAnswers[index][3][-1] + "']").click()
                                    except:
                                        driver.find_element(By.XPATH, "//label").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//div[@id='one-left']")) > 0:
                            print("Case : 4")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//div[@id='one-left']").click()
                                driver.find_element(By.XPATH, "//div[@id='one-right']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                for index, x in enumerate(myresultAnswers):
                                    try:
                                        driver.find_element(By.XPATH, "//div[@class='group1']//div[@value='" + str(
                                            int(int(x[3]) / 10)) + "']").click()
                                        driver.find_element(By.XPATH, "//div[@class='group2']//div[@value='" + str(
                                            int(x[3]) % 10) + "']").click()
                                    except:
                                        driver.find_element(By.XPATH, "//div[@class='float-left']//div[@value='" + str(
                                            int(int(x[3]) / 10)) + "']").click()
                                        driver.find_element(By.XPATH, "//div[@class='float-right']//div[@value='" + str(
                                            int(x[3]) % 10) + "']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//div[@class='select-item']")) > 0 :
                            print("Case : 6")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//div[@class='select-item']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                try:
                                    for index, x in enumerate(myresultAnswers):
                                        driver.find_element(By.XPATH,"//label[@for='mathplay-answer-" + myresultAnswers[index][3] + "']").click()
                                except:
                                    try:
                                        driver.find_element(By.XPATH,"//label[@for='mathplay-answer-" + myresultAnswers[index][3][-1] + "']").click()
                                    except:
                                        driver.find_element(By.XPATH, "//label").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//label[text()='True']")) > 0 :
                            print("Case : 7")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//label[text()='True']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                if myresultAnswers[0][3] == str(0):
                                    driver.find_element(By.XPATH, "//label[text()='False']").click()
                                else:
                                    driver.find_element(By.XPATH, "//label[text()='True']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//ul[@class='question-buttons']")) > 0 :
                            print("Case : 11")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                try:
                                    anwserTrue = data_question["dataStandard"]["options"]
                                except:
                                    anwserTrue = data_question['dataMaterial']['listStep'][0]['options']
                                f = len(driver.find_elements(By.XPATH, "//a[@aria-label='Question 1']"))
                                for z,e in enumerate(range(0, f)):
                                    driver.find_elements(By.XPATH, "//a[@aria-label='Question 1']")[e].click()
                                    anwserTrue = data_question['dataMaterial']['listStep'][e]['options']
                                    for index,g in enumerate(anwserTrue):
                                        if g['isAnswer'] == True :
                                            if index == 0:
                                                driver.find_elements(By.XPATH,"//span[text()='A']")[z].click()
                                            if index == 1:
                                                driver.find_elements(By.XPATH,"//span[text()='B']")[z].click()
                                            if index == 2:
                                                driver.find_elements(By.XPATH,"//span[text()='C']")[z].click()
                                            if index == 3:
                                                driver.find_elements(By.XPATH,"//span[text()='D']")[z].click()
                                    try:
                                        driver.find_element(By.XPATH, "//button[text()=' Trả lời']").click()
                                    except:
                                        continue
                                    time.sleep(3)
                                print("Trả lời")
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                            else:
                                f = len(driver.find_elements(By.XPATH, "//a[@aria-label='Question 1']"))
                                for z, e in enumerate(range(0, f)):
                                    driver.find_elements(By.XPATH, "//a[@aria-label='Question 1']")[e].click()
                                    anwserTrue = data_question['dataMaterial']['listStep'][e]['options']
                                    for index, g in enumerate(anwserTrue):
                                        if g['isAnswer'] == True:
                                            if index == 0:
                                                driver.find_elements(By.XPATH, "//span[text()='A']")[z].click()
                                            if index == 1:
                                                driver.find_elements(By.XPATH, "//span[text()='B']")[z].click()
                                            if index == 2:
                                                driver.find_elements(By.XPATH, "//span[text()='C']")[z].click()
                                            if index == 3:
                                                driver.find_elements(By.XPATH, "//span[text()='D']")[z].click()
                                    try:
                                        driver.find_element(By.XPATH, "//button[text()=' Trả lời']").click()
                                    except:
                                        continue
                                    time.sleep(3)
                                print("Trả lời")
                                time.sleep(2)
                        elif driver.execute_script("return document.getElementsByClassName('question-option-label').length") >= 2 or driver.execute_script("return document.getElementsByClassName('question-option').length") == 4 :
                            print("Case : 8")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                try:
                                    anwserTrue = data_question["dataStandard"]["options"]
                                except:
                                    anwserTrue = data_question['dataMaterial']['listStep'][0]['options']
                                for index,x in enumerate(anwserTrue):
                                    if x['isAnswer'] == True:
                                        caseOneAnswer(index)
                                time.sleep(1)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                # for index, x in enumerate(data_answer['answerFreeText']):
                                #     print(x)
                                #     try:
                                #         addAnwser(id_answer, str(questionNumber), index, x)
                                #         print("Done Add Answer")
                                #         id_answer += 1
                                #     except Exception as a:
                                #         print("Fail Add Answer")
                                #         print(a)
                            else:
                                print("else")
                                try:
                                    anwserTrue = data_question["dataStandard"]["options"]
                                except:
                                    anwserTrue = data_question['dataMaterial']['listStep'][0]['options']
                                for index, x in enumerate(anwserTrue):
                                    if x['isAnswer'] == True:
                                        caseOneAnswer(index)
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//label[text()='Đúng']")) > 0:
                            print("Case : 15")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                driver.find_element(By.XPATH, "//label[text()='Đúng']").click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print('Trả lời')
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                for index, x in enumerate(myresultAnswers):
                                    if int(x[0]) == 1:
                                        driver.find_elements(By.XPATH, "//label[text()='Đúng']")[index].click()
                                    else:
                                        driver.find_elements(By.XPATH, "//label[text()='Sai']")[index].click()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print('Trả lời')
                                time.sleep(2)
                        elif len(driver.find_elements(By.XPATH, "//textarea[@placeholder='Nhập đáp án']")):
                            print("case : 9")
                            myresult = findQuestion(questionNumber)
                            if myresult == None :
                                driver.find_element(By.XPATH, "//textarea[@placeholder='Nhập đáp án']").send_keys("loc")
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                            else:
                                print("else")
                                driver.find_element(By.XPATH, "//textarea[@placeholder='Nhập đáp án']").send_keys("loc")
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        elif driver.execute_script("return document.getElementsByClassName('mathplay-select').length") > 0 :
                            print("Case : 12")
                            try:
                                driver.execute_script("return document.getElementById('mathplay-select-3').click()")
                            except:
                                driver.execute_script("return document.getElementById('mathplay-select-3').click()")
                            driver.execute_script("return document.getElementById('mathplay-answer-1').click()")
                            myresult = findQuestion(questionNumber)
                            if myresult == None:
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
                                    print(x)
                                    try:
                                        addAnwser(id_answer, str(questionNumber), index, x)
                                        print("Done Add Answer")
                                        id_answer += 1
                                    except Exception as a:
                                        print("Fail Add Answer")
                                        print(a)
                            else:
                                clickAnswerQuestion()
                                print("Trả lời")
                        else:
                            print("Case : else")
                            myresult = findQuestion(questionNumber)
                            # exit()
                            if myresult == None:
                                source_element = driver.find_elements(By.XPATH, "//div[@class='text-item']")[2]
                                dest_element = driver.find_elements(By.XPATH, "//div[@class='text-item']")[1]
                                ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
                                time.sleep(2)
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(3)
                                urlLabel = 'https://api-elb.onluyen.vn/api/practice/step/'
                                data_answer = resDetail(urlLabel + urlList[7])
                                print("Data Answers : ", data_answer)
                                try:
                                    addDataQuestion(id_data, grade, subject, practices, problems, levelQuestion,
                                                    data_question, data_answer, questionNumber)
                                    id_data += 1
                                    print("Done Add Math")
                                except Exception as a:
                                    print("Fail Add Math")
                                    print(a)
                                for index, x in enumerate(data_answer['answerFreeText']):
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
                                for index, itemfirst in enumerate(myresultAnswers):
                                    allItem = driver.find_elements(By.XPATH, "//div[@class='text-item']")
                                    print("allTiem")
                                    for  asd in allItem :
                                        print(asd.text)
                                    for index_2,item in enumerate(allItem):
                                        if item.text == itemfirst[3] :
                                            if index == index_2:
                                                continue
                                            if index == 0 :
                                                print("index = ", index, "-index_2 = ", index_2)
                                                source_element = driver.find_elements(By.XPATH, "//div[@class='text-item']")[index_2]
                                                # dest_element = driver.find_element(By.XPATH, 100)
                                                ActionChains(driver).drag_and_drop_by_offset(source_element,-500,0).perform()
                                            else:
                                                print("index = ", index , "-index_2 = ",index_2)
                                                source_element = driver.find_elements(By.XPATH, "//div[@class='text-item']")[index_2]
                                                dest_element = driver.find_elements(By.XPATH, "//div[@class='text-item']")[index - 1]
                                                ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
                                            time.sleep(2)
                                            break
                                print("Câu trả lời : ", myresultAnswers)
                                print("Id câu hỏi : ", myresultAnswers[0][1])
                                clickAnswerQuestion()
                                print("Trả lời")
                                time.sleep(2)
                        try:
                            time.sleep(2)
                            try:
                                try:
                                    driver.find_element(By.XPATH, "//button[text()=' Câu tiếp theo']").click()
                                except:
                                    driver.find_element(By.XPATH, "//button[text()=' Tôi làm đúng']").click()
                            except:
                                time.sleep(2)
                                print("tiep tuc")
                                driver.find_element(By.XPATH, "//a[text()=' Tiếp tục']").click()
                            print("Câu tiếp theo")
                        except:
                            try:
                                driver.find_element(By.XPATH, "//button[text()=' Kết thúc']").click()
                            except:
                                driver.find_element(By.XPATH, "//a[text()=' Kết thúc']").click()
                            print("Kết thúc")
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//button[text()='Thoát ra ']").click()
                            print("Thoát ra")
                            break
                        time.sleep(2)
                        if len(driver.find_elements(By.XPATH, "//button[text()=' Kết thúc ']")) > 0:
                            print("ket")
                            driver.find_element(By.XPATH, "//button[text()=' Kết thúc ']").click()
                            time.sleep(2)
                            driver.find_element(By.XPATH, "//button[text()='Thoát ra ']").click()
                            print("Thoát ra")
                            break
                        time.sleep(3)
                if c < lengthProblems - 1 :
                    print("c < ")
                    driver.get(linkData)
                    time.sleep(2)
            driver.get(list_self_practice_url)
        time.sleep(2)
    driver.get("https://app.onluyen.vn/practices")
    time.sleep(2)