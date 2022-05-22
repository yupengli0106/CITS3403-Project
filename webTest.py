import unittest, time, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
class Case(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''open browser'''
        self.d = webdriver.Chrome()
        self.d.maximize_window()
        self.d.get('http://127.0.0.1:5000/')
        self.d.implicitly_wait(3)
        self.time = 1

    @classmethod
    def tearDownClass(self):
        '''exit browser'''
        time.sleep(1)
        self.d.quit() 

    def tearDown(self):
        '''Test case interval'''
        time.sleep(2)

    def test_a_reg(self):
        self.d.find_element_by_link_text('register').click()
        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        global account
        account = 'test' + str(times)
        print(account)
        self.d.find_element_by_id('username').send_keys(account)
        self.d.find_element_by_id('password').send_keys('test')
        self.d.find_element_by_id('password2').send_keys('test')
        time.sleep(self.time)
        x = '//*[@id="submit"]'
        self.d.find_element_by_xpath(x).click()

    def test_b_login(self):
        global account
        print("account:" + account)
        self.d.find_element_by_id('username').send_keys(account)
        self.d.find_element_by_id('password').send_keys('test')
        time.sleep(self.time)
        x = '//*[@id="submit"]'
        self.d.find_element_by_xpath(x).click()

    def get_xpath(self, answer_number):
        x = ['/html/body/div[3]/div[4]/span[2]',  # 0
             '/html/body/div[3]/div[3]/span[3]',  # 1
             '/html/body/div[3]/div[3]/span[2]',  # 2
             '/html/body/div[3]/div[3]/span[1]',  # 3
             '/html/body/div[3]/div[2]/span[1]',  # 4
             '/html/body/div[3]/div[2]/span[2]',  # 5
             '/html/body/div[3]/div[2]/span[3]',  # 6
             '/html/body/div[3]/div[1]/span[1]',  # 7
             '/html/body/div[3]/div[1]/span[2]',  # 8
             '/html/body/div[3]/div[1]/span[3]']  # 9
        return x[answer_number]

    def get_answer(self, q):
        with open('app/static/QA.txt', 'r', encoding="utf_8") as f:
            content = f.readlines()
        for line in content:
            line = line.strip()
            line = line.split('\t')
            if line[1] == q:
                print(line)
                answer = line[0]
                return answer

    def test_c_game(self):
        x = '//*[@id="game_shows"]/div/div/div[3]/button'
        self.d.find_element_by_xpath(x).click()
        x = '//*[@id="question"]'
        q = self.d.find_element_by_xpath(x).text
        print('q:' + q)
        answer = self.get_answer(q)
        for item in answer:
            print(item)
            x = self.get_xpath(int(item))
            self.d.find_element_by_xpath(x).click()
            # time.sleep(self.time)
        x = '/html/body/div[3]/div[4]/span[1]'
        self.d.find_element_by_xpath(x).click()  # Click Enter
        time.sleep(self.time)
        x = '/html/body/div[4]/div/div/div[3]/button'
        self.d.find_element_by_xpath(x).click()

    def test_d_theme_turn(self):
        self.d.find_element_by_id('theme_turn').click()
        time.sleep(self.time)
        self.d.find_element_by_id('theme_turn').click()

    def test_e_turn_password(self):
        global account
        newaccount = account + 'a'
        x = '/html/body/div[1]/div/span[3]/span[1]/a'
        self.d.find_element_by_xpath(x).click()
        self.d.find_element_by_id('username').send_keys(newaccount)
        self.d.find_element_by_id('password').send_keys('test1')
        self.d.find_element_by_id('password2').send_keys('test1')
        time.sleep(self.time)
        x = '//*[@id="submit"]'
        self.d.find_element_by_xpath(x).click()
        time.sleep(self.time)
        self.d.switch_to.alert.accept()


if __name__ == '__main__':
    import time, pytest

    pytest.main(
        [
            '--html=report/report.html',  # test report
            'webTest.py',
        ]
    )
