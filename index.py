from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from slugify import slugify
import os
import shutil

import time
import base64


# Function to create directory and copy PNG files
def create_directory_and_copy_files(text, source_directory, destination_directory):
    # Slugify the text to create a valid directory name
    slugified_text = slugify(text)
    
    # Create the destination directory if it doesn't exist
    destination_path = os.path.join(destination_directory, slugified_text)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Prepare a list to hold markdown links
    markdown_links = []

    # Get a list of all PNG files in the source directory, sorted by creation date
    png_files = [f for f in os.listdir(source_directory) if f.endswith(".png")]
    png_files.sort(key=lambda f: os.path.getctime(os.path.join(source_directory, f)))
    
    
    # Iterate over all files in the source directory
    for file_name in png_files:
        # Check if the file is a PNG file
        if file_name.endswith(".png"):
            # Build full file paths
            source_file = os.path.join(source_directory, file_name)
            destination_file = os.path.join(destination_path, file_name)
            
            # Copy the file
            shutil.copy(source_file, destination_file)
            print(f"Copied {file_name} to {destination_path}")

            # Add markdown link for the PNG file
            markdown_link = f"![{file_name}]({slugified_text}/{file_name})"

            markdown_links.append(f'# {file_name}')
            markdown_links.append(markdown_link)
            markdown_links.append('\n\n')


    # Create the markdown file in the current directory
    markdown_file_path = os.path.join(source_directory, f"{slugified_text}/{slugified_text}.md")
    with open(markdown_file_path, 'w') as md_file:
        # Write the markdown content with links to the images
        md_file.write("\n".join(markdown_links))
    
    print(f"Markdown file created at {markdown_file_path}")
    
    print(f"All PNG files have been copied to {destination_path}")

mainAccountEmail = 'minhbui.obu@gmail.com';
mainAccountPassword = 'Luoihoclacho9';

# Path to the GeckoDriver executable
geckodriver_path = '/snap/bin/geckodriver'

# Set up the Firefox driver
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service)


elsaMainPageEndpoint = 'https://speechanalyzer.elsaspeak.com/home';
recordingsEndpoint = 'https://speechanalyzer.elsaspeak.com/recordings';

driver.get(recordingsEndpoint)

# sign in

input_field = driver.find_element(By.CSS_SELECTOR, "input.form__input:nth-child(1)")

input_field.click()
input_field.send_keys(mainAccountEmail)

input_field = driver.find_element(By.CSS_SELECTOR, "input.form__input:nth-child(2)")

input_field.click()
input_field.send_keys(mainAccountPassword)

signInButton = driver.find_element(By.CSS_SELECTOR, "div.form__input-group:nth-child(5) > div:nth-child(1) > button:nth-child(2)")

signInButton.click()

time.sleep(3)

# ===


driver.get(recordingsEndpoint)
time.sleep(7)

recordingIds = []
urls = []

maxRecordingCountPerPage = 10

for pageIndex in [1, 2]:
  for recordingItemIndex in range (1, 11):
    currentRecordingItem = driver.find_element(By.CSS_SELECTOR, f'li.recording-item:nth-child({recordingItemIndex})')

    print(currentRecordingItem)

    currentRecordingItem.click()
    urls.append(driver.current_url)
    print(driver.current_url)

    time.sleep(2)

    driver.back()

    time.sleep(2)

  nextPageButton = driver.find_element(By.CSS_SELECTOR, f'li.page-item:nth-child(7)')

  nextPageButton.click()
  time.sleep(1)


# processing the first one
# urls = ['https://speechanalyzer.elsaspeak.com/recordings/673db6419430fa1760f7aa49']

waitForPageLoadSeconds = 15

