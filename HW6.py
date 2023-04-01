import requests
import json
import unittest
import os

###########################################
# Your name: Christina Ng                 #
# Who you worked with: Yuyu Yang          #
###########################################

def load_json(filename):
    '''
    Loads a JSON cache from filename if it exists

    Parameters
    ----------
    filename: string
        the name of the cache file to read in

    Returns
    -------
    dict
        if the cache exists, a dict with loaded data
        if the cache does not exist, an empty dict
    '''
    # file exists
    try:
        with open(filename, 'r', encoding='UTF-8') as f:
            # create json object
            data = json.load(f)
            return data
    # file does not exist
    except FileNotFoundError:
        return {}
    
def write_json(filename, dict):
    '''
    Encodes dict into JSON format and writes
    the JSON to filename to save the search results

    Parameters
    ----------
    filename: string
        the name of the file to write a cache to
    
    dict: cache dictionary

    Returns
    -------
    None
        does not return anything
    '''  
    with open(filename, 'w') as f:
        # write dict into json file, set indent to 4
        json.dump(dict, f, indent=4)
    return

def get_swapi_info(url, params=None):
    '''
    Check whether the 'params' dictionary has been specified. Makes a request to access data with 
    the 'url' and 'params' given, if any. If the request is successful, return a dictionary representation 
    of the decoded JSON. If the search is unsuccessful, print out "Exception!" and return None.

    Parameters
    ----------
    url (str): a url that provides information about entities in the Star Wars universe.
    params (dict): optional dictionary of querystring arguments (default value is 'None').
        

    Returns
    -------
    dict: dictionary representation of the decoded JSON.
    '''
    # create request object
    if params:
        r = requests.get(url, params)
    else:
        r = requests.get(url)


    # request status is successful
    if r.status_code == 200:
        # return response python object in json format
        return json.loads(r.text)
    # request status fails
    else:
        print('Exception!')
        return 

def cache_all_pages(people_url, filename):
    '''
    1. Checks if the page number is found in the dict return by `load_json`
    2. If the page number does not exist in the dictionary, it makes a request (using get_swapi_info)
    3. Add the data to the dictionary (the key is the page number (Ex: page 1) and the value is the results).
    4. Write out the dictionary to a file using write_json.
    
    Parameters
    ----------
    people_url (str): a url that provides information about the 
    characters in the Star Wars universe (https://swapi.dev/api/people).
    filename(str): the name of the file to write a cache to
        
    '''
    cache = load_json(filename)
    if not cache:
        cache = {}
    
    # Make a request for the first page
    page = 1
    url = f"{people_url}?page={page}"
    page_data = get_swapi_info(url)
    
    # Loop through all pages until no 'next' URL is returned
    while page_data:
        # Add page data to the cache dictionary
        cache[f"page {page}"] = page_data['results']
        
        # Check if there is a next page
        next_url = page_data['next']
        if next_url:
            page += 1
            page_data = get_swapi_info(next_url)
        else:
            break
    
    # Write the updated cache to the file
    write_json(filename, cache)
    return cache

def get_starships(filename):
    '''
    Access the starships url for each character (if any) and pass it to the get_swapi_info function 
    to get data about a person's starship.
    
    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the character's name as a key and a list of the name their 
    starships as the value
    '''
    # load json file from input file
    data = load_json(filename)
    s_dict = {}
    # iterate through data pages
    for i in data:
        # iterate through page content
        for x in data[i]:
            # store name
            name = x['name']
            # store url
            urls = x['starships']
            # create starship list
            s_list = []
            
            # validate url exists
            if urls:
                # iterate through each url
                for url in urls:
                    # store data api information for each url
                    api = get_swapi_info(url)
                    s_list.append(api['name'])
            # add api to output dict with name as key
            s_dict[name] = s_list
    return s_dict
    

#################### EXTRA CREDIT ######################

def calculate_bmi(filename):
    '''
    Calculate each character's Body Mass Index (BMI) if their height and mass is known. With the metric 
    system, the formula for BMI is weight in kilograms divided by height in meters squared. 
    Since height is commonly measured in centimeters, an alternate calculation formula, 
    dividing the weight in kilograms by the height in centimeters squared, and then multiplying 
    the result by 10,000, can be used.

    Parameter
    ----------
    filename(str): the name of the cache file to read in 
    
    Returns
    -------
    dict: dictionary with the name as a key and the BMI as the value
    '''

    pass

class TestHomework6(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.filename = dir_path + '/' + "swapi_people.json"
        self.cache = load_json(self.filename)
        self.url = "https://swapi.dev/api/people"

    # def test_write_json(self):
    #     write_json(self.filename, self.cache)
    #     dict1 = load_json(self.filename)
    #     self.assertEqual(dict1, self.cache)

    # def test_get_swapi_info(self):
    #     people = get_swapi_info(self.url)
    #     tie_ln = get_swapi_info("https://swapi.dev/api/vehicles", {"search": "tie/ln"})
    #     self.assertEqual(type(people), dict)
    #     self.assertEqual(tie_ln['results'][0]["name"], "TIE/LN starfighter")
    #     self.assertEqual(get_swapi_info("https://swapi.dev/api/pele"), None)
    
    def test_cache_all_pages(self):
        cache_all_pages(self.url, self.filename)
        swapi_people = load_json(self.filename)
        self.assertEqual(type(swapi_people['page 1']), list)

    def test_get_starships(self):
        starships = get_starships(self.filename)
        self.assertEqual(len(starships), 19)
        self.assertEqual(type(starships["Luke Skywalker"]), list)
        self.assertEqual(starships['Biggs Darklighter'][0], 'X-wing')

    # def test_calculate_bmi(self):
    #     bmi = calculate_bmi(self.filename)
    #     self.assertEqual(len(bmi), 59)
    #     self.assertAlmostEqual(bmi['Greedo'], 24.73)
    
if __name__ == "__main__":
    unittest.main(verbosity=2)
