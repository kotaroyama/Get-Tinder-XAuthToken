# Get Tinder XAuthToken

## Usage
**NOTE**: You need to register your Facebook account with Tinder first.

The script will ask for your Facebook email and password, and retrieves the Tinder XAuthToken automatically using the automated browser (Google Chrome via Selenium). You probably already have Google Chrome on your computer but if not, you will need to install it. 

## Motivation
I started working on [TinderImageDownloader](https://github.com/kotaroyama/TinderImageDownloader) in 2018, but I realized it is a pain to get the access token and needed something that does it without moving my hands.

Selenium is a library used to run automated tests on broswer, but I decided to use it to automate the process of retrieving the token in this project.

## Dependencies
You need to have a few python packages. I believe all of them can be downloaded via pip. Specifically, you will need: 

- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDrive - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/) 
