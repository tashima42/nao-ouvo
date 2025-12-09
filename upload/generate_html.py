import xml.etree.ElementTree as ET
import urllib.parse
from slug import create_slug
import argparse
import os

parser = argparse.ArgumentParser(description="Nao Ouvo generate html")

parser.add_argument("--feedfile", required=True, type=str, help="Feed file")
parser.add_argument("--writelocation", required=True, type=str, help="Where to write files to")

args = parser.parse_args()

feed_path = args.feedfile
write_location = args.writelocation

tree = ET.parse(feed_path)
root = tree.getroot()
items = root[0].findall("item")

html_template = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Não Ouvo (Arquivo da Comunidade)</title>
</head>

<body>
  <main>
    <h1>Não Ouvo (Arquivo da Comunidade)</h1>
    <div id="feed">
        <a href="feed.xml">https://tashima42.github.io/nao-ouvo/feed.xml</a>
    </div>
    <div id="nav">{nav}</div>
    <div id="episodes">
        {items}
    </div>
  </main>
</body>
</html>
"""
episode_block = """
<div id="{slug}">
  <h2 class="title">{title}</h2>
  <p class="date">{date}</p>
  <p class="description">{description}</p>
  <iframe src="https://archive.org/embed/{slug}" width="500" height="30" frameborder="0"
    webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe>
</div>
"""
nav_block = """<a href="{page}.html">{page}</a>"""

def generate(items):
    pages = []
    page = []
    counter = 0
    items_counter = 0
    # items_length = len(items)
    for item in items:
        page.append(item)
        counter += 1

        if counter == 9 or items_counter == len(items):
            pages.append(page)
            page = []
            counter = 0
    
        items_counter += 1

    page_counter = 0
    filename = "index.html"

    pages_files=["index"]


    for i in range(1, len(pages)):
        pages_files.append(str(i))

    nav_html = " ".join([nav_block.format(page=page) for page in pages_files])

    for page in pages:
        episodes = []
        print("page: ", page_counter)


        for item in page:
            title = item.find("title").text
            description = item.find("description").text
            date = item.find("pubDate").text

            slug = create_slug(title)

            ep = {
                'slug': slug,
                'title': title,
                'description': description,
                'date': date,
            }
            episodes.append(ep)

        items_html = "\n".join([episode_block.format(**ep) for ep in episodes])
        final_html = html_template.format(items=items_html, nav=nav_html)

        # Write to file
        with open(os.path.join(write_location, filename), "w", encoding="utf-8") as f:
            f.write(final_html)

        print("HTML file generated: ", filename)
        page_counter += 1
        filename = str(page_counter) + ".html"

generate(items)
