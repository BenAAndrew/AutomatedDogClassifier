from google_images_download import google_images_download
import concurrent.futures
  
# creating object 
response = google_images_download.googleimagesdownload()  
  
#important variables - customise for needs
breeds = [line.rstrip('\n') for line in open("breeds.txt")]
images_per_breed = 100
max_similtaneous_threads = 10

def downloadimages(query): 
    arguments = {"keywords": query, 
                 "format": "jpg", 
                 "size": "medium",
                 "output_directory": "dataset",
                 "limit": images_per_breed, 
                 #"chromedriver": "chromedriver.exe", 
                 "print_urls": False} 
    try: 
        response.download(arguments)    
    except:  
        pass

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_similtaneous_threads) as executor:
        executor.map(downloadimages, breeds)