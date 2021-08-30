import requests
import boto3
from botocore.exceptions import NoCredentialsError


def url_scraper(page_soup):
    '''
    Scrapes City of Phoenix Open Data page and gathers csv links for each month for City Checkbook and returns results in a dictionary
    '''
    
    # grabs each checkbook heading which is descriptive of month and year
    headings = page_soup.findAll("a", {"class":"heading"})
    # grabs each csv url link to data related to each checkbook heading
    resource_csv_urls = page_soup.findAll("a", {"class":"resource-url-analytics"})
    
    # creates a list of headings
    checkbook_headings_list = []
    dump = ['City', 'Checkbook']

    for idx, heading in enumerate(headings):

        head = headings[idx]['title']
        new_head = [word for word in head.split() if word not in dump]
        checkbook_headings_list.append(" ".join(new_head))
    
    # creates a list of urls 
    csv_hrefs_list = []

    for idx, url in enumerate(resource_csv_urls):
        csv_hrefs_list.append(resource_csv_urls[idx]['href'])
    
    # creates a dictionary of header:url key, values
    heading_csv_url_dict = {key:value for key, value in zip(checkbook_headings_list, csv_hrefs_list)}
    
    return heading_csv_url_dict


def writer(key, value):
    '''Input: Takes the key, value pair in a for loop supplied by the dict of csv links scraped earlier
       Output: Downloads csv data and saves to data directory and outupts file path of downloaded csv
    '''
    
    # gets http response from City Checkbook csv link
    r = requests.get(value)
    
    # creates desired filepath for download
    file_path = 'data/{}.csv'.format(key)
    
    # writes csv into filepath
    open(file_path, 'wb').write(r.content)
    
    return file_path


def upload_to_aws(local_file, bucket, s3_file):
    
    '''
    Uploads file to AWS S3 bucket
    '''
    
    # aws_access_key_id and aws_secret_access_key are stored in local .aws config file
    s3 = boto3.client('s3')
    
    # 3 parameters necessary for upload: (file to upload to s3, s3 bucket name, 
    # the name by which we will save the file in s3)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print('Upload Successful')
        return True
    
    except FileNotFoundError:
        print('The file was not found')
        return False
    
    except NoCredentialsError:
        print('Credentials not available')
        return False
    
    
def bulk_upload_to_aws(dict):
    
    '''Input: Heading, Link (key, value) dictionary of scraped CSV links and headings
    
       Output: Downloads the CSV's to local data directory and uploads the csv to S3 instance
    '''
    
    # S3 bucket that I am uploading to
    bucket = 'city-of-phx-open-data-engineering-raw-db'

    # loop through each Header, Link in dictionary
    for key, value in dict.items():
        
        # download csv and create file path 
        file_path = writer_d(key, value)
        
        # create s3 file name
        s3_file = file_path[5:]
        
        # upload csv to s3
        upload_to_aws(file_path, bucket, s3_file)