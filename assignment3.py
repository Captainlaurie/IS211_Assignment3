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

    # Set up dictionary for counting browsers
    browserCount = {
        "Safari": 0,
        "Chrome": 0,
        "MSIE": 0,
        "Firefox": 0
    }

    # Set up dictionary for hours
    hoursAccessed = {hour: 0 for hour in range(23)}

    csv_data = csv.reader(io.StringIO(urldata))

    # Keep track of number of images
    imageCounter = 0

    for row in csv_data:
        path_to_file = row[0]
        datetime_access_str = row[1]
        browser = row[2]

        # Regular expression to look for images

        if re.search(r"\.JPG|\.JPEG|\.PNG|\.GIF", path_to_file, re.IGNORECASE):
            imageCounter = imageCounter + 1

        # Count browsers by searching for the string of the browser name
        if "Safari" in browser:
            browserCount["Safari"] += 1

        elif "Chrome" in browser:
            browserCount["Chrome"] += 1

        elif "MSIE" in browser:
            browserCount["MSIE"] += 1

        elif "Firefox" in browser:
            browserCount["Firefox"] += 1


        # Find most popular browser
        mostPopBrowser = max(browserCount, key=browserCount.get)

        # Convert datetime_access_str to datetime
        access_time = datetime.datetime.strptime(datetime_access_str, "%Y-%m-%d %H:%M:%S")
        hoursAccessed[access_time.hour] += 1
        
        # Calculate the percentage of hits that were images
        totalHits = sum(hoursAccessed.values())
        imagePercentage = imageCounter / totalHits * 100

    print(f"Image count = {imageCounter}")
    print(f"Image requests account for {imagePercentage:.2f}% of all requests")
    print(f"The most popular browser = {mostPopBrowser}")
    
    
    # Find and print hits by hour
    hitsByHour = [(hour, hoursAccessed[hour]) for hour in hoursAccessed]
    hitsByHour.sort(key=lambda x: x[1], reverse=True)
    for hour, hits in hitsByHour:
        print(f"Hour {hour} has {hits} hits")
    
    
def main(url):
    print(f"Running main with URL = {url}...")

    data = downloadData(url)

    processData(data)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)


# url http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
