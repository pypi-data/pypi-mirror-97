"""
Commands aimed at generating skill templates.


"""
import os
from shutil import move, rmtree
from sys import version_info
from zipfile import ZipFile

import requests

from scintillant import BOTTLE_SKILL_TEMPLATE_URL


def start_bottle_skill(skill_name: str = None):
    """Download the latest skill template"""
    skill_name = input("Skill name: ") if not skill_name else skill_name
    skill_dirrectory = input(f"Skill directory ({skill_name}): ")
    if not skill_dirrectory:
        skill_dirrectory = skill_name
    print("Downloading project template...")

    r = requests.get(BOTTLE_SKILL_TEMPLATE_URL)
    with open('temp.zip', 'wb') as f:
        f.write(r.content)

    with ZipFile('temp.zip', 'r') as repo_zip:
        if skill_dirrectory == '.':
            repo_zip.extractall()
        else:
            repo_zip.extractall('.')

    os.remove('temp.zip')
    if not skill_dirrectory == '.':
        os.rename('bottle-skill-template-develop', skill_dirrectory)
    else:
        source = './bottle-skill-template-develop'
        files = os.listdir(source)
        for file in files:
            move(source + f'/{file}', os.getcwd())
        rmtree('./bottle-skill-template-develop')

    if not version_info < (3, 9):
        print("Language version below the required by the template")


def start_aiohttp_skill(skill_name: str = None):
    """Download the latest skill template
    TODO::
    """
    skill_name = input("Skill name: ") if not skill_name else skill_name
    print("Downloading project template...")
    #Repo.clone_from(AIOHTTP_SKILL_TEMPLATE_URL, getcwd() + f'/{skill_name}')


def start_fast_api_skill(skill_name: str = None):
    """Download the latest skill template
    TODO::
    """
    skill_name = input("Skill name: ") if not skill_name else skill_name
    print("Downloading project template...")
    #Repo.clone_from(FAST_API_SKILL_TEMPLATE_URL, getcwd() + f'/{skill_name}')