import spotify
import scraper

month = 1
metroID = 11104 #SF = 26330, cbus = 9480, detroit = 18073, des moines = 12444, austin = 9179, nashville = 11104, ny = 7644
city = "Nashville"

playlistName = city + " " + "January"
shows = scraper.getMetro(metroID)

# filter shows by date and/or venue
filterShows = []
for i in shows:
    if int(i["Month"]) == month:
        filterShows.append(i)
venues = scraper.venueList(filterShows)
[print(i[0], " has ", i[1], " shows this month") for i in venues]

artists = scraper.artistList(filterShows)

# connect to spotify and make the playlist
# username = "31gjfh4nausgb4s4itd7nfyuzrh4"
# playlistID = spotify.makeUserPlaylist(username, playlistName)
# spotify.buildPlaylist(artists, playlistID, username)




