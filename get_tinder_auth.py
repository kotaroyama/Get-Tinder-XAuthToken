"""Retrieves a Tinder XAuthToken for a registered user"""
import time
import re

from getpass import getpass

from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


def display_warning():
    """Displays warning other info"""
    print("Get Tinder Access Token - Retrieves a Tinder XAuthToken")
    print("Author: Kotaro Yama (kotaro.h.yama@gmail.com)")
    print("\nNOTE: You need to have registered on Tinder app or website with your Facebook account first\n")
    print("\nAlso, you do not have to do anything while the browser is doing its job.")

def parse_auth(html_doc):
    """Parses the access_token out of the html page"""
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
    """Retrieves the XAuthToken using the access_token_string"""
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

def main():
    display_warning()
    
    # Option to block the notification popup (for Google Chrome)
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    # Iterate the loop until the user enters correct email and password
    while True:
        try:
            # Login info (Facebook)
            email_adrs = input('Email: ')
            password = getpass() 

            # Automatically installs the chrome driver
            chromedriver_autoinstaller.install() 
            driver = webdriver.Chrome()
            driver.get("https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&client_id=464891386855067&ret=login&fallback_redirect_uri=221e1158-f2e9-1452-1a05-8983f99f7d6e&ext=1556057433&hash=Aea6jWwMP_tDMQ9y")

            # Email input
            email_text = driver.find_element_by_id("email")
            email_text.send_keys(email_adrs)
            # Password input
            password_text = driver.find_element_by_id("pass")
            password_text.send_keys(password)

            # Submit
            password_text.submit()

            # Get the continue button
            time.sleep(3)
            continue_button = driver.find_element_by_css_selector('.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.pq6dq46d.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.cbu4d94t.taijpn5t.k4urcfbm')

            break
        except Exception as e:
            driver.close()
            print('Incorrect credential, try again...\n')

    continue_button.click()

    # page_source property has the html source
    long_token = parse_auth(driver.page_source)

    # Close the driver for the long token
    driver.close()

    # Print out the XAuthToken
    xauth = get_xauth_token(long_token)['data']['api_token']
    print(f"\nXAuthToken: {xauth}")

if __name__ == '__main__':
    main()
