import urllib.request

def get_endpoint_status(endpoint, logger):
    """:endpoint: URL
       :type endpoint: String
       :logger: logger obj
       :type logger: Obj
    """
    try:
        url = 'http://{}'.format(endpoint)
        req = urllib.request.Request(url)
        res_obj = urllib.request.urlopen(req, timeout=3)
        
        response = res_obj.read().decode('utf-8')
        
        return response
    
    except Exception as e:
        logger.error('endpoint={} - error={}'.format(endpoint, e))