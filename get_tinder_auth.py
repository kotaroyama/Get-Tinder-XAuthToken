import time
import re
import requests

from getpass import getpass

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def parse_auth(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Find the script tag that has window.location.href
    #   There seem to be two <script> tags in the html
    #   The one that contains the acccess_token has a type attribute, and the
    #   other one doesn't.
    script_content = soup.find(type="text/javascript").string

    # Extract the regular expression match of the access_token and get the match string
    access_token_string = re.search('access_token=[a-zA-Z0-9]*&', script_content).group(0)

    # Polish the regular string again
    access_token_string_modified = re.search('[a-zA-Z0-9]*&', access_token_string).group(0)
    access_token_string_final = re.search('[a-zA-Z0-9]*', access_token_string_modified).group(0)

    return access_token_string_final

def get_xauth_token(long_token):
    USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"

    HEADERS = {
        'app_version': '6.9.4',
        'platform': 'ios',
        "content-type": "application/json",
        "User-agent": USER_AGENT,
        "Accept": "application/json"
    }

    new_url = 'https://api.gotinder.com/v2/auth/login/facebook'
    new_data = {"token": long_token}
    r_new = requests.post(new_url, headers=HEADERS, json=new_data)

    return r_new.json()

def sleep_for_x_secs(sec):
    sec = 500
    time.sleep(sec)

def main():
    # Option to block the notification popup (for Google Chrome)
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    # Login info (Facebook)
    email_adrs = input('Please enter your email: ')
    password = getpass() 

    driver = webdriver.Chrome(options=option)
    driver.get("https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y")

    while True:
        # Email input
        email_text = driver.find_element_by_id("email")
        email_text.send_keys(email_adrs)
        # Password input
        password_text = driver.find_element_by_id("pass")
        password_text.send_keys(password)

        try:
            # Submit
            password_text.submit()
            break
        except selenium.common.exceptions.NoSuchElementException:
            print("Incorrect credential")

    # Get the OK button (To allow Tinder Auth)
    ok_button = driver.find_element_by_name("__CONFIRM__")
    ok_button.submit()

    # page_source property has the html source
    long_token = parse_auth(driver.page_source)

    # Close the driver for the long token
    driver.close()

    # Print out the JSON object
    xauth = get_xauth_token(long_token)
    print(xauth)

if __name__ == '__main__':
    main()