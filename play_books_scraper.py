from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def extract(main_url,filename):
    uClient = uReq(main_url)
    main_html = uClient.read()
    uClient.close()
    main_soup = soup(main_html, "html.parser")
    cards = main_soup.findAll("div",{"class":"vU6FJ p63iDd"})
    f = open(filename, "w")

    headers = "title, author, publisher, date_published, ratings, pages, isbn, language, genres\n"

    f.write(headers)

    for card in cards:
        url = 'https://play.google.com' + card.a['href']
        print(url)
        client = uReq(url)
        book = client.read()
        client.close()
        book_soup = soup(book, "html.parser")
        container = book_soup.findAll("main",{"class":"LXrl4c"})
    
        title = container[0].findAll("h1",{"class":"AHFaub"})
        title = title[0].span.text

        author = container[0].findAll("span",{"class":"ExjzWd"})
        if len(author) == 0:
            author = ''
        elif type(author) == None:
            author = ''
        else:
            author = author[0].a.text

        info = container[0].findAll("span",{"class":"htlgb"})

        publisher = info[0].text
        date_published = info[1].text
        pages = info[2].text
        isbn = info[3].text
        language = info[6].text
        genres = info[7].text

        ratings = container[0].findAll("div",{"class":"BHMmbe"})
        if len(ratings) == 0:
            ratings = 0
        else:
            ratings = ratings[0].text

        try:
            f.write(title.replace(",","|") + ',' + author.replace(",","|") + ',' + publisher.replace(",","|") + ',' + date_published.replace(",","|") + ',' + str(ratings) + ',' + pages + ',' + isbn + "," + language + ',' + genres.replace(",","|") + "\n")
        except UnicodeEncodeError:
            continue

    print(filename + " written on disk....")

    f.close()