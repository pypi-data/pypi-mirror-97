import urllib3

def download_series (url, localDir) :
    print ('Beginning file download with urllib module')
    urllib3.request.urlretrieve (url, localDir) 
    return 
