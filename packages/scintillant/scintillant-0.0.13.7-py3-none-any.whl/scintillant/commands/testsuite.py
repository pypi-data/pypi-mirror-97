"""
Commands for activating the test environment


"""
import sys
import os
import json
from zipfile import ZipFile
import multiprocessing
from livereload import Server
import click
import requests

from scintillant import addons_versions


def create_snlt():
    with open(os.getcwd() + '/.snlt', 'w+') as snlt:
        if sys.platform == 'win32':
            std_path = 'C:\\snlt\\testsuite\\'
        else:
            std_path = '/ust/testsuite/'
        path = input("Specify the path where Python can create "
                     f"the test environment files ({std_path}): ")
        path = std_path if not path else path
        click.echo(path)
        json.dump({
            "skill_name": "bottle-skill-template",
            "skill_working_url": "http://localhost:8080",
            "testsuite": {
                "version": addons_versions['__testsuite__'],
                "path": path,
                "theme": "dark"
            }
        }, snlt, sort_keys=True, indent=4)


def update_snlt():
    js = json.load(open(os.getcwd() + '/.snlt'))
    if sys.platform == 'win32':
        std_path = 'C:\\snlt\\testsuite\\'
    else:
        std_path = './testsuite/'
    path = input("Specify the path where Python can create "
                 f"the test environment files ({std_path}): ")
    path = std_path if not path else path
    with open(os.getcwd() + '/.snlt', 'w+') as snlt:
        if 'testsuite' in js and 'path' not in js['testsuite']:
            js['testsuite']['path'] = path
        elif 'testsuite' not in js:
            js['testsuite'] = {'theme': 'dark'}
            js['testsuite']['path'] = path
        json.dump(js, snlt, sort_keys=True, indent=4)


def install_suite(path):
    suite_release = ("https://github.com/PaperDevil/snlt_testsuite/releases/download/"
                     f"{addons_versions['__testsuite__']}"
                     "/dist.zip")
    r = requests.get(suite_release)
    os.makedirs(os.path.dirname(path + 'temp.zip'), exist_ok=True)
    with open(path + 'temp.zip', 'wb') as f:
        f.write(r.content)
    with ZipFile(path + 'temp.zip', 'r') as repo_zip:
        repo_zip.extractall(path)
    os.remove(path + 'temp.zip')


def get_current_app(app_path: str = None):
    try:
        click.echo("Tryng get application instance...")
        sys.path.append(app_path or os.getcwd())
        from manage import run_app
        return run_app
    except ImportError as exc:
        raise ImportError(
            "The specified path does not contain a valid manage.py file. "
            "Make sure you've installed all the dependencies from the "
            "requirements.txt file and created the run_app function correctly "
            "inside the manage.py file!"
        )


def start_bot_server():
    app = get_current_app()
    click.echo("Starting application server...")
    try:
        app(port=8080)
    except Exception as exc:
        click.echo(exc)


def start_test_suite():
    if os.path.exists(os.getcwd() + '/.snlt'):
        js = json.load(
            open(os.getcwd() + '/.snlt')
        )
        if 'testsuite' not in js or 'path' not in js['testsuite']:
            update_snlt()
            return start_test_suite()
        else:
            test_suite_path = js['testsuite']['path']
            install_suite(test_suite_path)
    else:
        create_snlt()
        return start_test_suite()

    if not os.path.exists(test_suite_path):
        install_suite(test_suite_path)
        return start_test_suite()

    click.echo("Creates processes...")
    _process = multiprocessing.Process(target=start_bot_server, args=())
    _process.start()

    click.echo("starting testsuite...")
    server = Server()
    server.serve(root=test_suite_path, default_filename='index.html')
