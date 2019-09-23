from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from flask import Blueprint
# tests/front_end_tests.py
import time
import re
import unittest
import urllib.request as urllib2
from flask_bootstrap import Bootstrap
from flask_testing import LiveServerTestCase
from selenium import webdriver
from flask import Flask, url_for




class TestBase(LiveServerTestCase):

    def create_app(self):
        import application
        application.app.config.update(
            # Change the port that the liveserver listens on
            LIVESERVER_PORT=8943
        )
        return application.app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Firefox()
        self.driver.get(self.get_server_url())
        

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
    
    
   
      
class TestLogin(TestBase):
    
    def test_login(self):
    	test_employee1_email="ayushbansal323@gmail.com"
    	test_employee1_password="a1as2sd3d"
    	self.driver.find_element_by_id("inputEmail").send_keys(test_employee1_email)
    	self.driver.find_element_by_id("inputPassword").send_keys(test_employee1_password)
    	self.driver.find_element_by_xpath("//*[@type = 'submit']").click()
    	time.sleep(10)
    	# Assert that browser redirects to dashboard page
    	assert url_for('home') in self.driver.current_url
    
    def test_login_fail1(self):
    	test_employee1_email="ayush@gmail.com"
    	test_employee1_password="a1as2s"
    	self.driver.find_element_by_id("inputEmail").send_keys(test_employee1_email)
    	self.driver.find_element_by_id("inputPassword").send_keys(test_employee1_password)
    	self.driver.find_element_by_xpath("//*[@type = 'submit']").click()
    	time.sleep(10)
    	
    	src = self.driver.page_source
    	text_found = re.search(r'The username does not exist', src)
    	self.assertNotEqual(text_found, None)
    	
    def test_login_fail2(self):
    	test_employee1_email="ayushbansal323@gmail.com"
    	test_employee1_password="a1as2s"
    	self.driver.find_element_by_id("inputEmail").send_keys(test_employee1_email)
    	self.driver.find_element_by_id("inputPassword").send_keys(test_employee1_password)
    	self.driver.find_element_by_xpath("//*[@type = 'submit']").click()
    	time.sleep(10)
    	
    	src = self.driver.page_source
    	text_found = re.search(r'The username or password does not match', src)
    	self.assertNotEqual(text_found, None)
    
    def test_page_excess(self):
    	response = urllib2.urlopen("http://127.0.0.1:8943/book/039925675X")
    	assert url_for('home') not in self.driver.current_url

class CreateObjects(object):

    def login_user(self):
    	test_employee1_email="ayushbansal323@gmail.com"
    	test_employee1_password="a1as2sd3d"
    	self.driver.find_element_by_id("inputEmail").send_keys(test_employee1_email)
    	self.driver.find_element_by_id("inputPassword").send_keys(test_employee1_password)
    	self.driver.find_element_by_xpath("//*[@type = 'submit']").click()
    	time.sleep(12)

class TestHome(CreateObjects, TestBase):
		
	def test_search_by_year(self):
		self.login_user()
		test_year="1998"
		select = Select(self.driver.find_element_by_id('submitSelector'))
		select.select_by_visible_text('year')
		self.driver.find_element_by_id("inputSearch").send_keys(test_year)
		self.driver.find_element_by_id("submitSearch").click()
		time.sleep(8)
		
	def test_search_by_title(self):
		self.login_user()
		test_title="Steve Jobs"
		select = Select(self.driver.find_element_by_id('submitSelector'))
		select.select_by_visible_text('title')
		self.driver.find_element_by_id("inputSearch").send_keys(test_title)
		self.driver.find_element_by_id("submitSearch").click()
		time.sleep(10)
		src = self.driver.page_source
		text_found = re.search(r'Steve Jobs', src)
		self.assertNotEqual(text_found, None)
		
	def test_search_by_author(self):
		self.login_user()
		test_author="Walter Isaacson"
		select = Select(self.driver.find_element_by_id('submitSelector'))
		select.select_by_visible_text('author')
		self.driver.find_element_by_id("inputSearch").send_keys(test_author)
		self.driver.find_element_by_id("submitSearch").click()
		time.sleep(10)
		src = self.driver.page_source
		text_found = re.search(r'Walter Isaacson', src)
		self.assertNotEqual(text_found, None)
		
	def test_search_by_isbn(self):
		self.login_user()
		test_isbn="1451648537"
		self.driver.find_element_by_id("inputSearch").send_keys(test_isbn)
		self.driver.find_element_by_id("submitSearch").click()
		time.sleep(10)
		src = self.driver.page_source
		text_found = re.search(r'Walter Isaacson', src)
		self.assertNotEqual(text_found, None)
	
	def test_click_book(self):
		self.login_user()
		response = urllib2.urlopen("http://127.0.0.1:8943/book/039925675X")
		self.assertEqual(response.code, 200)
	
if __name__ == '__main__':
    unittest.main()
