from urllib.request import urlopen, urlretrieve
from json import load
id2 = '4284013'
songId = load(urlopen('https://gdbrowser.com/api/level/'+id2))['songID']
songFile = load(urlopen('https://gdbrowser.com/api/level/'+id2))['songLink']
print([songId, songFile])
urlretrieve(songFile, str(songId)+'.mp3')