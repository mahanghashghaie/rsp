from bs4 import BeautifulSoup as bs
import requests
import re
import sys
import random
import os
import pyperclip


def clean_html_tags(raw_html):
    """ cleanses a raw html string from html tags
    Parameters
    ----------
    raw_html : str
        raw html string literal that is to be cleansed
    Returns
    -------
    cleantext : str
        is the input string without html tags
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_password_from_song_lyrics(num_of_pages, extra_text):
    """ generates password from song lyrics
    Parameters
    ----------
    num_of_pages : int
        number of pages with song urls to be crawled
    extra_text : str
        string which will be appended to the extracted song lyrics
    Returns
    -------
    password : str
        this is the stripped song lyrics appended with the extra_text
    """
    content_list = get_content_overview_pages(num_of_pages)
    song_urls = extract_song_urls(content_list)
    rnd_index = random.randint(0,len(song_urls)-1)
    return extract_stripped_lyrics(song_urls[rnd_index]) + extra_text

def get_content_overview_pages(num_of_pages):
    """ generates list of html documents
    Parameters
    ----------
    num_of_pages : int
        number of pages with song urls to be crawled
    Returns
    -------
    content_list : list
        contains the html source for the num_of_pages that have been crawled
    """
    baseurl = "https://www.songtexte.de/songtexte.html"
    content_list = []
    for i in range(num_of_pages):
        r  = requests.get("https://www.songtexte.de/songtexte.html?seite={}".format(i+1))
        content_list.append(r.text)
    return content_list

def extract_song_urls(overview_content):
    """ extracts song lyric urls
    Parameters
    ----------
    overview_content : list
        list of html document sources which contain song urls
    Returns
    -------
    song_urls : list
        this is a list which contains all song lyric urls which can be found in
        overview_content
    """
    song_urls = []
    for page in overview_content:
        soup = bs(page, 'html.parser')
        for link in soup.findAll("div", {"class": "info"}):
            song_url = link.a.get("href")
            if song_url is not None:
                song_urls.append(song_url)
    return song_urls

def extract_stripped_lyrics(song_url):
    """ extracts whitespace stripped song lyrics from url
    Parameters
    ----------
    song_url : str
        url to the page which contains the song lyrics
    Returns
    -------
    song_lyrics : str
        return the song lyrics stripped of whitespaces and cleansed from html tags
    """
    r  = requests.get(song_url)
    data = r.text
    soup = bs(data, 'html.parser')
    for link in soup.findAll("p", {"class": "lyrics"}):
        cleaned_content = clean_html_tags("".join(str(el) for el in link.contents))
        return re.sub('\s+',' ',cleaned_content).replace(" ","")

def main():
    """ copies password to system clipboard
    
    Takes in command line arguments to generate the password and copy it to the clipboard.
    REMINDER: sys.argv[0] is always the script name.
    You should call this function as such:
    python3 gen_rnd_password.py 3 thisisappendedtotheoutput
    This call would take the song lyrics of the first 3 pages and then
    randomly select one of the songs to generate the password
    """    
    num_of_pages = 3
    if len(sys.argv) > 1:
        num_of_pages = int(sys.argv[1])
    extra_text = "no_extra_text"
    if len(sys.argv) > 2:
        extra_text = sys.argv[2]
    password = get_password_from_song_lyrics(num_of_pages, extra_text)
    pyperclip.copy(password)

if __name__ == '__main__':
    main()
