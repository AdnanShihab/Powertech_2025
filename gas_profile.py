# %%
import requests

url = "https://api.opendata.ffe.de/opendata?id_opendata=12"

params = {
    "id_opendata": 12,
    "internal_id_1": 162
}

# check if the API is available by making a GET request to the /health endpoint
response = requests.get(url)
if not response.status_code == 200:
    print(f"API not available. Status code: {response.status_code}")
    print(response.json())
    exit()

print('API available.')

# fetch the data by making a GET request to the 'opendata' endpoint
# using the previously defined parameters
# response = requests.get(url + '/opendata', params=params)
#
# # check if the request was successful
# if not response.status_code == 200:
#     print(f"Request failed. Status code: {response.status_code}.")
#     print(response.json())
#     exit()
#
# print('Request successful.')

# get the response as a dictionary
data = response.json()
print(data.keys())

# print some of the metadata
print(f"id_opendata: {data['id_opendata']}")
print(f"title: {data['title']}")
# print(f"internal_id_1: {data['internal_id']}")

# print the first three data entries
for data_entry in data['data'][:]:
    print(data_entry)