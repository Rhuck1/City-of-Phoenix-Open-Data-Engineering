


def url_scraper(page_soup):
    
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