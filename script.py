import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#Add a cover letter suitable for the selected role
cover_story = '''
I am writing to express my keen interest in the Python Developer Intern role at [Company Name]. 
Currently pursuing a [Your Degree] in Computer Science, I have a solid foundation in Python and relevant 
frameworks like Django and Flask.
Eager to contribute my skills to your innovative team, 
I have successfully completed projects showcasing problem-solving abilities and collaboration. 
Excited about [Company Name]'s commitment to cutting-edge technologies, I believe my proficiency 
in Python aligns well with your goals.
Thank you for considering my application. I am enthusiastic about contributing to [Company Name]'s success
as a Python Developer Intern.
'''

#specify the role and desired minimum stipend
role = 'python developer'
desired_min_stipend = 10000

driver = webdriver.Firefox()

driver.get('https://internshala.com')

login = driver.find_element(by=By.CLASS_NAME, value='login-cta')
login.click()

email = driver.find_element(by=By.ID, value='modal_email')
#Provide your email registered in internshala
email.send_keys('youremail@example.com')
password = driver.find_element(by=By.ID, value='modal_password')
#Password for your account
password.send_keys('password')

time.sleep(5)
submit = driver.find_element(by=By.ID, value='modal_login_submit')
submit.click()

time.sleep(10)
internships_page = driver.find_element(by=By.ID, value='internships_new_superscript')
internships_page.click()

search_box = driver.find_element(by= By.ID, value='keywords')
submit = driver.find_element(by=By.ID, value='search')

search_box.send_keys(role)
time.sleep(3)
submit.click()

visited = set()

time.sleep(5)
while True:
    internships = driver.find_elements(by=By.CLASS_NAME, value='container-fluid.individual_internship.visibilityTrackerItem ')
    if len(internship) == 0:
        break
    for internship in internships:
        if internship in visited:
            continue
        location = internship.find_element(by=By.CLASS_NAME, value='location_link.view_detail_button')
        if location.text != 'Work From Home':
            continue
        stipend = internship.find_element(by=By.CLASS_NAME, value='stipend')
        value = int(re.findall('\d+', ''.join(stipend.text.split()[1].split(',')))[0])
        if value < desired_min_stipend:
            continue
        apply = internship.find_element(by=By.CLASS_NAME, value='btn.btn-primary.easy_apply.button_easy_apply_t')
        apply.click()
        time.sleep(3)
        continue_button = driver.find_element(by=By.ID, value='continue_button')
        continue_button.click()
        time.sleep(3)

        try:
            assessment = driver.find_element(by=By.CLASS_NAME, value='form-group.additional_question').is_displayed()
            if assessment:
                visited.add(internship)
                close = driver.find_element(by=By.ID, value='easy_apply_modal_close')
                close.click()
                confirm_close = driver.find_element(by=By.ID, value='easy_apply_modal_close_confirm_exit')
                confirm_close.click()
                continue
        except NoSuchElementException:
            pass

        cover_letter = driver.find_element(by=By.CLASS_NAME, value='ql-editor')
        cover_letter.send_keys(cover_story)

        confirm = driver.find_element(by=By.ID, value='submit')
        time.sleep(2)
        confirm.click()
        print('application successful!')
        time.sleep(3)

        apply_more = driver.find_element(by=By.ID, value='backToInternshipsCta')
        apply_more.click()
        time.sleep(3)
        break

driver.quit()