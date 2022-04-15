from selenium import webdriver
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# The excel sheet is in the form of 11 cells starting from 0 count, so 0-10
# In order:
#   date(0), building(1), interaction(2), nickname(3), searchable name(4), priority(5), topics(6), notes(7), specify other(8), contact method(9), reason of no contact(10)
# Example:
#   || 04/01/2022 || abel south || 7 || Parker Nicholas Brown || Brown, Parker Nicholas || low || summer plans, transition, time management || "" || "" || scheduled || "" ||

email_username = config('email_user', default='')
unl_password = config('unl_pass', default='')
with open('AutomationRAForms\data.csv', 'r') as csv_file:
  csv_reader = csv.reader(csv_file)


  ############### Automated Login ###############
  web_form = webdriver.Chrome()
  web_form.get('https://unl.erezlife.com/')
  web_form.maximize_window()
  # Helper method that switches the iframe by id
  def frame_switch_id(id): 
    web_form.switch_to.frame(web_form.find_element_by_id(id))

  # Sign into MyRed Account based on local .env information
  web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div/main/form/fieldset/div[1]/div/input').send_keys(email_username)
  web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div/main/form/fieldset/div[2]/div/input').send_keys(unl_password)
  web_form.find_element_by_name("_eventId_proceed").send_keys(u'\ue007')
  time.sleep(1)
  # Switch to the duo mobile iframe and send a push notification for two factor authentication
  frame_switch_id("duo_iframe")
  web_form.find_element_by_xpath('//button[text()="Send Me a Push "]').click()
  time.sleep(10)


  ############### Filling out the form ###############
  for line in csv_reader:
    web_form.switch_to.default_content()
    # Click on the Intentional Interaction tab
    web_form.find_element_by_link_text("Intentional Interaction").click()
    time.sleep(1)


    # Pick date from CSV file
    date = line[0]
    building = line[1]
    buildings = {
    'abel north': 'gensec_location-5969',
    'abel south': 'gensec_location-5970',
    'kauffman': 'gensec_location-5973',
    'sandoz': 'gensec_location-5971',
    'selleck': 'gensec_location-5972',
    'love': 'gensec_location-5981',
    'massengale': 'gensec_location-5980',
    'harper': 'gensec_location-5967',
    'schramm': 'gensec_location-5965',
    'smith': 'gensec_location-5966',
    'village': 'gensec_location-5958',
    'courtyards': 'gensec_location-5978',
    'eastside': 'gensec_location-5977',
    'knoll': 'gensec_location-5975',
    'suites': 'gensec_location-5976'
    }
    # Enter the date into the date field
    web_form.find_element_by_id("gensec_form_date_from").send_keys(date)
    # Select the building the form is meant for
    web_form.find_element_by_id(buildings[building]).click()
    # Scroll down to focus on the next part of the form
    web_form.find_element_by_class_name("subsection-label").location_once_scrolled_into_view
    # Create a dictionary of interaction instances and their values from the HTML listed values
    interaction = line[2]
    interaction_instance = {
    '1': '1403',
    '2': '1404',
    '3': '1405',
    '4': '1406',
    '5': '1973',
    '6': '1974',
    '7': '1975',
    '8': '1976'
    }
    select_instance = Select(web_form.find_element_by_xpath("/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[2]/td[2]/div/select"))
    # Select the interaction instance
    select_instance.select_by_value(interaction_instance[interaction])


    # Enter name of the resident (nickname just forward) into search bar
    web_form.find_element_by_name("ps_pattern").send_keys(line[3])
    # Click on the search spyglass button to search for the resident
    web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[3]/td[2]/div/div[2]/div/img[1]').click()
    time.sleep(2)
    # Find the box containing all the names in the list
    names_in_search_box = web_form.find_element_by_xpath("/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[3]/td[2]/div/div[2]/ul")
    # Find every name that appears in the search box list element
    options = names_in_search_box.find_elements_by_tag_name("li")
    time.sleep(2)
    # Loop through each name and find the name that matches the listed name for the resident exactly
    for option in options:
        current_name = option.get_attribute('innerText')
        if (current_name == line[4]):
          # Once the correct name is found, select on the name and stop searching
          option.click()
          break
    

    # Create a dictionary of all follow up priority values
    priority = line[5]
    priority_list = {
    'low': '1426',
    'medium': '1427',
    'high': '1428'
    }
    # Select the priority box
    select_priority_followup = Select(web_form.find_element_by_xpath("/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[4]/td[2]/div/select"))
    # Select the intended priority for the resident
    select_priority_followup.select_by_value(priority_list[priority])


    # Select the extra option drop down '+' button
    web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[5]/td[2]/div/div[1]/button').click()
    time.sleep(2)
    # Find the ul HTML list holder
    topics_list = web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[5]/td[2]/div/div[2]/ul')
    # Find all of the li elements for checkboxes
    topics = topics_list.find_elements_by_tag_name("label")
    time.sleep(2)
    # Loop through all of the listed topics. If a topic in the dictionary is found in the given data cell check the box related to the topic
    x = 1
    for topic in topics:
      # If the word appears in the given data cell click on the associated text box
      current_topic = topic.get_attribute('innerText')
      if (current_topic in line[6]):
        topic.click()
      x += 1
    # Input any meeting notes into the notes textbox
    web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[6]/td[2]/div/textarea').send_keys(line[7])
    # Check if 'other' was selected for specification
    if ('other' in line[6]):
      web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[7]/td[2]/div/input').send_keys(line[8])


    # Select method of communication
    contact_method = line[9]
    method_of_communication_list = {
    'scheduled': '1739',
    'spontaneous': '1740',
    'zoom': '1741',
    'text': '1742',
    'no show': '1743',
    'could not reach': '1744'
    }
    # Select the priority box
    select_method_communication = Select(web_form.find_element_by_xpath("/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[8]/td[2]/div/select"))
    # Select the method of communication for the interaction
    select_method_communication.select_by_value(method_of_communication_list[contact_method])
    # Check if resident could not be reached
    if (method_of_communication_list[contact_method] == '1744'):
      web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[1]/table/tbody[3]/tr[9]/td[2]/div/textarea').send_keys(line[10])
    # Click on the RD review button
    web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/div[2]/form/div[2]/div/button[2]').click()
    time.sleep(1)
    # Select Tobey Brockman checkbox
    rd_checkbox = web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/form/ul/li/div/div/ul/li[2]/input')


    # Find and assign the submit button to a variable
    submit = web_form.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/main/form/div/div/button')
    # Check if the box is already selected, and if it is, continue onward without selecting the box again on accident
    if (rd_checkbox.is_selected):
      submit.click()
    else:
      rd_checkbox.click()
      submit.click()

# Once finished, quit by closing the browser
web_form.quit()

#TODO : ADD SRA SELECTION LOGIC
#TODO : ADD SPECIFIC SELECTION LOGIC FOR ANY MEMBER OF STAFF