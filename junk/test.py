from youtube_search import YoutubeSearch
import datetime
# url = input("Enter Name: ")

# results = YoutubeSearch(url, max_results=1).to_dict()

# print(results)

# commafy = lambda num: f"{num:,}"


# print(commafy(123456789222))


# def time_(seconds):
# 	duration = str(datetime.timedelta(seconds=seconds))
# 	if not duration.startswith("0"):
# 		return duration
# 	return duration[2:]


# def time_(seconds):
# 	duration = str(datetime).timedelta(seconds=seconds)
# 	if not duration.startswith("0"):
# 		return duration

# 	temp = duration.split(":")
# 	minutes = f"{temp[1]}:{temp[2]}"
# 	return minutes

# print(time_(226))	




import os
import youtube_dl


# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 	meta = ydl.extract_info(url, download=True)
	# formats = meta.get('formats', [meta])

# get_formats = [f['format'].split(" ")[3][1:-1] for f in formats if f['format'][0] == "1"][1:]

# resolutions = list(dict.fromkeys(get_formats))

# for f in formats:
# 	fmts = []
# 	if f['format'] == "1":
# 		fmts.append(f['format'].split(" ")[0])

#

# youtube_dl.utils.DownloadError



# print(resolutions)

# options = {
# 	"format" : get_formats[-1],
# }

# with youtube_dl.YoutubeDL(options) as ydl:
# 	ydl.download([url])


# # print(get_formats)



# audio_folder = "songs"
# ydl_opts = {
# 	'format': 'bestaudio/best',
# 	'postprocessors': [{
# 		'key': 'FFmpegExtractAudio',
# 		'preferredcodec': 'mp3',
# 		'preferredquality': '360',
# 	}],
# }
# URLS.objects.create(user=request.user, url=f'http://www.youtube.com/watch?v={pk}')


# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 	ydl.download(['https://www.youtube.com/watch?v=dVvlmpo5g9k'], download=False)


# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 	meta = ydl.extract_info("https://www.youtube.com/watch?v=dVvlmpo5g9k&list=RDdVvlmpo5g9k", download=False)


# # info = {'views': meta['view_count'],
# # 			'likes': meta['like_count'],
# # 			'dislikes': meta['dislike_count'],
# # 			'duration': meta['duration'],
# # 			'title': meta['title'],
# 			# }
# print(meta)








audio_folder = "songs"

# ydl_opts = {
# 	'postprocessors': [{
# 		'key': 'FFmpegExtractAudio',
# 		'preferredcodec': 'mp4',
# 		'preferredquality': '192',
# 	}],
# }

ydl_opts = {}
url = "https://www.youtube.com/watch?v=dVvlmpo5g9k&list=RDdVvlmpo5g9k"

# if not os.path.exists(audio_folder):
# 	os.mkdir(audio_folder)
# os.chdir(audio_folder)

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	# ydl.download([url])
	results = ydl.extract_info(url, download=False)

for dict_ in results["entries"]:
	for key, value in dict_.items():
		if key == "playlist_title":
			print(value)



# for i in results:
# 	print(i['playlist_index'], i['webpage_url'])

# thumbnail
# playlist_index
# webpage_url
# playlist_title

# _type
# entries
# id
# title
# uploader
# uploader_id
# uploader_url
# extractor
# webpage_url
# webpage_url_basename
# extractor_key