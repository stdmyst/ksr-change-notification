from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from email.message import EmailMessage

import smtplib
import time
import json
#import schedule


def send_mail(content):
    with open("../files/settings.json", encoding="UTF-8") as f:
        settings = json.load(f)
    
    (
        smtp_server, port, password,
        sender_email, receiver_email,subject
    ) = settings.values()
    
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.set_debuglevel(1)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()
    

def find_date():
    options = wd.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = wd.Chrome(options=options)
    driver.get("https://fgiscs.minstroyrf.ru/ksr")
    time.sleep(1)
    new_data_of_change = driver.find_element(By.CLASS_NAME, 'data-of-change').text
    
    with open("../files/ksr_change_notification.log", "r+", encoding="UTF-8") as file:
        print(new_data_of_change)
        if new_data_of_change not in file.read():
            file.seek(0)
            file.write(new_data_of_change.text)
            send_mail(f"Доступна новая версия КСР\r\n\n{new_data_of_change.text}\r\n\nСсылка на страницу загрузки: https://fgiscs.minstroyrf.ru/ksr")


#def job_that_executes_once():
#    find_date()
#    return schedule.CancelJob


if __name__ == "__main__":
#    schedule.every().second.do(job_that_executes_once)
#    schedule.every().day.do(find_date)
    
#    while True:
#        schedule.run_pending()
#        time.sleep(1)
    find_date()
