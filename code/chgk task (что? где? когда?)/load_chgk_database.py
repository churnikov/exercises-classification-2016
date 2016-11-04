"""chgk database loader.

Usage:
  load_chgk_database.py -o FOLDER [-s START] [-e END]
  load_chgk_database.py  (-h | --help)
  load_chgk_database.py  --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  -o FOLDER --output=FOLDER     Where to save images and pickle of questions
  -s START --start=START        Page to start parsing
  -e END --end=END              Page to end parsing
"""

import requests
import re
import urllib.request
import os
import pickle

from bs4 import BeautifulSoup
from docopt import docopt

path = 'http://db.chgk.info'

def get_n_of_pages():
    path = 'http://db.chgk.info'
    r = requests.get('http://db.chgk.info')
    soup = BeautifulSoup(r.text, 'lxml')

    last_page = soup.find('a', title='Перейти на последнюю страницу')['href']
    n_of_pages = int(re.compile('\d+').search(last_page).group(0))
    return n_of_pages

def get_image(img_tag, output = 'Data/'):
    """
    gets img_tag and saves files to Data/images_chgk/. If there is none it would be created
        OR you can scecify folder to save.
        Must be absolute path and be named ../images_chgk/ or it would be created with that name



    returns file name
            or None if there is no image

    example: 123123.jpg
    """

#     regular expression for image name
    reg = re.compile('[\d]+.[\w]+$')
    if img_tag:
#         img_tag usualy looks like '<img src="http://db.chgk.info/images/db/20160407.jpg">'
        img_url = img_tag['src']
        img_name_found = reg.search(img_url)
        if img_name_found:
            img_name = img_name_found.group(0)
        else:
            return None

        directory = output + 'images_chgk/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        urllib.request.urlretrieve(img_url, directory + img_name)
        return img_name
    return None

def get_question(block, output=None):
    """
    gets block -- <div class = "question">

    returns tuple (question_text, image_name) where:
        question_text -- all text found in before <div class="collapsible"> including 'razdatka'
        image_names -- name of image found before <div class="collapsible">. It is saved in 'Data/images_chgk/'.
    """

    question_text = ''

    for t in block.find_all(text=True, recursive=False):
        if t: question_text += ' ' + t.strip()

    for t in block.find('p').find_all(text=True, recursive=False):
        if t: question_text += ' ' + t.strip()

    razdatka = block.find('div', 'razdatka')
    if razdatka:
        r_texts = razdatka.find_all(text=True, recursive=True)
        for t in r_texts:
            question_text += ' ' + t.strip()

#     get_image returns None if there is no image
    give_out = block.find('img')
    if output:
        image_name = get_image(give_out, output)
    else:
        image_name = get_image(give_out)

    return question_text, image_name


def get_answer(block, output=None):
    """
    block -- <div class="collapse-processed">
    output is need only for get_image

    returns tuple (answer_text, image_name, comment_text)
    """
    answer_block = block.find('p')
    answer_text = answer_block.get_text().strip()

    comment_block = answer_block.find_next_sibling('p')
    if comment_block:
        comment_text = comment_block.get_text().strip()
    else:
        comment_text = None

    if output:
        image_name = get_image(block.find('img'), output)
    else:
        image_name = get_image(block.find('img'))

    return answer_text, image_name, comment_text

def get_links(page):
    """
    page -- html that was got from iterating over links on main page

    returns pack of links to pages with questions
    """
    soup_pack = BeautifulSoup(page.text, 'lxml')
    pack = []
    for o in soup_pack.find_all('tr', 'odd'):
        pack.append(path + o.find('a')['href'])
    for e in soup_pack.find_all('tr', 'even'):
        pack.append(path + e.find('a')['href'])
    return pack

def get_questions(page, output=None):
    """
    page -- page on db.chgk.info with questions
    output is need only for get_image

    returns list of tuple where each tuple:
        (question text;
        image name for question if there is one. if not, it is None;
        answer text;
        image name for answer if there is one. if not, it is None;
        comment text if there is one. in not, it is None.)
    """
    questions = []
    soup_quest = BeautifulSoup(page.text, 'lxml')
    for s, a in zip(soup_quest.find_all('div', 'question'), soup_quest.find_all('div', 'collapsible')):
        if output:
            question_text, q_image_name = get_question(s, output)
            answer_text, ans_image_name, comment_text = get_answer(a, output)
        else:
            question_text, q_image_name = get_question(s)
            answer_text, ans_image_name, comment_text = get_answer(a)

        if question_text == '':
            print(page.url)
        else:
            questions.append((question_text, q_image_name, answer_text, ans_image_name, comment_text))
    return questions

if __name__ == "__main__":
    arguments = docopt(__doc__, version='chgk database loader 0.0.1')
    if arguments['--start']:
        start = int(arguments['--start'])
    else:
        start = 0

    if arguments['--end']:
        end = int(arguments['--end'])
    else:
        end = get_n_of_pages()

    out_dir = arguments['--output']

    questions = []
    for i in range(start, end+1):
        print('proceeding link # {n}'.format(n=i))
        payload = {'page' : i}
        page = requests.get('http://db.chgk.info/last', params=payload)
        links = get_links(page)
        for l in links:
            q = requests.get(l)
            quests = get_questions(q, out_dir)
            questions.extend(quests)
    pickle_file = out_dir + 'questions.pickle'
    with open(pickle_file, 'wb') as f:
        pickle.dump(questions, f)
