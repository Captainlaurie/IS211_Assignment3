import argparse
import urllib.request
import csv
import re
import io
import datetime


def downloadData(url):
    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return:
    """
    # read the URL
    # pip install requests
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    # return the data
    return response


def processData(urldata):
    
    '''
    Process the csv data
    
    :param urldata:
    :return:
    
    '''
        
    csv_data = csv.reader(io.StringIO(urldata))
    
    #Keep track of number of images
    imageCounter = 0
    
    #Set up dictionary for counting browsers        

    browserCount = {"Safari": 0, "Chrome": 0, "MSIE": 0, "Firefox": 0 }
    
    for row in csv_data:
        
        path_to_file = row[0]
        datetime_access_str = row[1]
        browser = row[2]
        
        
        #Regular expression to look for GIF, JPG, JPEG, PNG images
        
        extension = path_to_file.split(".")[-1]
        
        #if path_to_file.upper().endswith("JPEG", "JPG", "PNG", "GIF"):
       
        if re.search(r"(?i)(JPG|JPEG|PNG|GIF)$", extension):
            imageCounter = imageCounter + 1
           

        # Count browsers
        if re.search(r"(?i)Safari", browser):
            browserCount["Safari"] += 1

        if re.search(r"(?i)Chrome", browser):
            browserCount["Chrome"] += 1

        if re.search(r"(?i)MSIE", browser):
            browserCount["MSIE"] += 1

        if re.search(r"(?i)Firefox", browser):
            browserCount["Firefox"] += 1
            
        
    return browserCount, imageCounter
            
            
    #Convert datetime_access_str to datetime
        
    access_time = datetime.datetime.strptime(datetime_access_str, "%Y %m %d %H: %M: %S")
    
    print(access_time.hour)

    #Print image count
    print(f"Image count = {imageCounter}")
 
    #Print the browser counts and find the highest
    print(f"Safari count = {browserCount['Safari']}")
    print(f"Chrome count = {browserCount['Chrome']}")
    print(f"MSIE count = {browserCount['MSIE']}")
    print(f"Firefox count = {browserCount['Firefox']}")
    


def main(url):
    print(f"Running main with URL = {url}...")
    
    #data = downloadData(url)
    
    #processData(data)
    
    pass


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
    