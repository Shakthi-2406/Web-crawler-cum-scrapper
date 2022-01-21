from bs4 import BeautifulSoup
import requests, csv

paginator = 1 #paginator to start with

csvfile =  open("data.csv", "w", encoding='utf-8', newline="") 
writer = csv.writer(csvfile)
writer.writerow(["TITLE","LINK"])

while requests.get(f'https://www.coursef.com/course?page={paginator}').text: #will be true until the page exists (goes till last page)
    source = requests.get(f'https://www.coursef.com/course?page={paginator}').text
    soup = BeautifulSoup(source, 'lxml')

    for div in soup.find_all('div', class_='col-md-3'):

        for link in div.find_all('a', class_='stretched-link'):
            course_link_val = link.get('href')
            course_title_source = requests.get(course_link_val).text
            soup1 = BeautifulSoup(course_title_source, 'lxml')
            course_link = course_link_val
            sample_title = "No Title"
            try:
                title = soup1.find('h1').text.encode("utf-8").decode()
            except AttributeError: #if the course is without title. I found one at "https://www.coursef.com/course?page=14"
                title = sample_title.encode("utf-8").decode()

            writer.writerow([title,course_link])
    paginator += 1

csvfile.close()
