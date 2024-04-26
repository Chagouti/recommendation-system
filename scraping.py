import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
titles = []

image_links=[]
descriptions=[]

genres=[]
i=0

for num in range(1,5):
  print('page ')
  print(num)
# Define the URL of the anime page to scrape
  url = f"https://www.anime-planet.com/anime/all?sort=status_1&order=desc&page={num}"

# Send an HTTP GET request to the URL
  response = requests.get(url)

# Check if the request was successful
  if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the table containing the anime data by inspecting the page source
    table = soup.find("ul", {"class": "cardDeck cardGrid"})


    # Create empty lists to store data



    # Iterate through the rows of the table
    for row in table.find_all("li"):
           a=row.find("a")
           div=a.find_all('div')
           img=div[0].find('img')
           if img:
               image_link = img["data-src"]
           else:
               image_link = "N/A" 
           image_links.append(image_link)
           h3=a.find_all('h3')
           title = h3[0].get_text(strip=True)
        
           titles.append(title)
           info=a['href']
           response = requests.get("https://www.anime-planet.com"+info)
           soup1 = BeautifulSoup(response.text, "html.parser")
           div1=soup1.find("div",{"class": "pure-1 md-3-5"})


           try:
               div2=div1.find_all('div')
               p=div2[0].find("p")
               description=p.get_text(strip=True)
               descriptions.append(description)


               try:
                
                   ul=div2[1].find('ul')
                   if ul:
                      genre=""
                      for row2 in ul.find_all("li"):
                          genre=genre+" , "+row2.get_text(strip=True)
                      genres.append(genre)
                   else:
                       genres.append('NaN')

               except AttributeError:
                   ul=div2[2].find('ul')
                   if ul:
        
                      genre=""
                      for row2 in ul.find_all("li"):
                          genre=genre+" , "+row2.get_text(strip=True)
                      genres.append(genre)
                   else:
                       genres.append('NaN')                

           except AttributeError:
               div2=div1.find_all('div')
               p=div1.find("p")
               description=p.get_text(strip=True)
               descriptions.append(description)
               ul=div2[0].find('ul')
               if ul:
        
                  genre=""
                  for row2 in ul.find_all("li"):
                     genre=genre+" , "+row2.get_text(strip=True)
                  genres.append(genre)
               else:
                   genres.append('NaN')          
        
           print(titles[i].encode("utf-8"))
           i=i+1
        

        
  


    
# Create a DataFrame from the collected data
data = {"Title": titles,"genres":genres,"overview":descriptions, "Poster":image_links}

df = pd.DataFrame(data)

    # Save the data to a CSV file
df.to_csv("top_animes28.csv", index=False)

print("Data has been scraped and saved to 'top_animes.csv'.")
