from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# 创建Chrome浏览器选项
chrome_options = Options()

# 创建Chrome浏览器驱动并设置选项
driver = webdriver.Chrome("C:/Users/ACDC/.cache/selenium/chromedriver/win64/125.0.6422.141/chromedriver.exe")  # 将"path_to_chromedriver"替换为你的Chrome驱动器的路径

# 导航到Google邮箱登录页面
driver.get("https://mail.google.com/")

# 找到登录表单的输入字段并输入邮箱地址
email_input = driver.find_element_by_id("identifierId")
email_input.send_keys("liszhouyou@gmail.com")  # 将"your_email@gmail.com"替换为你的邮箱地址

# 提交邮箱地址表单
email_input.send_keys(Keys.ENTER)

# 等待页面加载完成
driver.implicitly_wait(10)

# 找到密码输入字段并输入密码
password_input = driver.find_element_by_name("password")
password_input.send_keys("Mj672159.")  # 将"your_password"替换为你的邮箱密码

# 提交密码表单
password_input.send_keys(Keys.ENTER)

# 登录成功后，可以在这里执行其他操作，如发送邮件、查看收件箱等

# 关闭浏览器
driver.quit()