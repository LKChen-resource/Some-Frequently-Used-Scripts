#Automatic reservation of badminton court at Hunan University
from selenium import webdriver
import os
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#首页http://gym.hnu.edu.cn/
main_url='http://gym.hnu.edu.cn/'
#登录
login_url='http://gym.hnu.edu.cn/gym/login'
#抢场地
target_url='http://gym.hnu.edu.cn/gym/book?vid=68'

class gym:
    """初始化加载"""
    def __init__(self):
        self.status = 0  #状态，表示当前执行步骤
        self.login_method = 1 #{0:模拟登录，1：cookie登录}
        self.driver = webdriver.Edge() #初始化浏览器 executable_path=''

    """cookies：记录用户信息"""
    def  set_cookies(self):
        self.driver.get(login_url)
        print("###正在登录###")
        WebDriverWait(self.driver,20,0.1).until(EC.presence_of_element_located((By.ID,'code')))
        self.driver.find_element(By.ID,'code').click()
        self.driver.find_element(By.ID,'code').send_keys('S200100017')
        self.driver.find_element(By.ID,'pwd').click()
        self.driver.find_element(By.ID,'pwd').send_keys('HN/clk1998/')
        #self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.ID,'68'))
        
        #time.sleep(20)
        print("###登录成功###")
        input("按下回车开始场地预约")
        pickle.dump(self.driver.get_cookies(),open('cookies.pkl','wb'))
        print("###cookies已保存###")
        
        #self.driver.get(target_url)

    """获取cookies"""
    def get_cookies(self):
         
        cookies = pickle.load(open('cookies.pkl','rb'))
        for cookie in cookies:
            #print(cookie)
            cookie_dict = {
                'domain' : 'gym.hnu.edu.cn',
                'name': cookie.get('name'),
                'value':cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)
            print("###载入cookie成功")


        

    """登录"""    
    def login(self):
        #如果为0，模拟登录
        if self.login_method == 0:
            self.driver.get(login_url)
        elif self.login_method == 1:
            self.driver.get(target_url)
                #登录一下 通过selenium传入用户信息
            self.set_cookies()
            #如果当前目录下，没有cookie
            # if not os.path.exists('cookies.pkl'):
            #     # 登录一下
            #     self.set_cookies()
            # else:
            #     self.driver.get(target_url)
            #     #登录一下 通过selenium传入用户信息
            #     self.get_cookies()

    """打开浏览器"""
    def enter_gym(self):
        print("###打开浏览器，进入体育馆预约界面")
        #调用login
        # self.login()
        #self.driver.refresh()
        self.status = 2
        print("###登录成功###")
        #预约
        

    def sleepAwhile(self,H,M,S):
        sleeptimes=self.time_different(H,M,S)
        print("###程序进入睡眠，等待,",H,":",M,":",S,"启动###")
        time.sleep(sleeptimes)

    def time_different(self,target_hour,target_min,target_sec):
        t=time.localtime()
        sleep_time=(target_hour-t.tm_hour)*3600+(target_min-t.tm_min)*60+(target_sec-t.tm_sec)
        return sleep_time


    #抢场地，并下单   ###点击流程没做好，选择场地的逻辑，顺序、判断标准
    def choose_field(self):
        if self.status == 2:
            print('='*30)
            print("###开始选择场地日期和时间段")
            self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.ID,'68')) #68-羽毛球场；61-形体房；46-乒乓球
            """1.选择场地类型
                2.根据目标顺序，依次判断场地/根据场地信息，对目标进行判定
                3."""
            print("开始选择场地")#不稳定，有时可以进入场地选择完成，有时不行:采用该方式有时发包需要等待，该方式类似点击，故存在指定元素未加载成功
