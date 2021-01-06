from bs4 import BeautifulSoup
import requests
from termcolor import colored


loading, success, important = 'green', 'blue', 'red'


def get_details(index_number):
    print(colored('Getting necessary student data from STU site...', loading))
    if index_number == '06170333':
        print('Student with this index number not found, please try a different index number')
        return
    dob = ''
    surname = ''
    day = ''
    month = ''
    year = ''
    acyear = ''
    program = ''

    month_dict = {
        'Jan': '1',
        'Feb': '2',
        'Mar': '3',
        'Apr': '4',
        'May': '5',
        'Jun': '6',
        'Jul': '7',
        'Aug': '8',
        'Sep': '9',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    page_url = 'https://stu.edu.gh/bkapps/pages/students/student_details.php?index_number='+index_number+'&k=1034183274'
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('td')

    surname = get_raw_text(tables, 'FULL NAME:', position=0)
    if surname == 'ARHINFUL':
        print('Student with this index number not found, please try a different index number')
        return
    dob = get_raw_text(tables, 'DATE OF BIRTH:')
    # split daob
    if dob is not None:
        dob = list(dob.split(' '))
        day = dob[1]
        month = month_dict[dob[2]]
        year = dob[3]
        acyear = get_raw_text(tables, 'YEAR OF ADMISSION:')



    program_name = get_raw_text(tables, 'PROGRAM:')
    # get program code
    code_url = 'https://stu.edu.gh/bkapps/pages/std_forgot_pass1.php'
    code_page = requests.get(code_url)
    code_soup = BeautifulSoup(code_page.content, 'html.parser')
    options = code_soup.find_all('option')
    for option in options:
        if option.text == program_name:
            program = option.get('value')
            break
    if index_number == '06170333':
        print('Student with this index number not found, please try a different index number')
        return

    print(colored('All required information extracted successfully...', success))
    return [
        surname, day, month, year, acyear, program
    ]


def get_raw_text(tables, checker, position=None):
    value = None
    for child in tables:
        if child.text == checker:
            full_value = child.next_sibling.next_sibling.text
            if position is not None:
                value = list(full_value.split(" "))[position]
            else:
                value = full_value
            break
    return value





