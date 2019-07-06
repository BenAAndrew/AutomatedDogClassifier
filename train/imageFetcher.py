from google_images_download import google_images_download
import concurrent.futures

#get projectProperties from elevated directory
import sys
sys.path.append('../')
import projectProperties 
  
# creating object 
response = google_images_download.googleimagesdownload()  
  
#important variables - customise for needs
breeds = [line.rstrip('\n') for line in open(projectProperties.details['classes_list'])]
imagesPerClass = int(projectProperties.details['images_per_class'])
maxThreads = int(projectProperties.details['image_fetching_threads'])
datasetName = projectProperties.details['dataset_name']
imageSize = projectProperties.details['image_size']
imageFormat = projectProperties.details['image_format']

def downloadimages(query): 
    arguments = {"keywords": query, 
                 "format": imageFormat, 
                 "size": imageSize,
                 "output_directory": datasetName,
                 "limit": imagesPerClass, 
                 #"chromedriver": "chromedriver", 
                 "print_urls": False} 
    try: 
        response.download(arguments)    
    except:  
        pass

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
        executor.map(downloadimages, breeds)