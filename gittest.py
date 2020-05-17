import os
import sys

def updaterepo(repo, filelist, description):

    if repo is None:
        print('Need to supply a valid repo name')
        sys.exit(0)
    else:
        print(f'Repo set as : {repo}')

    print(f'We are in folder : {str(os.getcwd())}')
    print(f'The status for the repo {repo} is:\n {os.system("git status")}')

    for file in filelist:
        try:
            os.system("git add " + file)
            os.system("git commit -a -m '" + description + "'")
        except Exception as e:
            print(e)

    os.system("git push origin master")



updaterepo('box', ['testfile.txt'], 'this is my first git load test')