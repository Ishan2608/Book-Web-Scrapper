# Import required libraries
import requests
from bs4 import BeautifulSoup


# ------------------------------------------------------------------------
# USER DEFINED FUNCTIONS
# ------------------------------------------------------------------------

# Function to Format the user input name
def format_book_name(user_input):
  # Replace multiple consecutive spaces with a single space
  cleaned_input = ' '.join(user_input.split())

  # Replace spaces with '+' between words
  formatted_input = cleaned_input.replace(' ', '+')

  return formatted_input


# Function to Return List of all Books with this Name
def get_book_list(search_url):
  # send the request
  response = requests.get(search_url)
  # parse the HTML response received
  soup = BeautifulSoup(response.text, 'html.parser')
  # parse the response and find the required element
  left = soup.find('div', {'class': 'leftContainer'})
  tlist = left.find('table', {'class': 'tableList'})

  # Initialize a list to store the texts
  anchor_texts = []
  anchor_hrefs = []

  # Process each row in the tbody
  for row in tlist.find_all('tr', recursive=False):
    # Find the second td tag in the row
    second_td = row.find_all('td')[1]

    # Find the anchor tag inside the second td
    anchor_tag = second_td.find('a')

    # Get the anchor text and href
    anchor_text = anchor_tag.text.strip()
    anchor_href = anchor_tag['href']

    # Append the anchor text and href to the respective lists
    anchor_texts.append(anchor_text)
    anchor_hrefs.append(anchor_href)

  for ind in range(0, len(anchor_texts)):
    print(f"{ind + 1} - {anchor_texts[ind]}")

  print()
  
  choice = get_user_choice() - 1
  book_link = anchor_hrefs[choice]
  link = f"https://www.goodreads.com{book_link}"
  scrape_book_info(link)
  


# Function to get user choice
def get_user_choice():
  choice = int(input("Enter serial number for your choice: "))
  return choice


# Function to Scrap the Website
def scrape_book_info(book_url):
  # Make an HTTP request to the book URL
  response = requests.get(book_url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Extract relevant information
  title = soup.find('h1', {'data-testid': 'bookTitle'}).text.strip()
  author = soup.find('span', {'data-testid': 'name'}).text.strip()

  # Extract Summary
  summary = soup.find('span', {'class': 'Formatted'}).text.strip()

  # Extract Genres
  genre_div = soup.find('div', {'data-testid': 'genresList'})
  parent_ul = genre_div.find('ul', {'class': 'CollapsableList'})
  # Find the parent span with tabindex="-1"
  parent_span = parent_ul.find('span', {'tabindex': '-1'})
  # Extract text from all nested span elements
  genre = [
      span.text.strip()
      for span in parent_span.find_all('span', recursive=False)[1:]
  ]

  # Extract Ratings
  ratings = soup.find('div', {
      'class': 'RatingStatistics__rating'
  }).text.strip()

  # reviews = soup.find('span', {'itemprop': 'reviewCount'}).text.strip()

  # Display the information
  print(f'Title: {title}')
  print(f'Author: {author}')
  print(f'Genre: {genre}')
  print(f'Ratings: {ratings}')
  print(f'Summary:\n{summary}')
  # print(f'Reviews: {reviews}')


# ------------------------------------------------------------------------
# PROGRAM WORKFLOW
# ------------------------------------------------------------------------

# Example usage:
user_input = input("Enter the name of a book: ")
formatted_book_name = format_book_name(user_input)

search_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&query={formatted_book_name}"
get_book_list(search_url)
