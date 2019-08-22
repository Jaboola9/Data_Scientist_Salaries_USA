import requests
import json
import pandas as pd
from pandas.io.json import json_normalize #package for flattening json in pandas df

def get_locations(search_term,key):
    """
    Search available locations in SkyScanner API based on string search, returns results in pd.DataFrame.
    SkyScanner Endpoint Description: 'Get a list of places that match a query string.'
    """
    url_api = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices'
    url = f"{url_api}/autosuggest/v1.0/US/GBP/en-US/"

    querystring = {"query":search_term}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    js = json.loads(response.text)
    out = pd.DataFrame(js['Places'])
    return out

def browse_quotes(origin,dest,key,deptDate,retDate=None):
    """
    Submit custom queries to the SkyScanner Browse Quote API Endpoint and returns a Requests Response object.
    SkyScanner Endpoint Description: 'Retrieve the cheapest quotes from our cache prices.'
    """
    url_api = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices'
    url = f"{url_api}/browsequotes/v1.0/US/USD/en-US/{origin}/{dest}/{deptDate}"
    
    if retDate:
        querystring = {"inboundpartialdate":retDate}
    else:
        querystring = {}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

def browse_routes(origin,dest,key,deptDate,retDate=None):
    """
    Submit custom query to the SkyScanner Browse Routes API Endpoint and returns a Requests Response object.
    SkyScanner Endpoint Description: 'Retrieve the cheapest routes from our cache prices. Similar to the Browse Quotes API but with the routes built for you from the individual quotes.'
    """
    url_api = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices'
    url = f"{url_api}/browseroutes/v1.0/US/USD/en-US/{origin}/{dest}/{deptDate}"
    
    if retDate:
        querystring = {"inboundpartialdate":retDate}
    else:
        querystring = {}
        
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

def browse_dates(origin,dest,key,deptDate='anytime',retDate=None):
    """
    Submit custom query to the SkyScanner Browse Dates API Endpoint and returns a Requests Response object.
    SkyScanner Endpoint Description: 'Retrieve the cheapest dates for a given route from our cache.''
    """
    url_api = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices'
    url = f"{url_api}/browsedates/v1.0/US/USD/en-US/{origin}/{dest}/{deptDate}"

    if retDate:
        querystring = {"inboundpartialdate":retDate}
    else:
        querystring = {}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response

def browse_dates_inbound():
    """
    Submit custom query to the SkyScanner Browse Inbound Dates API Endpoint and returns a Requests Response object.
    SkyScanner Endpoint Description: 'Retrieves the cheapest dates for a given route from our cache. Must include inboundpartialdate.''
    """
    url_api = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices'
    url = f"{url_api}/browsedates/v1.0/%7Bcountry%7D/%7Bcurrency%7D/%7Blocale%7D/%7Boriginplace%7D/%7Bdestinationplace%7D/%7Boutboundpartialdate%7D/%7Binboundpartialdate%7D"

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': key
        }

    response = requests.request("GET", url, headers=headers)

    return response

def parse_quotes(resp):
    """
    Parse response from browse_quotes into single DataFrame. Drops Currency and Places nodes.
    """
    t = json.loads(resp.text)
    
    # Parse nodes to DataFrames, omit Currency and Location
    quote_node = json_normalize(t['Quotes'], meta = 'OutboundLeg') # unnest OutboundLeg dictionary and append to quotes
    carrier_node = pd.DataFrame(t['Carriers']).set_index('CarrierId') # hold carrier information to attach in line 132
    
    # Match Carrier Names to each Quote list of CarrierIds
    carrier_names_per_quote = pd.DataFrame() # carrier name column to fill
    
    for quote_carrier_id_lists in quote_node['OutboundLeg.CarrierIds']: # a list of carriers for each row of quote table
        
        quote_carrier_names = [carrier_node.loc[id,'Name'] for id in quote_carrier_id_lists] # from ids, list names
        carrier_names_per_quote = carrier_names_per_quote.append(quote_carrier_names, ignore_index = True)# append to quote row
    
    carrier_names_per_quote.rename(columns = {0:'CarrierNames'}, inplace = True) # rename carrier name DataFrame
    
    # Append
    quotes = pd.concat([quote_node, carrier_names_per_quote], axis=1)# append to quote DataFrame
    
    return quotes
            
def parse_routes(resp):
    """
    Parse response from browse_routes into single DataFrame. Drops Currency and Places nodes.
    """
    # use parse_quotes above, seems really similar
    
    t = json.loads(resp.text)
    
    # Parse nodes to DataFrames, ['Dates']
    dates_node = json_normalize(t['Dates'], meta = 'OutboundDates') # unnest OutboundDates dictionary and append to parent node
    
    # Append
    routes = pd.concat([quote_node, dates_node], axis=1)# append to quote DataFrame
    
    return routes 

