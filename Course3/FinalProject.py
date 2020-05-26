
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import requests_with_caching
import json

def get_movies_from_tastedive(movie):
    baseurl = "https://tastedive.com/api/similar"
    payload = {'q': movie, 'type': 'movies', 'limit': '5'}
    r = requests_with_caching.get(baseurl, params = payload)
    py_data = json.loads(r.text)
    return py_data

def extract_movie_titles(response):
    list_of_movies = []
    for item in response['Similar']['Results']:
        list_of_movies.append(item['Name'])        
    return list_of_movies

def get_related_titles(movies):
    get_five_more = []
    for movie in movies:
        temp = get_movies_from_tastedive(movie)
        temp_list = extract_movie_titles(temp)
        for item in temp_list:
            if item not in get_five_more:
                get_five_more.append(item)                
    return get_five_more

#**************Another API***********#

def get_movie_data(movie):
    baseurl = "http://www.omdbapi.com/"
    payload = {'t': movie, 'r': 'json'}
    r = requests_with_caching.get(baseurl, params = payload)
    py_data = json.loads(r.text)
    return py_data

def get_movie_rating(py_data):
    rotten_tomatoes_rating = 0
    sources = py_data['Ratings']
    for source in sources:
        if source['Source'] == 'Rotten Tomatoes':
            rotten_tomatoes_rating = int(source['Value'][:-1])        
    return rotten_tomatoes_rating

#**********Final here**************#

def get_sorted_recommendations(list_of_titles):
    movies_with_values = {}
    titles = get_related_titles(list_of_titles)
    #print(titles)
    for title in titles:
        pyd = get_movie_data(title)
        movies_with_values[title] = get_movie_rating(pyd) 
    #print(movies_with_values)
    sorted_movies = sorted(movies_with_values, key = lambda k: (movies_with_values[k], k), reverse = True)
    print(sorted_movies)
    return sorted_movies
