# Copyright (C) Fabio Ciani, 2021
# Written by Fabio Ciani <fabio1.ciani@mail.polimi.it>, October 2021

# Thanks to Ben Dodson <https://github.com/bendodson> and u/severedxties <https://www.reddit.com/user/severedxties/> for the research and open-source codes.

# https://bendodson.com/projects/itunes-artwork-finder/
# https://artwork.themoshcrypt.net/

import requests

# Prepare for API call.
baseUrl = ["https://itunes.apple.com/search?term=", "&country=it&media=music&entity="]

# Ask the desired output to the user.
allowedEntities = ["song", "album", "artist"]
entity = input("Would you like to search a song, an album, or an artist?\n")

# Look for errors.
if not(entity in allowedEntities):
    raise Exception("An unprocessable entity was provided.")

# Acquire search item.
term = input("Please, write it down.\n")
term = term.replace(" ", "+")

# Generate API call.
url = baseUrl[0] + term + baseUrl[1] + entity

# Parse and use the first result to build a valid artwork link.
response = requests.get(url)
parsedResponse = response.json()
parsedDict = parsedResponse["results"][0]

artworkUrl = parsedDict["artworkUrl100"]
artworkUrl = artworkUrl.replace("100x100bb", "600x600-999")

pathIndex = artworkUrl.find("image")
artworkPath = artworkUrl[pathIndex:]

# Make the final URLs.
highResolutionUrl = "http://is5.mzstatic.com/" + artworkPath
print(highResolutionUrl)

losslessIndex = artworkPath.find("Music")
losslessUrl = "https://a1.mzstatic.com/us/r1000/063/" + artworkPath[losslessIndex:-16]
print(losslessUrl)