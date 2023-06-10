import json
from re import I
from bs4.element import SoupStrainer
import requests
from bs4 import *
from requests.exceptions import RetryError
import searcher
import time

class Scrapper:
    def __init__(self, file_path) -> None:
        self.links_target = searcher.getlinks(file_path) #Links in which you'll search for the images
        print("target_links",self.links_target)
        self.target_link_image_tags_mappings = dict()
        self.tag_imageLink_maps = dict()
        self.img_tags = self.get_image_tags()
        self.img_links = self.make_image_links()

    def get_image_links(self):
        return self.img_links

    def get_image_tags(self):
        image_tags = []
        target_link_image_tags_mappings = dict()
        for target_link in self.links_target:
            try:
                time.sleep(0.1)
                r = requests.get(target_link, verify=False)
                soup = BeautifulSoup(r.text, 'html.parser')
                tags = soup.findAll("img")
                print(len(tags))
                for tag in tags:
                    image_tags.append(tag) 

                self.target_link_image_tags_mappings[target_link] = tags
                image_tags.append(tags)
            except Exception as e:
                print(e)
                continue

        print(len(image_tags))
        return image_tags



        # print(image_tags)

    def make_image_links(self):
        # image_links = [self.image_links_from_image_tags(tag) for tag in self.img_tags]

        image_links = []

        for target_link in self.links_target:
            for tag in self.target_link_image_tags_mappings[target_link]:
                image_links.append(self.image_links_from_image_tags(tag))
        
        # return image_links

        print(f"Found {len(image_links)} image_links")
        # for image_tag, image_link  in zip(self.img_tags, image_links):
        #     print(type(image_link))
        #     print(type(image_tag))
        #     self.tag_imageLink_maps[image_tag] = image_link
        
        return image_links


    def image_links_from_image_tags(self, img_tag):
        # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = img_tag["data-srcset"]
                 
            # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = img_tag["data-src"]

                    return image_link
                except:
                    try: # In image tag ,searching for "data-fallback-src"
                        image_link = img_tag["data-fallback-src"]

                        return image_link
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = img_tag["src"]

                            return image_link
                        except:
                            try:
                                image_link = img_tag['imgurl']

                                return image_link
 
                        # if no Source URL found
                            except Exception as e:
                                print("Can't find image link form the tag")
                                print(e)

                                return "Invalid tag"

    def getlinks(self):
        return self.links_target
    
    # def download(self):
        

if __name__ == "__main__":
    s = Scrapper()
    # links = s.getlinks()
    # print(links)
    # s.get_image_tags()  
    # print(s.target_link_image_tags_mappings.keys())
    print(s.img_links)
