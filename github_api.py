import csv
import os

from github import Github
from sqlmodel import create_engine

from database import get_users

file_path = 'users.csv'


def fill_data(engine: create_engine):
    users_list = get_users(engine)
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for user in users_list:
            writer.writerow([user.user_id, user.warns, user.kicks, user.mutes])


def get_data() -> str:
    string = ''
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            string_row = ''
            for element in row:
                string_row += f'{element},'
            string += f'{string_row}\n'
    return string


def update_csv():
    data = get_data()
    token = os.getenv('TOKEN', 'token')
    g = Github(token)
    repo = g.get_repo('mezgoodle/genji-moderator')
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, 'Update users.csv', data, contents.sha, branch='master')