#//*[@id="session_container"]/div[2]/div[2]/div[13]/span

            target_field1 = ['/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[8]/div[13]','/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[8]/div[14]']#6号场
            target_field2 = ['/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[9]/div[13]','/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[9]/div[14]']#5号场从表头开始，第3行，第14列（最后一列）
            target_field3 = ['/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[7]/div[13]','/html/body/div[1]/article/div/div[5]/div/div/div/div/div[1]/div/div[2]/div/div/div[2]/div[1]/div/div[2]/div[7]/div[14]']#1号场
           #//*[@id="session_container"]/div[2]/div[3]/div[2]
            # target_field1 = ['//*[@id="session_container"]/div[2]/div[12]/div[13]','//*[@id="session_container"]/div[2]/div[12]/div[14]']#6号场
            # target_field2 = ['//*[@id="session_container"]/div[2]/div[13]/div[13]','//*[@id="session_container"]/div[2]/div[13]/div[14]']#5号场从表头开始，第3行，第14列（最后一列）
            # target_field3 = ['//*[@id="session_container"]/div[2]/div[14]/div[13]','//*[@id="session_container"]/div[2]/div[14]/div[14]']#1号场//*[@id="session_container"]/div[2]/div[5]/div[13]
            
            WebDriverWait(self.driver,20,0.1).until(EC.presence_of_element_located((By.XPATH,target_field1[0])))
            print("元素加载完成")
            i=0
            while self.driver.current_url !='http://gym.hnu.edu.cn/gym/order/submit' :

                #//*[@id="session_container"]/div[2]/div[2]/div[13]/span
                ##session_container > div.box-time > div:nth-child(2) > div:nth-child(7)
                ##session_container > div.box-time > div:nth-child(2) > div:nth-child(6)
                ##session_container > div.box-time > div:nth-child(8) > div:nth-child(13)
                #document.querySelector("#session_container > div.box-time > div:nth-child(8) > div:nth-child(13)")
                
                
                if self.check_field_status(target_field1[0]) and self.check_field_status(target_field1[1]) :
                    self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field1[0]))
                    self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field1[1]))
                    print("预约目标-1-完成")
                else:
                    if self.check_field_status(target_field2[0]) and self.check_field_status(target_field2[1]):
                        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field2[0]))
                        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field2[1]))
                        print("预约目标-2-完成")
                        
                    else:
                        if self.check_field_status(target_field3[0]) and self.check_field_status(target_field3[1]): 
                            self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field3[0]))
                            self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.XPATH,target_field3[1]))
                            # status=self.driver.find_element(By.XPATH,target_field3[0]).get_attribute('class')
                            # if status == 
                            print("预约目标-3-完成")
                        else:
                            print('目标场次123,全被预定')
                WebDriverWait(self.driver,20,0.05).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/article/div/div[5]/div/div/div/div/div[2]/div[2]/div[3]/button")))
                submit=self.driver.find_element(By.XPATH,"/html/body/div[1]/article/div/div[5]/div/div/div/div/div[2]/div[2]/div[3]/button")
                self.driver.execute_script("arguments[0].click();",submit)
                print("确定预定")
                i=i+1
                print(i)
            print("循环结束")
            submit_button='//*[@id="order_container"]/tr[3]/td/button'#tr[2]为约一个场，tr[3]为约两个场
            WebDriverWait(self.driver,20,0.05).until(EC.presence_of_element_located((By.XPATH,submit_button)))
            #time.sleep(0.1)
            book_button=self.driver.find_element(By.XPATH,submit_button)
            self.driver.execute_script("arguments[0].click();",book_button)
            
            
    def refresh(self,date):
        self.driver.get(target_url)

        WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".m-n.text-muted")))
        while self.driver.find_element(By.CSS_SELECTOR,".m-n.text-muted").text != date:
            self.driver.refresh()
            time.sleep(0.5)
            print('刷新页面')
            WebDriverWait(self.driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".m-n.text-muted")))
        print('日期更新至'+date)
        # if self.driver.find_element(By.CSS_SELECTOR,".m-n.text-muted").text == date:
        #     print('日期更新')
        # else:
        #     self.driver.refresh()
        #     print('刷新页面')
        
            

    def persist_find(self,target):
        while self.driver.find_element(By.XPATH,target) != 1:
            self.persist_find(target)
            time.sleep(0.05)

    # 检查元素是否存在
    def check_field_status(self,target_fd):
        
        try:
            status=self.driver.find_element(By.XPATH,target_fd).get_attribute('class')
            if status == 'selectTrue':
                return True
            else:
                print(status)
                return False
        except Exception as e:
            
            return False
        
 
        


        
if __name__ == '__main__':
    gy = gym()
    gy.login()
    gy.enter_gym()
    gy.sleepAwhile(21,57,30)
    gy.refresh("2023-06-15")
    gy.choose_field()
    print("请付款")
    input("回车--结束预约脚本")
    

