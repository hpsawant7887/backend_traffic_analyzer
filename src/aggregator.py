
def aggregate_success_rate(aggregated_success_rate, status_response, logger):
    """This method calculates and returns aggregated response rate
       :aggregated_success_rate: A Dictionary
       :status_response: A Dictionary
       :logger: logger obj
    """
    try:
        app = status_response['Application']
        version = status_response['Version']
        req_count = int(status_response['Request_Count'])
        success_count = int(status_response['Success_Count'])
    
    
        if app in aggregated_success_rate:
            if version in aggregated_success_rate[app]:
                aggregated_success_rate[app][version]['total_req_count'] += req_count
                aggregated_success_rate[app][version]['total_success_count'] += success_count
                agg_success_rate = (aggregated_success_rate[app][version]['total_success_count']/aggregated_success_rate[app][version]['total_req_count']) *100
            
                aggregated_success_rate[app][version]['success_rate_%'] = round(agg_success_rate, 2)   # round to 2 decimal points
        
            else:
                success_rate = round((success_count/req_count)*100, 2)     # round to 2 decimal points
                aggregated_success_rate[app][version] = {
                    'total_req_count': req_count,
                    'total_success_count': success_count,
                    'success_rate_%': success_rate
                }
            
        else:
            success_rate = round((success_count/req_count)*100, 2)     # round to 2 decimal points
            aggregated_success_rate[app] = {
                version:{
                    'total_req_count': req_count,
                    'total_success_count': success_count,
                    'success_rate_%': success_rate
                }
            }
    
        return aggregated_success_rate
    except Exception as e:
        logger.error(e)
        return aggregated_success_rate
    
    
    
    
    
    
    
    
