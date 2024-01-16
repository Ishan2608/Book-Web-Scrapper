# Import required libraries
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

# ------------------------------------------------------------------------
# USER DEFINED FUNCTIONS
# ------------------------------------------------------------------------


# Function to Format the user input name
def format_book_name(user_input):
  """
  Formats the name of the book such that it can be passed as query parameter
  in the website url.
  Example: Book Name -> sherlock holmes. Formatted String -> sherlock+holmes
  Parameters:
    user_input: string
  Returns:
    formatted_book_name: string
  """
  # Replace multiple consecutive spaces with a single space
  cleaned_input = ' '.join(user_input.split())

  # Replace spaces with '+' between words
  formatted_input = cleaned_input.replace(' ', '+')

  return formatted_input


# Function to get user choice
def get_user_choice():
  """
  Gets the user choice after a menu has been printed based on the book name
  Returns:
    user_choice: integer
  """
  print()
  choice = int(input("Enter serial number for your choice(e.g. 1): "))
  return choice


# Function to print a dictionary that contains book information
def print_dict(book_info):
  """
  Prints the book information with each key and its value in a new line.
  Parameter:
    book_info: dictionary
  """
  for key in book_info:
    print(f"{key}: {book_info[key]}")
  print()


# Function to print info of all books in the form of a table
def print_table(link_list):
  """
  Prints the book information in a table format using PrettyTable library.
  Parameter:
    link_list: list of URLs
  (WORK IN PROGRESS)
  """
  table = PrettyTable()
  table.field_names = [
      "Index", "Title", "Author", "Genre", "Ratings", "Summary"
  ]
  for i in range(0, len(link_list)):
    link_ = f"https://www.goodreads.com{link_list[i]}"
    book = scrape_book_info(link_)
    table.add_row([
        i + 1, book['Title'], book['Author'], book['Genre'], book['Ratings'],
        book['Summary']
    ])
  print(table)


# Function to Scrap the Website
def scrape_book_info(book_url):
  """
  Scrapes the book information from the website and returns a dictionary with the keys: title, author, genre, ratings, and summary.
  Parameter:
    book_url: string (URL of the book)
  Returns:
    book_info: dictionary
  """
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

  return {
      'Title': title,
      'Author': author,
      'Genre': genre,
      'Ratings': ratings,
      'Summary': summary
  }


# Function to scrape all books in the list
def scrape_all(link_list):
  """
  Runs a loop to scrape all the books in the list by calling the scrape_book_info function.
  Parameter:
    link_list: list of URLs
  """
  for i in range(0, len(link_list)):
    link_ = f"https://www.goodreads.com{link_list[i]}"
    book_info = scrape_book_info(link_)
    print_dict(book_info)


# Function to Return List of all Books with this Name
def get_book_list(search_url):
  """
  Fetches a list of book URLs from the search results page based on the keywords entered by the user. Aslo gets the list of corresponding links.
  Parameters:
    search_url: string (URL of the search results page)
  """
  # send the request
  response = requests.get(search_url)
  # parse the HTML response received
  soup = BeautifulSoup(response.text, 'html.parser')
  # parse the response and find the required element
  left = soup.find('div', {'class': 'leftContainer'})
  check = soup.find('h3', {'class': 'searchSubNavContainer'}).text.strip()

  # Check if the website returned any list of books
  if (check == 'No results.'):
    print("No results found for this search. 😭😭😭😭😭")
    return
    
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

  print("0 - Show Info for ALL")
  for ind in range(0, len(anchor_texts)):
    print(f"{ind + 1} - {anchor_texts[ind]}")

  print()

  choice = get_user_choice() - 1
  if (choice == -1):
    scrape_all(anchor_hrefs)
    # print_table(anchor_hrefs)

  else:
    book_link = anchor_hrefs[choice]
    link = f"https://www.goodreads.com{book_link}"
    book_info = scrape_book_info(link)
    print_dict(book_info)


# ------------------------------------------------------------------------
# PROGRAM WORKFLOW
# ------------------------------------------------------------------------

# Example usage:
user_input = input("Enter the name of a book: ")
formatted_book_name = format_book_name(user_input)

search_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&query={formatted_book_name}"
get_book_list(search_url)
