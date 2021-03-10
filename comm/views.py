from django.shortcuts import render,HttpResponse
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import time,random,requests
# Create your views here.

def comm(request):
    return render(request,'comm.html',locals())

def ig(request):
    url = request.POST["url"]
    p = request.POST["p"]
    Keyword = request.POST["Keyword"]
    tag = request.POST["tag"]
    rep = request.POST["re"]

    #IGID='jacky70638'
    #IGpassword='KACKY827058'
    browser = webdriver.Chrome()
    #ur='https://www.instagram.com/'
    #browser.get(ur)
    #time.sleep(1)
    #browser.find_element_by_xpath('//*[@name="username"]').send_keys(IGID) #輸入帳號
    #browser.find_element_by_xpath('//*[@name="password"]').send_keys(IGpassword) # 輸入密碼
    #browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()#按登入
    #time.sleep(1)
    browser.get(url)#https://www.instagram.com/p/CMCZnmCjTZx/
    time.sleep(1)
    while True:
        try:
            browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/li/div/button/span').click()#按+
            time.sleep(3)
        except:    
            break
    soup = BeautifulSoup(browser.page_source,"lxml")
    purl=soup.find_all("div",class_="KL4Bh")[0].img.get('src')
    user_name=soup.find_all("div",class_="C4VMK")[0].a.text
    pic_url=soup.find_all("div",class_="RR-M- h5uC0 mrq0Z")[0].img.get('src')
    text__url=soup.find_all("div",class_="C4VMK")[0].find("span",class_="").text
    text__url=text__url.split()
    text_url=text__url[0]+text__url[1]
    q=soup.find_all("div",class_="C4VMK")
    qq=soup.find_all("a",class_="_2dbep qNELH kIKUG")
    print(len(qq))
    a=0
    b,c,img_url=[],[],[]
    for i in range(len(q)):
        if a==0:
            a+=1
        else:
            s=q[i].a.text
            t=q[i].find("span",class_="").string
            b.append(s)
            c.append(t)
    for i in range(len(qq)):
        r=qq[i].img.get('src')
        img_url.append(r)
    browser.close()

    u_name=[]
    u_comment=[]
    u_img_url=[]
    for i in range(int(p)):
        while True:
            try:
                number = random.randint(0,len(q)-1)
                if Keyword in c[number]:
                    ta=c[number].count("@")
                    if int(ta)>=int(tag):
                        if str(rep) == "Y":
                            u_name.append(b[number])
                            u_comment.append(c[number])
                            u_img_url.append(img_url[number])
                            break
                        else:
                            if int(len(u_comment)) == int(0):
                                u_name.append(b[number])
                                u_comment.append(c[number])
                                u_img_url.append(img_url[number])
                                break
                            else:
                                if c[number] in u_comment:
                                    pass
                                else:
                                    u_name.append(b[number])
                                    u_comment.append(c[number])
                                    u_img_url.append(img_url[number])
                                    break
                    else:
                        pass
                else:
                    pass
            except:
                pass
            else:
                pass
    kq=[]        
    for i in range(len(u_name)):
        kq.append(u_name[i]+' '+u_comment[i])
        print("得獎者",u_name[i],u_comment[i])
    
    dic={'u_img_url':u_img_url,'u_name':u_name, 'u_comment':u_comment}
    dic['u_info'] = zip(dic['u_img_url'], dic['u_name'],dic['u_comment'])

    return render(request,'commm.html',locals())