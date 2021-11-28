import requests_html
from bs4 import BeautifulSoup
import requests
import time
import os
test_url1 = "https://mangatx.com/manga/heaven-defying-sword/chapter-1/"
test_url2 = "https://mangatx.com/manga/heaven-defying-sword/"


def make_chapter_url(link, chapter_number):
    manga_name = link.split('manga/')[1].split('/chapter-')[0]
    return  "https://mangatx.com/manga/{}/chapter-{}".format(manga_name,chapter_number)



def get_manga_name(link):
    manga_name = link.split('manga/')[1].split('/chapter-')[0].replace('-',' ')
    print("manga_name = " + str(manga_name))
    return manga_name



def save_chapter_image(chapter_images,name,number):
    ses = requests.session()

    if os.path.isdir("./{}".format(str(name))) == False:
        os.mkdir("./{}".format(str(name)))
    cur_dir = "./{}/chapter {}".format(name,str(number))
    if os.path.isdir(cur_dir) == False:
        os.mkdir(cur_dir)
    count = 1
    time.sleep(0.2)
    #"{}.jpg".format(count),"wb"
    for img in chapter_images:
        res = ses.get(img)
        with open("{}/{}.jpg".format(cur_dir,count),"wb") as f:
            f.write(res.content)
            print(count)
        count += 1












def scrape_a_chapter(url):
    session = requests_html.HTMLSession()

    response = session.get(url)
    response.html.render(timeout=10)

    soup = BeautifulSoup(response.content,"html.parser")
    x = soup.find_all('div',attrs={"class":"page-break no-gaps"})
    chapter = []
    for tag in x:
        image = tag.find('img')['data-src']
        print(image)
        chapter.append(image)
    return chapter


#wp-manga-chapter

def get_chapters_number(url):
    session = requests_html.HTMLSession()

    response = session.get(url)
    response.html.render(timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    x = soup.find_all('li', attrs={"class": "wp-manga-chapter"})[0].find('a').contents[0].replace('Chapter','')
    return int(x)



def download_manga(url):
    latest_chapter = get_chapters_number(url)
    print(latest_chapter)
    for i in range(1,latest_chapter+1):
        chapter_link = make_chapter_url(url,i)
        print("Chapter Link: " + str(chapter_link))
        list_of_images_link = scrape_a_chapter(chapter_link)
        save_chapter_image(list_of_images_link,get_manga_name(url),i)
        print("done")
        time.sleep(0.09)


url11 = input("mangatx url: ")

download_manga(url11)

