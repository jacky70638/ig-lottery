from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time,random
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
import matplotlib as mpl

#------------------------------抓文張連結
conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=IG;SERVER=USER-PC\ASP')
cursor = conn.cursor()

IGID=''
IGpassword=''
browser = webdriver.Chrome()
url = 'https://www.instagram.com/hoelaine1116/'
browser.get(url)
time.sleep(1)
browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()#按登入
time.sleep(0.8)
browser.find_element_by_xpath('//*[@name="username"]').send_keys(IGID) #輸入帳號
browser.find_element_by_xpath('//*[@name="password"]').send_keys(IGpassword) # 輸入密碼
browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()#按登入
time.sleep(3)
browser .find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()#按稍後再說
url = 'https://www.instagram.com/hoelaine1116/'
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
n_title=soup.find("h2",class_="_7UhW9 fKFbl yUEEX KV-D4 fDxYl").text

n = 5
post_url = []
for i in range(n):
    scroll = 'window.scrollTo(0, document.body.scrollHeight);'
    browser.execute_script(scroll)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    for elem in soup.select('article div div div div a'):
        if elem['href'] not in post_url:
            post_url.append(elem['href'])
            cursor.execute("insert into IG(id,post) values('{}','{}')".format(n_title,elem['href']))
    time.sleep(1)

url = 'https://www.instagram.com/hoelaine1116/'
browser.get(url)
date,like,comment=[],[],[]
for i in range(len(post_url)):    
    try:
        post_elem = browser.find_element_by_xpath('//a[@href="'+str(post_url[i])+'"]')
        action = ActionChains(browser)
        action.move_to_element(post_elem).perform()
        time.sleep(1)
        
        soup = BeautifulSoup(browser.page_source,"lxml")
        n_like_elem = browser.find_elements_by_class_name('-V_eO')
        n_like = n_like_elem[0].text
        n_comment = n_like_elem[1].text
        if '萬' in n_like:
            n_like=n_like.replace('萬','')
            n_like=float(n_like)*10000
            n_like=int(n_like)
            like.append(n_like)
        else:
            like.append(n_like)
        comment.append(n_comment)
        cursor.execute("""UPDATE IG SET p_like='{}',p_comment='{}'
                    WHERE post='{}'""".format(n_like,n_comment,post_url[i]))#更新資料  
    except:
        scroll = 'window.scrollBy(0,250)'
        browser.execute_script(scroll)
        continue

for i in range(len(post_url)):    
    url='https://www.instagram.com{}'.format(post_url[i])
    browser.get(url)
    soup = BeautifulSoup(browser.page_source,"lxml")
    n_date=soup.find("time",class_="_1o9PC Nzb55").get('title')
    date.append(n_date)
    time.sleep(0.5)
    cursor.execute("""UPDATE IG SET date='{}'
                    WHERE post='{}'""".format(n_date,post_url[i]))#更新資料  

browser.close()
conn.commit()
cursor.close()
conn.close()
# ------------------------------資料分析
conn = pyodbc.connect('DRIVER={SQL Server};user=sa;password=1234;database=IG;SERVER=USER-PC\ASP')
cursor = conn.cursor()
cursor.execute("SELECT * FROM IG")
rows = cursor.fetchall()

name,post,like,comment,date=[],[],[],[],[]
for row in rows:
    name.append(row.id)
    post.append(row.post)
    like.append(int(row.p_like))
    comment.append(int(row.p_comment))
    date.append(row.date)

max_like = str(max(like))
min_like = str(min(like))
a=np.linspace(int(max_like),int(min_like),10,dtype=int)
a=a.tolist()
max_comment = str(max(comment))
min_comment = str(min(comment))
b=np.linspace(int(max_comment),int(min_comment),10,dtype=int)
b=b.tolist()

date_d=[]
date_n=[]
for i in range(len(date)):
    d=date[i][5:11]
    d=d.replace('月','/')
    d=d.replace('日','')
    date_d.append(d)
    n=i+1
    date_n.append(n)

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
    
name_like=name[0]+'按讚數分析'
name_comment=name[0]+'留言數分析'
width=0.25  
plt.bar(date_d,like,width=0.6,color="r",label='讚數')    #繪製長條圖
plt.xticks(date_d, date_d,rotation=75,fontsize=11,fontweight='bold')      #設定 X 軸刻度標籤
plt.yticks(a, a)                         #設定 Y 軸刻度標籤
plt.legend()                                       #顯示圖例
plt.title(name_like)                                       #設定圖形標題
plt.xlabel('DATE')                                 #設定 X 軸標籤
plt.ylabel('Volume')                               #設定 Y 軸標籤
plt.show()

width=0.25  
plt.bar(date_d,comment,width=0.6,color="g",label='留言數')    #繪製長條圖
plt.xticks(date_d, date_d,rotation=75,fontsize=11,fontweight='bold')      #設定 X 軸刻度標籤
plt.yticks(b,b)                         #設定 Y 軸刻度標籤
plt.legend()                                       #顯示圖例
plt.title(name_comment)                                       #設定圖形標題
plt.xlabel('DATE')                                 #設定 X 軸標籤
plt.ylabel('Volume')                               #設定 Y 軸標籤
plt.show()

cursor.close()
conn.close()
