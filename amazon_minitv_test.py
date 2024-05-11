import time

import pytest
from appium import webdriver


@pytest.fixture(scope="class")
def setup(request):
    desired_caps = {
        "platformName": "Android",
        "deviceName": "NikhilPhone",
        "appPackage": "com.android.vending",
        "appActivity": "com.amazon.minitv.android.app.activities.MiniTVMainActivity",
        "automationName": "UiAutomator2"
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()


@pytest.mark.usefixtures("setup")
class TestAmazonMiniTV:

    def test_open_amazon_mini_tv(self):
        app_opened = self.driver.find_element().size
        assert len(app_opened) > 0, "App is not opened successfully"
        pass

    def test_select_series(self):
        series_element = self.driver.find_element("xpath",
                                                  "//android.widget.LinearLayout[1]")
        series_element.click()

        time.sleep(2)
        series_details_page_element = self.driver.find_element("xpath",
                                                               "//android.widget.TextView[@text='Series Details']")
        assert series_details_page_element.is_displayed(), "Series details page is not opened"

        print("Series details page is opened successfully")
        pass

    def test_play_first_episode(self):
        seasons = self.driver.find_elements("xpath", "//android.widget.TextView[contains(@text, 'Season')]")

        for season in seasons:
            season.click()
            time.sleep(2)
            first_episode = self.driver.find_element("xpath", "//android.widget.TextView[contains(@text, 'Episode 1')]")
            first_episode.click()

            time.sleep(10)

            video_playing = self.driver.find_element("xpath", "//android.widget.VideoView")
            assert video_playing.is_displayed(), "Video is not playing"
            print("Video is playing for Season:", season.text)

        pass


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])
