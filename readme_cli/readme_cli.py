import sys

from bs4 import BeautifulSoup
import requests
import urwid
from readme_cli import utilities


# ASCII color codes
RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'


def stylize_code(soup):
    """Identifies and stylizes code in a question or answer."""
    stylized_text = []
    code_blocks = [block.get_text() for block in soup.find_all("code")]
    blockquotes = [block.get_text() for block in soup.find_all("blockquote")]
    main_heading = [block.get_text() for block in soup.find_all("h1")]
    headings = [block.get_text() for block in soup.find_all("h2")]
    list_items = [block.get_text() for block in soup.find_all("li")]
    strong_items = [block.get_text() for block in soup.find_all("strong")]
    links = [block.get_text() for block in soup.find_all("a")]
    newline = False

    for child in soup.recursiveChildGenerator():
        name = getattr(child, "name", None)

        if name is None: # Leaf (terminal) node
            if child in code_blocks:
                if newline: # Code block
                    #if code_blocks.index(child) == len(code_blocks) - 1: # Last code block
                        #child = child[:-1]
                    stylized_text.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    stylized_text.append(("code", u"%s" % str(child)))
            elif child in blockquotes:
                if newline: # Code block
                    stylized_text.append(("blockquote", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    stylized_text.append(("blockquote", u"%s" % str(child)))
            elif child in main_heading:
                stylized_text.append(("main_heading", u"\n%s" % str(child)))
            elif child in strong_items:
                stylized_text.append(("strong_item", u"\n%s" % str(child)))
            elif child in headings:
                stylized_text.append(("heading", u"\n%s" % str(child)))
            elif child in list_items:
                stylized_text.append(("list_item", u"\n - %s" % str(child)))
            elif child in links:
                stylized_text.append(("link", u"\n%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')
                stylized_text.append(u"%s" % str(child))

    return urwid.Text(stylized_text)

def interleave(a, b):
    result = []
    while a and b:
        result.append(a.pop(0))
        result.append(b.pop(0))

    result.extend(a)
    result.extend(b)

    return result


class App(object):
    def __init__(self, readme_results):
        self.palette = [
            ("main_heading", "light green,bold,underline", "default", "standout"),
            ("code", "black", "light gray", "standout"),
            ("blockquote", "black", "light gray", "standout"),
            ("heading", "brown,bold", "default", "standout"),
            ("list_item", "light cyan", "default", "standout"),
            ("strong_item", "brown,bold", "default", "standout"),
            ("link", "light green,underline", "default", "standout")
        ]

        readme_content = [stylize_code(readme_results)]

        pile = urwid.Pile(interleave(readme_content, [urwid.Divider('-')] * (len(readme_content) - 1)))
        padding = utilities.ScrollBar(utilities.Scrollable(urwid.Padding(pile, left=2, right=2)))
        linebox = urwid.LineBox(padding)

        layout = urwid.Frame(body=urwid.Overlay(linebox, urwid.SolidFill(u'\N{MEDIUM SHADE}'), "center", ("relative", 60), "middle", 23))
        self.main_loop = urwid.MainLoop(layout, self.palette)

        self.main_loop.run()


def read(url):
    try:
        readme_url = url + "/blob/master/README.md"
        req = requests.get(readme_url)
    except requests.exceptions.RequestException:
        sys.stdout.write("\n%s%s%s" % (RED, "Readme_cli was unable to fetch github readme content. "
                                            "Please check that you are connected to the internet.\n", END))
        sys.exit()

    soup = BeautifulSoup(req.text, "html.parser")
    readme = soup.find("article", {"class": "markdown-body entry-content container-lg"})

    App(readme) # Open the interface


