import requests
import re
import time
from multiprocessing.dummy import Pool as ThreadPool 

#list dork
dorks = open('dork.txt', 'r').read().splitlines()
#list proxy
proxies = open('proxy.txt', 'r').read().splitlines()
#url parameter aktif
parameter_aktif = []
#url parameter yang duplikat
parameter_duplikat = []


def bing_scan(dork):

    #menggunakan proxy untuk request bing search engine 
    for proxy in proxies:

        try:

            #membuat request dengan proxy yang telah ditentukan 
            req = requests.get('http://www.bing.com/search?q=' + dork, proxies={"http": proxy, "https": proxy}, timeout=10)

            #mengecek apakah request berhasil atau tidak 
            if req.status_code == 200:

                #mengecek apakah url memiliki parameter atau tidak 
                links = re.findall(r'<h2><a href="(.*?)"', req.text)

                for link in links:

                    #mengecek apakah url memiliki parameter atau tidak 
                    if '?' in link:

                        #menambahkan url parameter aktif ke list 
                        parameter_aktif.append(link)

                        #mengecek apakah url parameter sudah ada di list atau belum 
                        if link not in parameter_duplikat:

                            #menambahkan url parameter yang duplikat ke list 
                            parameter_duplikat.append(link)

                            #menyimpan hasil ke file result.txt 
                            with open('result.txt', 'a') as f:

                                f.write(link + '\n')

                                print('[+] URL Parameter Aktif : ' + link)

        except Exception as e:

            pass

    time.sleep(1)

    
#membuat multiproses hingga 10 page 
pool = ThreadPool(10) 
pool.map(bing_scan, dorks)
