# Scintillant Bot Framework
- - -
A framework for instantly creating chat bots based on other popular tools.
At the moment, the framework supports the development of skills for the popular chatbot Lilia.
### Installation
``pip install scintillant==0.0.7``

### Using
To quickly create a skill template, use the command:
```>> snlt bottle```

## Quick Start
Create a directory in which you will work 

``>> mkdir my_test_skill``

Create a virtual environment in which you will install the necessary dependencies for work, including the Scintillant framework:

```shell
>> py -m venv env
>> source env/Scripts/activate
```

Install the Scintillant framework. It is also included in the list of dependencies for each skill template.
```shell
(env) >> pip install scintillant
```

After successful installation, you need to get the latest version of the skill template. 
Run the command ``(env) >> snlt bottle`` and follow the instructions.

When choosing a working directory, select the current directory (.) Or leave the field blank to create the template in a subfolder with the skill name.

Install the remaining dependencies and run the skill.
```shell
(env) >> pip install -r requirements.txt
(env) >> py manage.py
```

## Project setup
In the .env file, you can find the starting configurations of the project.

Most addictions are easy to change and not viral. At the moment, the core of the skill is the Bottle framework, but you can easily replace it with AioHTTP or FastAPI.

In the future, it will be possible to receive versions of templates based on other popular web frameworks, as well as on pure WSGI (werkzeug).