for listIndex in range(len(urls)):
  recordingItemUrl = urls[listIndex]
  print(recordingItemUrl)

  driver.get(recordingItemUrl)
  time.sleep(waitForPageLoadSeconds)

  transcriptElementSelector = '.transcript__list'
  transcriptElement = driver.find_element(By.CSS_SELECTOR, f'{transcriptElementSelector}')

  driver.execute_script("arguments[0].style.overflow = 'visible';", transcriptElement)
  driver.execute_script("arguments[0].style['max-height'] = '10000px';", transcriptElement)

  transcriptItemsElements = transcriptElement.find_elements(By.CSS_SELECTOR, 'div')

  print(transcriptItemsElements, ' ' , len(transcriptItemsElements))
  minimumTranscriptItemsLength = 10

  while (len(transcriptItemsElements) < minimumTranscriptItemsLength):
    time.sleep(1)
    transcriptItemsElements = transcriptElement.find_elements(By.CSS_SELECTOR, 'div')

  transcriptItemsElements = transcriptElement.find_elements(By.CSS_SELECTOR, 'div')

  transcriptElement.screenshot('transcript.png')

  # ===

  intonationUrl = f'{recordingItemUrl}/intonation';

  driver.get(intonationUrl)
  time.sleep(waitForPageLoadSeconds)

  pitchChartApexChartCanvasElement = driver.find_element(By.CSS_SELECTOR, 'div[id^="apexchart"]')
  chartCanvasWidth = int(pitchChartApexChartCanvasElement.size['width'])
  print(chartCanvasWidth)

  chartWidth = (chartCanvasWidth * 2) + 500
  
  pitchChartElement = driver.find_element(By.CSS_SELECTOR, '.pitch-chart__chart')

  driver.execute_script(f"arguments[0].style['width'] = '{chartWidth}px';", pitchChartElement)

  pitchChartElement.screenshot('pitchchart.png')

  intonationTranscriptListElementSelector = '.transcript__list'
  intonationTranscriptListElement = driver.find_element(By.CSS_SELECTOR, intonationTranscriptListElementSelector)

  driver.execute_script("arguments[0].style.overflow = 'visible';", intonationTranscriptListElement)
  driver.execute_script("arguments[0].style['max-height'] = '10000px';", intonationTranscriptListElement)

  intonationTranscriptListElement.screenshot('intonation-transcript.png')

  # ===

  fluencyPageUrl = f'{recordingItemUrl}/fluency/pace'

  driver.get(fluencyPageUrl)
  time.sleep(waitForPageLoadSeconds)

  paceChartApexChartCanvasElement = driver.find_element(By.CSS_SELECTOR, 'div[id^="apexchart"]')
  chartCanvasWidth = int(paceChartApexChartCanvasElement.size['width'])
  print(chartCanvasWidth)
  chartWidth = (chartCanvasWidth * 2) + 500

  paceChartElement = driver.find_element(By.CSS_SELECTOR, '.line-chart__chart')

  driver.execute_script(f"arguments[0].style['width'] = '{chartWidth}px';", paceChartElement)

  paceChartElement.screenshot('pacechart.png')

  # ===

  pausingPageUrl = f'{recordingItemUrl}/fluency/pausing'

  driver.get(pausingPageUrl)
  time.sleep(waitForPageLoadSeconds)


  pausingChartApexChartCanvasElement = driver.find_element(By.CSS_SELECTOR, 'div[id^="apexchart"]')
  chartCanvasWidth = int(pausingChartApexChartCanvasElement.size['width'])
  print(chartCanvasWidth)
  chartWidth = (chartCanvasWidth * 2) + 500

  pausingChartElement = driver.find_element(By.CSS_SELECTOR, '.column-bar__chart')

  driver.execute_script(f"arguments[0].style['width'] = '{chartWidth}px';", pausingChartElement)

  pausingChartElement.screenshot('pausingchart.png')

  pausingTranscriptElementSelector = '.transcript__list'
  pausingTranscriptElement = driver.find_element(By.CSS_SELECTOR, f'{pausingTranscriptElementSelector}')

  driver.execute_script("arguments[0].style.overflow = 'visible';", pausingTranscriptElement)
  driver.execute_script("arguments[0].style['max-height'] = '10000px';", pausingTranscriptElement)

  pausingTranscriptItemsElements = pausingTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  print(pausingTranscriptItemsElements, ' ' , len(pausingTranscriptItemsElements))

  while (len(pausingTranscriptItemsElements) < minimumTranscriptItemsLength):
    time.sleep(1)
    pausingTranscriptItemsElements = pausingTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  pausingTranscriptItemsElements = pausingTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  pausingTranscriptElement.screenshot('pausingTranscript.png')

  # ===

  hesitationsPageUrl = f'{recordingItemUrl}/fluency/hesitations'

  driver.get(hesitationsPageUrl)
  time.sleep(waitForPageLoadSeconds)

  hesitationsChartApexChartCanvasElement = driver.find_element(By.CSS_SELECTOR, 'div[id^="apexchart"]')
  chartCanvasWidth = int(hesitationsChartApexChartCanvasElement.size['width'])
  print(chartCanvasWidth)
  chartWidth = chartCanvasWidth

  hesitationsChartElement = driver.find_element(By.CSS_SELECTOR, '.hesitations-chart__filler')

  driver.execute_script(f"arguments[0].style['width'] = '{chartWidth}px';", hesitationsChartElement)

  hesitationsChartElement.screenshot('hesitationschart.png')

  hesitationsTranscriptElementSelector = '.transcript__list'
  hesitationsTranscriptElement = driver.find_element(By.CSS_SELECTOR, f'{hesitationsTranscriptElementSelector}')

  driver.execute_script("arguments[0].style.overflow = 'visible';", hesitationsTranscriptElement)
  driver.execute_script("arguments[0].style['max-height'] = '10000px';", hesitationsTranscriptElement)

  hesitationsTranscriptItemsElements = hesitationsTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  print(hesitationsTranscriptItemsElements, ' ' , len(hesitationsTranscriptItemsElements))

  while (len(hesitationsTranscriptItemsElements) < minimumTranscriptItemsLength):
    time.sleep(1)
    hesitationsTranscriptItemsElements = hesitationsTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  hesitationsTranscriptItemsElements = hesitationsTranscriptElement.find_elements(By.CSS_SELECTOR, 'div')

  hesitationsTranscriptElement.screenshot('hesitationsTranscript.png')


  # ===

  grammarPageUrl = f'{recordingItemUrl}/grammar'

  driver.get(grammarPageUrl)
  time.sleep(waitForPageLoadSeconds)


  accordionGrammarRangeElement = driver.find_element(By.CSS_SELECTOR, '.grammar-range__accordion')
  accordionGrammarRangeElement.click()

  time.sleep(1)

  accordionGrammarRangeElement.screenshot('grammar-range.png')

  accordionYourTopGrammarErrorsElement = driver.find_element(By.CSS_SELECTOR, '.grammar-top-errors__accordion')
  accordionYourTopGrammarErrorsElement.click()


  # Find the parent element using the CSS selector
  sub_categories_parent_element = driver.find_element(By.CSS_SELECTOR, ".grammar-top-errors__accordion > dl:nth-child(1) > dd:nth-child(2)")
    
  # Find all direct children of the parent element
  children = sub_categories_parent_element.find_elements(By.XPATH, "./*")
    
  # Click on each child element
  for child in children:
      # Click the element
      child.click()
      
      # Wait briefly to observe the action (if needed)
      time.sleep(1)
  
  accordionYourTopGrammarErrorsElement.screenshot('your-top-grammar-errors.png')


  # ===

  vocabularyPageUrl = f'{recordingItemUrl}/vocabulary'

  driver.get(vocabularyPageUrl)
  time.sleep(waitForPageLoadSeconds)

  vocabularyElement = driver.find_element(By.CSS_SELECTOR, '.vocabulary__flexible')
  vocabularyElement.screenshot('vocabulary.png')

  recordingTitleTextElement = driver.find_element(By.CSS_SELECTOR, '.recording-title__text')
  recordingTitleRaw = recordingTitleTextElement.text
  print(recordingTitleRaw)

  slugified = slugify(recordingTitleRaw)
  print(slugified)

  create_directory_and_copy_files(slugified, '.', '.')





















print('final urls ', urls)








# Print the title of the page
print('Page Title:', driver.title)

time.sleep(5)
