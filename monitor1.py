from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

url = 'http://fcpa.stanford.edu/enforcement-actions.html'
source = urllib.request.urlopen(url).read()
soup = BeautifulSoup(source, 'lxml')

#print(soup.title.string)
#print(soup.find_all('p'))

for url in soup.find_all('a'):
    print(url.get('href'))

#    headers = {}
#    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
