from Selenium import InternetSpeedTwitterBot, PROMISED_UP, PROMISED_DOWN

selenium = InternetSpeedTwitterBot()

selenium.get_internet_speed()
if selenium.up < PROMISED_UP or selenium.down < PROMISED_DOWN:
    selenium.tweet_at_provider()
