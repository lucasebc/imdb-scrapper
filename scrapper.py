from asyncore import write
from math import floor, ceil
import os

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup, PageElement

from mail import writeMail, sendMail

# imdb_url = 'https://www.imdb.com/search/title/?num_votes=0,&sort=num_votes,desc'
        # https://www.imdb.com/search/title/?num_votes=0,&sort=num_votes,desc&start=51&ref_=adv_nxt
        # https://www.imdb.com/search/title/?title_type=feature&num_votes=0,&sort=num_votes,desc&count=250

movies = [] # list of movies according to the value defined in NUM_MOVIES

NUM_MOVIES  = 2000                  # number of movies to search
COUNT       = 250                   # number of movies per page
NUM_PAGES   = NUM_MOVIES / COUNT    # number pages to search

imdb_search_url = 'https://www.imdb.com/search/title/?' # complete url of advanced search
params = {
    'title_type': 'feature',    # filter: type of content: feature movie
    'num_votes': '0,',          # filter: from number of votes: 0
    'sort': 'num_votes,desc',   # sort by: number of votes
    'count': '250',             # number of items per page: 250 (max)
    'start': '0',               # start from item number
    'ref_': 'adv_nxt',          # reference page: adv_next: move forward, adv_prv: maico jacson
}
classes = {
    'movies': 'lister-list',                # .lister-list
    'movie': 'lister-item',                 # .lister-list > .lister-item
    'title': 'lister-item-header',          # .lister-list > .lister-item > .list-item-header > a / children[1]
    'year': 'lister-item-year',             # .lister-list > .lister-item > .list-item-header > .lister-item-year
    'user_score': 'ratings-imdb-rating',    # .lister-list > .lister-item > .ratings_bar > ratings-imdb-rating
    'metascore': 'metascore',               # .lister-list > .lister-item > .ratings_bar > ratings-metascore > metascore
    'num_votes': 'sort-num_votes-visible',  # .lister-list > .lister-item > .sort-num_votes-visible > span[name=nv][0]
    'image': 'lister-item-image'            # .lister-list > .lister-item > .lister-item-image > a > img
}

# for each page, mount the imdb url, open it and get the fields from the movie list
for i in range(0, ceil(NUM_PAGES)):
    params['start'] = str(COUNT * i)

    final_url = imdb_search_url

    for param_key, param_value in params.items():
        if(param_key == 'start' and param_value > '0'):
            final_url += param_key + '=' + str(int(params[param_key])+1) + '&'
        else: final_url += param_key + '=' + param_value + '&'


    final_url = final_url[:-1] #remover ultimo &
    print(final_url)

    html = urlopen(final_url)
    bs = BeautifulSoup(html, 'lxml')

    # movies = bs.find_all(attrs={"data-testid": "WeatherDetailsLabel"}, string='Max. / Mín.')[0]

    movie_list_html = bs.find_all(class_=classes['movie'])

    counter = int(params['start'])
    for movie_html in movie_list_html:
        if counter < NUM_MOVIES:
            movie = dict()
            counter += 1
            try:
                movie['id']             = str(counter)
                movie['title']          = movie_html.find(class_=classes['title']).a.get_text().strip()
                movie['year']           = movie_html.find(class_=classes['year']).get_text().strip()[-5:-1]
                movie['metascore']      = movie_html.find(class_=classes['metascore']).get_text().strip() if movie_html.find(class_=classes['metascore']) else '-'
                movie['user_score']     = movie_html.find(class_=classes['user_score']).strong.get_text().strip() if movie_html.find(class_=classes['user_score']).strong else '-'
                movie['num_votes']      = movie_html.find(class_=classes['num_votes']).find_all('span')[1].get_text().strip()
                movie['revenue']        = movie_html.find(class_=classes['num_votes']).find_all('span')[4].get_text().strip() if len(movie_html.find(class_=classes['num_votes']).find_all('span')) > 4 else '-'
                movie['image']          = movie_html.find(class_=classes['image']).a.img['loadlate']
                
            except HTTPError as e:
                print(e)
            except AttributeError as e:
                print(e)
            except IndexError as e:
                print(e)
            
            movies.append(movie)
        else:
            break

# show message to decide if should order movies
shouldOrder = ''
while shouldOrder != '1' and shouldOrder != '2':
    shouldOrder = input("Deseja classificar os filmes?\n1 - Sim | 2 - Não\n")

if shouldOrder == '1':
    # mount messages for order options 
    orderOptions = [(1,"Título",'title'),
                    (2,"Ano",'year'),
                    (3,"Metascore",'metascore'),
                    (4,"User score",'user_score'),
                    (5,"# de votos",'num_votes'),
                    (6,"Arrecadação",'revenue')]
    orderMsg = 'Por qual campo deseja classificar?\n'
    orderBy = 0
    for opt in orderOptions:
        orderMsg += str(opt[0]) + ' - ' + opt[1] + ' | '
    orderMsg = orderMsg[:-2]
    
    # show message with order options
    while int(orderBy) not in range(orderOptions[0][0],orderOptions[-1][0]+1):
        orderBy = input(orderMsg+'\n')
        if not orderBy.isdigit():
            orderBy = 0

    # shiw message with sort options
    sortBy = 0
    while sortBy not in ['1','2']:
        sortBy = input('Deseja ordenar em:\n1 - ascendente | 2 - decrescente\n')


    # order movies by the field and sort selected
    orderBy = [x[2] for x in orderOptions if x[0] == int(orderBy)][0]
    movies.sort(key=lambda x: x[orderBy], reverse=int(sortBy) - 1)

# open file
file = open("filmes.txt", 'w+', encoding='UTF-8')
file.write('#    | imdb | metascore | ano  | votos | arrecadação | título | imagem\n')

# create dir to save cover images
if not os.path.exists("fotos"):
    os.makedirs("fotos")

# download images and write file
count = 0
for movie in movies:
    count += 1
    if count <= 20:
        urlretrieve(movie['image'], 'fotos/'+movie['id']+'.png')
        movie['image'] = 'fotos/'+movie['id']+'.png'

        file.write(str(count) + ' | ')
        file.write(movie['user_score'] + ' | ')
        file.write(movie['metascore'] + ' | ')
        file.write(movie['year'] + ' | ')
        file.write(movie['num_votes'] + ' | ')
        file.write(movie['revenue'] + ' | ')
        file.write(movie['title'] + ' | ')
        file.write(movie['image'] + ' | ')
        file.write('\n')
    else:
        break

file.close()

# show message to choose to receive an email with the movies
send_mail = None
toMail = ''
while send_mail not in [True, False]:
    inpt = input("Deseja receber um email com os 20 primeiros filmes?\n 1 - Sim | 2 - Não\n")
    if inpt in ['1', '2']:
        send_mail = True if inpt == '1' else False
        toMail = input('Digite seu email\n')

# if true, send mail
if(send_mail):
    body = """\
        <table>
            <tr>
                <th>Título</th><th>Ano</th><th>Metascore</th><th>User score</th><th># votos</th>
            </tr>
        """
    count = 1
    for movie in movies:
        if count <= 20:
            body += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>".format(movie['title'], movie['year'], movie['metascore'], movie['user_score'], movie['num_votes'])
            count += 1
        else:
            break

    body += "</table>"

    mail = writeMail(toMail, 'Filmes', body)
    sendMail(mail, 'outlook')
