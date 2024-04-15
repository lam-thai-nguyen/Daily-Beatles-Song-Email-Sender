import requests
from bs4 import BeautifulSoup
import random


class CantReadSong(Exception):
    pass


def choose_song():
    # Send request
    url = "https://www.brianhartzog.com/beatles/beatles-alphabetical-list-of-all-lyrics.htm"
    response = requests.get(url).text
    
    # Create bs4 instance
    soup = BeautifulSoup(response, "lxml")
    
    # Choose a song
    song_list = []
    tables = soup.find_all('table')[3:29]
    for table in tables:
        songs = table.find_all('a')
        for song in songs:
            song_url = 'https://www.brianhartzog.com/beatles/' + song['href']
            song_list.append(song_url)
    
    return random.choice(song_list)


def get_song(url):
    print(f"=======REQUESTING {url}==========")
    # Send request
    response = requests.get(url).text

    # Create bs4 instance
    soup = BeautifulSoup(response, "lxml")

    # Extract desired results
    try:
        table_data = soup.find_all("td")[2]
    except:
        raise CantReadSong("The link may be dead. Run the script again")
    name = table_data.h2.text

    song = {}
    song_info = table_data.find_all("td")
    for i, info in enumerate(song_info):
        if i % 2 == 0:
            song[info.text] = ""
        else:
            song[list(song.keys())[i // 2]] = info.text

    lyrics = table_data.find_all("p")

    with open(f"songs/{'-'.join(name.split())[1:-1]}.txt", "w") as f:
        f.write(f"{name[1:-1].upper()}")

        f.write("\n\n")

        for key in song:
            f.write(f"{key} {song[key]}\n")

        f.write("\n")

        for i, p in enumerate(lyrics[:-1]):
            lines = p.text.split("        ")
            for line in lines:
                f.write(line)

            if i == 0:
                f.write("\n")
            else:
                f.write("\n\n")
       
    save_path = f"songs/{'-'.join(name.split())[1:-1]}.txt"  
    return save_path


if __name__ == "__main__":
    while True:
        url = choose_song()
        save_path = get_song(url)
        with open(save_path, 'r') as f:
            if len(f.readlines()) < 15:
                continue
        break
