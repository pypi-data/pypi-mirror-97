import pickle
import requests
from bs4 import BeautifulSoup

url = 'https://docs.python.org/3/py-modindex.html'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
headers = {'User-Agent': ua}
r = requests.get(url,headers=headers)

soup = BeautifulSoup(r.text, 'lxml')
al = []

for line in soup.find('table').find_all('a'):
    al.append(line.text)
    
with open('default_lib_list_392.pkl','wb') as f:
    pickle.dump(al,f)