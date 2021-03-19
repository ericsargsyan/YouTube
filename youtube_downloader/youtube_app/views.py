from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
import youtube_dl
import os
import datetime
from youtube_search import YoutubeSearch
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import URLS, Playlists, PlaylistURLS
from pytube import Playlist
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


class HomeView(View):
	def get(self, request):
		return render(request, "youtube_app/home.html")


class SupportView(View):
	def get(self, request):
		return render(request, 'youtube_app/support.html')


def _valid(url: str) -> bool:
	if url.startswith("https://www.youtube.com/"):
		return True
	return False


def is_playlist(url):
	split_url = url.split("&")
	for i in split_url:
		if i.startswith("list="):
			return True
	return False


def time_(seconds):
	duration = str(datetime.timedelta(seconds=seconds))
	if not duration.startswith("0"):
		return duration
	return duration[2:]


def embed_urls(urls):
	embedded_urls = []
	for url_to_be_embedded in urls:
		embedded_urls.append(url_to_be_embedded.replace("watch?v=", "embed/").split("&")[0])
	return embedded_urls


def extract_from_playlist(results, item="playlist"):
	result = []
	for dict_ in results["entries"]:
		for key, value in dict_.items():
			if key == item:
				result.append(value)
	return result


@login_required
def search_results(request):

	if request.method == "POST":
		url = request.POST.get('url')
		if _valid(url):
			if is_playlist(url):
				Playlists.objects.create(user=request.user, playlist_url=url)
				PlaylistURLS.objects.create(user=request.user, urls=url)

				playlist = Playlist(url)
				embedded_urls = embed_urls(playlist)

				context = {
					"playlist": url,
					"embedded_urls": embedded_urls
				}

				return render(request, "youtube_app/playlist_download.html", context)

			results = YoutubeSearch(url, max_results=1).to_dict()

		else:
			results = YoutubeSearch(url, max_results=8).to_dict()

			# videos = URLS.objects.all()
			# paginator = Paginator(videos, 8)
			# page_number = request.GET.get('page')
			# page_obj = paginator.get_page(page_number)

			urls = []
			image_urls = []

			# extract video url and image url

			for line in results:
				urls.append(line['url_suffix'])
				image_urls.append(line['thumbnails'][0].strip("\'"))

		context = {
			'results': results,
			# 'page_obj': page_obj
		}

		return render(request, 'youtube_app/search_result.html', context)
	return render(request, "youtube_app/search_result.html")


@login_required
def playlist_download(request, url):
	print("In playlist")
	ydl_opts = {'ignoreerrors': True}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		results = ydl.extract_info([url], download=False)
		playlist = extract_from_playlist(results, "webpage_url")

	print(playlist)
	embedded_urls = embed_urls(playlist)

	context = {
		"playlist": url,
		"embedded_urls": embedded_urls
	}

	return render(request, "youtube_app/playlist_download.html", context)


def playlist_mp4(request):
	url = str(Playlists.objects.all().filter(user=request.user).last())
	print(type(url))
	ydl_opts = {'ignoreerrors': True}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		results = ydl.extract_info(url, download=False)

	# playlist = extract_from_playlist(results, "webpage_url")

	playlist_folder = "Playlists"
	main_playlist = results["entries"][0]["playlist"]

	if request.method == "POST":
		if not os.path.exists(playlist_folder):
			os.mkdir(playlist_folder)
		os.chdir(playlist_folder)
		if not os.path.exists(main_playlist):
				os.mkdir(main_playlist)
		os.chdir(main_playlist)

		ydl_opts = {'ignoreerrors': True}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])

		os.chdir(os.path.join('..', '..'))
	print(os.getcwd())
	# print(url)
	return HttpResponse("It Works!!!!")


@login_required
def download(request, id):
	video_url = f"https://www.youtube.com/watch?v={id}"
	commafy = lambda num: f"{num:,}"
	ydl_opts = {}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		meta = ydl.extract_info(video_url, download=False)

	views = commafy(meta['view_count'])
	likes = commafy(meta['like_count'])
	dislikes = commafy(meta['dislike_count'])
	duration = time_(meta['duration'])

	info = {'views': views,
			'likes': likes,
			'dislikes': dislikes,
			'duration': duration,
			'title': meta['title'],
			'id': id
			}

	filename = f"{info['title']}"
	video_folder = "videos"
	options = {
		'outtmpl': filename,
	}

	if not URLS.objects.filter(user=request.user, url=video_url).exists():
		URLS.objects.create(user=request.user, url=video_url)

	if request.method == "POST":
		URLS.objects.create(user=request.user, url=video_url)
		if not os.path.exists(video_folder):
			os.mkdir(video_folder)
		os.chdir(video_folder)
		with youtube_dl.YoutubeDL(options) as ydl:
			# messages.success(request, "The video have been successfully downloaded!")
			ydl.download([video_url])
		os.chdir("..")

		return redirect('success_massage')
	return render(request, "youtube_app/download.html", info)


class HistoryView(LoginRequiredMixin, ListView):
	template_name = "youtube_app/history.html"
	model = URLS
	paginate_by = 8

	def get_queryset(self):
		starting_time = datetime.datetime.now()  # .strftime('%m/%d/%Y, %H:%M:%S')
		print(f"Starting Time: {starting_time.strftime('%m/%d/%Y, %H:%M:%S')}")
		urls_history = URLS.objects.all().filter(user=self.request.user.id)
		urls_to_send = []
		for url_to_be_embedded in urls_history:
			urls_to_send.append(str(url_to_be_embedded))

		embedded_urls = embed_urls(urls_to_send)

		print(f"Code Execution Time: {(datetime.datetime.today() - starting_time).seconds}")

		return embedded_urls

	def post(self, request):
		urls_history = URLS.objects.all().filter(user=self.request.user.id)
		urls_history.delete()
		return redirect('profile_page')


@login_required
def download_audio(request, pk):
	audio_folder = "songs"
	if request.method == "POST":
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		URLS.objects.create(user=request.user, url=f'http://www.youtube.com/watch?v={pk}')

		if not os.path.exists(audio_folder):
			os.mkdir(audio_folder)
		os.chdir(audio_folder)
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:

			ydl.download([f'http://www.youtube.com/watch?v={pk}'])
		os.chdir("..")

		# messages.success(request, "The video have been successfully downloaded!")

		return redirect('success_massage')
	return render(request, "youtube_app/download.html")


class MassageView(LoginRequiredMixin, View):

	def get(self, request):
		return render(request, "youtube_app/success_message.html")


def playlist_history(request):
	url = PlaylistURLS.objects.all().filter(user=request.user.id)

	for get_url in url:
		playlist_url = get_url

	playlist = Playlist(str(playlist_url))

	urls_to_embed = [video for video in playlist]
	embedded_urls = embed_urls(urls_to_embed)

	print(embedded_urls)

	return render(request, "youtube_app/playlist_history.html", {"videos": embedded_urls})


# class PlaylistHistory(LoginRequiredMixin, View):
# 	template_name = "youtube_app/playlist_history.html"
# 	model = Playlists
# 	paginate_by = 8
#
# 	def get_queryset(self):
# 		urls_history = Playlists.objects.all().filter(user=self.request.user.id)
# 		urls_to_send = []
# 		for url_to_be_embedded in urls_history:
# 			urls_to_send.append(str(url_to_be_embedded))
#
# 		embedded_urls = embed_urls(urls_to_send)
# 		return embedded_urls
#
# 	def post(self, request):
# 		urls_history = URLS.objects.all().filter(user=self.request.user.id)
# 		urls_history.delete()
# 		return redirect('profile_page')
