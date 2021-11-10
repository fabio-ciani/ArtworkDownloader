# Copyright (C) Fabio Ciani, 2021
# Written by Fabio Ciani <fabio1.ciani@mail.polimi.it>, October-November 2021

# Thanks to Ben Dodson <https://github.com/bendodson> and u/severedxties <https://www.reddit.com/user/severedxties/> for the research on the artwork URLs' structure and their open-source projects.
# Shout out to Karl Ding <https://github.com/karlding>, who managed to achieve a workaround regarding the download artists' images.

# https://bendodson.com/projects/itunes-artwork-finder/
# https://artwork.themoshcrypt.net/
# https://gist.github.com/karlding/954388cb6cd2665d4f3a

import requests

def getMusic():
    artworkURL = parsedDict["artworkUrl100"]
    artworkURL = artworkURL.replace("100x100bb", "600x600-999")

    pathIndex = artworkURL.find("image")
    artworkPath = artworkURL[pathIndex:]

    # Create final URLs.
    highResolutionURL = "http://is5.mzstatic.com/" + artworkPath
    print(highResolutionURL)

    losslessIndex = artworkPath.find("Music")
    losslessURL = "https://a1.mzstatic.com/us/r1000/063/" + artworkPath[losslessIndex:-16]
    print(losslessURL)

def getArtist():
    artistID = parsedDict["artistId"]
    artistURL = "https://music.apple.com/it/artist/" + str(artistID)

    # Extract artist image URL directly from HTML source.
    HTML = requests.get(artistURL).text
    tagIndex = HTML.find("<meta property=\"og:image\" content=\"")
    extensionIndex = HTML[tagIndex:].find(".png\">")

    # Calculate boundaries in order to obtain a link.
    start = tagIndex + 35
    end = tagIndex + extensionIndex + 4
    imgURL = HTML[start:end]

    # Apply the same strategy used in getMusic() method.
    imgURL = imgURL.replace("1200x630cw", "3000x3000-999")

    pathIndex = imgURL.find("image")
    imgPath = imgURL[pathIndex:]

    # Create final URLs.
    highResolutionURL = "http://is5.mzstatic.com/" + imgPath
    print(highResolutionURL)

    losslessIndex = imgPath.find("thumb")
    losslessURL = "https://a1.mzstatic.com/us/r1000/063/" + imgPath[losslessIndex + 6:-18]
    print(losslessURL)



# Prepare for API call.
baseURL = ["https://itunes.apple.com/search?term=", "&country=it&media=music&entity="]

# Ask the desired output to the user.
allowedEntities = {
    "song": "musicTrack",
    "album": "album",
    "artist": "musicArtist"
}

entity = input("Would you like to search a song, an album, or an artist?\n")

# Look for errors.
if not(entity in allowedEntities.keys()):
    raise Exception("An unprocessable entity was provided.")

# Acquire search item.
term = input("Please, write it down.\n")
term = term.replace(" ", "+")

print()

# Generate API call.
url = baseURL[0] + term + baseURL[1] + allowedEntities[entity]

# Parse and use the first result to build a valid artwork link.
response = requests.get(url)
parsedResponse = response.json()
parsedDict = parsedResponse["results"][0]

if not(entity == "artist"):
    getMusic()
else:
    getArtist()