import requests
import pyfiglet
from halo import Halo
from bs4 import BeautifulSoup
import urllib

def getlinks(file_path):

    spinner = Halo(text='\nScanning\n', spinner='...')
    R = '\033[31m' 
    G = '\033[32m'
    C = '\033[36m'
    W = '\033[0m' 
    # image=input(C+"Enter the image path : ")
    image = file_path
    print("-------------------image---------------"+image)
    try:
        #spinner.start()
        headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        url='http://www.google.co.in/searchbyimage/upload'
        secondurl={'encoded_image': (image, open(image, 'rb')), 'image_content': ''}
        #print(secondurl)
        response = requests.post(url, files=secondurl,allow_redirects=False)
        fetch=response.headers['Location']
        
        print("Fetch "+fetch)
        req=requests.get(fetch,headers=headers)
        print(req)
        linklist=[]
        linklist2=[]
        print(G+"[+] Scan started......")
        print(G+"Checking the image :")         
        if(req.status_code == 200):        
            soup = BeautifulSoup(req.content,'html.parser')
            #print(soup)
            
            for x in soup.find_all('a', class_='ekf0x hSQtef'):
                x=x['href']
                final_url='http://www.google.co.in'+x
                print(final_url)
                req2=requests.get(final_url,headers=headers)
                print(req2)
                if(req2.status_code == 200):        
                    soup2 = BeautifulSoup(req2.content,'html.parser')
                    #print(soup2)
                    count = 0
                    for g2 in soup2.find_all('a',class_="VFACy kGQAp sMi44c lNHeqe WGvvNb"):
                        if count==20:
                            break
                        #print(g2['href'])
                        linklist2.append(g2['href'])
                        count+=1

            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')          
            c=0
            for g in soup.find_all('div',class_='g'):
                anchors = g.find_all('a')
                c+=1         
                if 'href' in str(anchors[0]):
                    print(anchors[0]['href'])
                    linklist.append(anchors[0]['href'])
            if c == 0:
                print(R+"No links associated with this image")
            scrapper_getlinks=linklist+linklist2
            return scrapper_getlinks
    #     spinner.stop()
    except Exception as e:
        print("Scrapper Exception: "+str(e))
        
        
    

    


