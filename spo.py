import sys
import spotipy
import spotipy.util as util
import json
import codecs

scope = 'user-library-read'

#token = util.prompt_for_user_token(username,scope,client_id='0acd1f153b25428fa508c8283aa590d2',client_secret='27e270a880f640a09ccaa2494208e5cc',redirect_uri='your-app-redirect-url')

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

#token = util.prompt_for_user_token(username, scope)
token = util.prompt_for_user_token(username,scope,client_id='0acd1f153b25428fa508c8283aa590d2',client_secret='27e270a880f640a09ccaa2494208e5cc',redirect_uri='http://google.es')

def generate_dataset(name,n_limit,dicti):
	with codecs.open('results.txt', 'w', encoding='utf-8') as the_file:
		stack = []
		ide = get_id_with_name(name)
		dicti[ide] = name
		artist_id,names = get_related_artists_id_with_artist(ide)
		for a in range(len(artist_id)):
			dicti[artist_id[a]] = names[a]
		the_file.write(generate_related_artists_string(ide,artist_id,100))
		stack.extend(artist_id)
		stack = list(set(stack))
		artists_already_processed = []
		artists_already_processed.append(ide)
		for i in range(n_limit-1):
			if i%20 == 0:
				token = util.prompt_for_user_token(username,scope,client_id='0acd1f153b25428fa508c8283aa590d2',client_secret='27e270a880f640a09ccaa2494208e5cc',redirect_uri='http://google.es')
			if len(stack) == 0:
				break
			ide = stack.pop()
			while ide in artists_already_processed:
				ide = stack.pop()
			artist_id,names = get_related_artists_id_with_artist(ide)
			for a in range(len(artist_id)):
				dicti[artist_id[a]] = names[a]
			artists_already_processed.append(ide)
			the_file.write(generate_related_artists_string(ide,artist_id,100))
			stack.extend(artist_id)
			stack = list(set(stack))

	with codecs.open('dictionaire.txt', 'wb',encoding='utf-8') as the_file:
		for key, value in dicti.iteritems():
			the_file.write(key + " " + value + "\n")



def generate_related_artists_string(ide,related_ids,n_repeated):
	string = ""
	for artist in related_ids:
		for i in range(n_repeated):
			string = string + ide + " " + artist + " "

	return string


def get_id_with_name(name):
	results = sp.search(q='artist:' + name, type='artist')
	data = json.dumps(results)
	data = json.loads(data)
	ide = data["artists"]["items"][0]["id"]
	return ide

def get_related_artists_id_with_artist(ide):
	artists = sp.artist_related_artists(ide)
	data = json.dumps(artists)
	data = json.loads(data)
	artists_json = data["artists"]
	results = []
	names = []
	for artist in artists_json:
		results.append(artist["id"])
		names.append(artist["name"])
	return results,names


if token:
	sp = spotipy.Spotify(auth=token)
	name = 'drake'
	dicti = {}
	generate_dataset(name,1500,dicti)
	#print ide
	
	#artists = sp.artist_related_artists(ide)
	#print json1

else:
    print "Can't get token for", username


