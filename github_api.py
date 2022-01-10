import csv

from github import Github
from sqlmodel import create_engine

from database import get_users
from config import GITHUB_TOKEN

file_path = 'users.csv'


def fill_data(engine: create_engine) -> None:
    """
    Read data from database and fill with it csv file
    :param engine: sqlmodel's engine
    :return: nothing to return
    """
    users_list = get_users(engine)
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for user in users_list:
            writer.writerow([user.user_id, user.warns, user.kicks, user.mutes])


def get_data() -> str:
    """
    Get data from csv file and return as string
    :return: csv-file content
    """
    string = ''
    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            string_row = ''
            for element in row:
                string_row += f'{element},'
            string += f'{string_row}\n'
    return string


def update_csv() -> None:
    """
    Update csv file on GitHub
    :return: nothing to return
    """
    data = get_data()
    token = GITHUB_TOKEN
    g = Github(token)
    repo = g.get_repo('mezgoodle/genji-moderator')
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, 'Update users.csv', data, contents.sha, branch='master')
