# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()


    def test_landing_page_title(self):
        print("DEBUG 1")
        driver = self.driver
        driver.get("http://0.0.0.0:8090")
        #print(driver)
        self.assertIn("CS673", driver.title)
        #elem = driver.find_element_by_name("q")
        #elem.send_keys("pycon")
        #elem.send_keys(Keys.RETURN)
        assert "Job Statistics Portal" in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
