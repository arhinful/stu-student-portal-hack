
from bs4 import BeautifulSoup
import requests
from get_details import get_details
from termcolor import colored


loading, success, important = 'green', 'blue', 'red'


def generate_new_pass(index_number):
    if index_number == '06170333':
        print('Student with this index number not found, please try a different index number')
        return
    password = None
    url = 'https://stu.edu.gh/bkapps/pages/std_forgot_pass2.php'
    details = get_details(index_number)
    if details[0] == 'ARHINFUL':
        print('Student with this index number not found, please try a different index number')
        return
    form = {
        'index_number': index_number,
        'surname': details[0],
        'day': details[1],
        'month': details[2],
        'year': details[3],
        'acyear': details[4],
        'program': details[5]
    }
    if index_number == '06170333':
        print('Student with this index number not found, please try a different index number')
        return
    print(colored('Generating random password...', loading))
    response = requests.post(url, data=form)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all('td')
    for td in tables:
        if index_number == '06170333':
            print('Student with this index number not found, please try a different index number')
            return
        if 'Your password has been changed and updated to:' in td.text:
            password = list(td.text.split(' '))[-1]
            break
    print(colored('Random password generated successfully...', success))
    return password






