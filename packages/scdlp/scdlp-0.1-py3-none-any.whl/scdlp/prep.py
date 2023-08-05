import os


def prep(project_name):
    os.system(".env\\scripts\\activate")
    os.chdir(os.getcwd() + "/" + project_name)
    os.system("pip install -r requirements.txt")