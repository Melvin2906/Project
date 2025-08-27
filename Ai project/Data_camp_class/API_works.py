from urllib.request import urlopen

with urlopen('http://localhost:3000/lyrics/') as response:
  
  # Use the correct function to read the response data from the response object
  data = response.read()
  encoding = response.headers.get_content_charset()

  # Decode the response data so you can print it as a string later
  string = data.decode(encoding)
  
  print(string)


  # Import the requests package
import requests

# Pass the API URL to the get function
response = requests.get("http://localhost:3000/lyrics")

# Print out the text attribute of the response object
print(response.text)