import sys
from readme_cli import readme_cli

RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'



def help():
    """Print library detailes and usage"""
    print("%sReadme_cli, Made by @genza999%s\n" % (BOLD, END))
    print("Command line tool that displays github README.md content for github repositories")
    print("\n\n%sUsage:%s $ readme_cli %s[github_repo_url]%s\n" % (UNDERLINE, END, YELLOW, END))


def main():
    url = ""
    if len(sys.argv) == 1 or sys.argv[1].lower() == "-h" or sys.argv[1].lower() == "--help":
        help()
    else:
        try:
            url = ' '.join(sys.argv[1:])
        except IndexError:
            print("You need to pass in a url to proceed")
            sys.exit()
    if url:
        readme_cli.read(url)
    else:
        sys.exit()
