import requests
import json

START_URL = "https://schema.org"

def fetch_content(url: str) -> str:
    request = requests.get(url).content.strip().decode("latin_1")
    return request

def fetch_urls(site_content: str):
    urls = []
    while True:
        start = site_content.find('href="https')
        if start == -1:
            break
        end = site_content.find('"', start+6)
        url = site_content[start+6:end]
        site_content = site_content[end:]
        urls.append(url)
    return urls
    
def clean(store: dict[list]):
    all_urls = []
    cleaned = {}
    for lev in store.keys():
        cleaned[lev] = []
        for url in list(store[lev]):
            if url not in all_urls:
                all_urls.append(url)
                cleaned[lev].append(url)
        cleaned[lev].sort()
    return cleaned
            
    
    
def recursive(urls, level):
    if level <= max_level:
        with open("urls.json", "r") as file_data:
            data = json.load(file_data)
        new_urls = []
        for url in urls:
            print(f"fetching {url}")
            try:
                url_content = fetch_content(url)
                found_urls = fetch_urls(url_content)
                for x in found_urls:
                    if x not in data:
                        new_urls.append(x)
                        data.append(x)
            except requests.ConnectTimeout:
                continue
            
        with open("urls.json", "w") as file_data:
            json.dump(data, file_data, indent=4)
        recursive(new_urls, level + 1)
        
        
if __name__ == "__main__":
    desire_level = 0
    max_level = 2
    recursive([START_URL], desire_level)
    #cleand = clean(storage)
    
    #with open("data/storage.json", "w") as file_data:
        #json.dump(cleand, file_data, indent=4)
