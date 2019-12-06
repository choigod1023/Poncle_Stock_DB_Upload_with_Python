import requests
from selenium import webdriver
import time
import json
import pymysql

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
db = pymysql.connect(host='ls-26ad06eefaae1cfe950257242db7dc380bb5c17a.cf3gtsxh4cfe.ap-northeast-2.rds.amazonaws.com', user='dbjhuser',
                     password='db20191023!!', db='dbjhmol', port=3306)

cursor = db.cursor()


def login():
    try:
        driver.get('https://agent.poncle.co.kr/member/login?url=Lw==')
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="userid"]').send_keys('jh04070502')
        driver.find_element_by_xpath('//*[@id="userpw"]').send_keys('rhkdtp00')
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        return
    except:
        return


global full_json
full_json = []


def stockupload():
    if True:
        driver.get('https://agent.poncle.co.kr/stock/listStock?window=&start=1&sort=indate&by=desc&serialtype=serial&dates=1&sdate=&edate=&scale=1000&cond=&gubun=&telcompany=&incompany=&outcompany=&outuser=&models=1&model=&color=&ss=serial&serial=&mserial=')
        time.sleep(5)
        driver.refresh()
        i = 1
        start_count = 1
        while True:
            driver.get('https://agent.poncle.co.kr/stock/listStock?window=&start='+str(start_count) +
                       '&sort=indate&by=desc&serialtype=serial&dates=1&sdate=&edate=&scale=1000&cond=&gubun=&telcompany=&incompany=&outcompany=&outuser=&models=1&model=&color=&ss=serial&serial=&mserial=')
            print(driver.find_element_by_xpath('/html/body').text)
            json_list = json.loads(
                driver.find_element_by_xpath('/html/body').text, encoding='utf-8')
            if True:
                if json_list['list'] != []:
                    jsons = json_list['list']
                    full_json.append(jsons)
                    for one_json in jsons:

                        state = one_json['statex']
                        receive_date = one_json['indate']
                        progress = one_json['condx']
                        serial = one_json['serial']
                        model = one_json['model']
                        color = one_json['color']
                        price = one_json['inprice']
                        receive_place = one_json['incompany_title']
                        forward_place = one_json['outcompany_title']
                        processing_date = one_json['outdate']
                        handler = one_json['user']
                        memo = one_json['memo']
                        gubun = one_json['gubun']
                        sql = 'select count(*) from bus_stock where serial = "{}";'.format(serial)
                        try:
                            cursor.execute(sql)
                            rows = cursor.fetchall()
                            if rows[0][0] > 0:
                                sql = 'update bus_stock set state = "{}",receive_date = "{}",progress = "{}",serial="{}",model = "{}",color="{}",price="{}",receive_place="{}",forward_place="{}",processing_date="{}",handler="{}",memo="{}",gubun="{}" where serial = "{}";'.format(
                                    state, receive_date, progress, serial, model, color, price, receive_place, forward_place, processing_date, handler, memo, gubun, serial)
                            else:
                                sql = 'insert into bus_stock values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","1","{}");'.format(
                                    state, receive_date, progress, serial, model, color, price, receive_place, forward_place, processing_date, handler, memo, gubun)
                        except:
                            sql = 'insert into bus_stock values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","1","{}");'.format(
                                state, receive_date, progress, serial, model, color, price, receive_place, forward_place, processing_date, handler, memo, gubun)
                        cursor.execute(sql)
                        db.commit()
            time.sleep(2)
            driver.refresh()
            start_count = i*1000
            i = i+1
        print(full_json)
        time.sleep(2)
        driver.get('https://agent.poncle.co.kr/stock/listStock?window=&start=1000&sort=indate&by=desc&serialtype=serial&dates=1&sdate=&edate=&scale=1000&state=S&cond=&gubun=&telcompany=&incompany=&outcompany_title=&outuser=&models=1&model=&color=&ss=serial&serial=&mserial=')
        a = json.loads(driver.find_element_by_xpath('/html/body').text)


login_cnt = 0
while True:
    url = driver.current_url
    print(url)
    if not login_cnt or 'https://agent.poncle.co.kr/member' in url:
        print("hi")
        login()
        login_cnt = 1
    time.sleep(2)
    if stockupload():
        driver.quit()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        continue
    time.sleep(5)
