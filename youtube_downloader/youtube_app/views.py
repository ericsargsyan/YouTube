from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
import youtube_dl
import os
import datetime
from youtube_search import YoutubeSearch
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import URLS
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def home(request):
	return render(request, "youtube_app/home.html")


def support(request):
	return render(request, 'youtube_app/support.html')


def _valid(url: str) -> bool:
	if url.startswith("https://www.youtube.com/"):
		return True
	else:
		return False


def time_(seconds):
	duration = str(datetime.timedelta(seconds=seconds))
	if not duration.startswith("0"):
		return duration
	return duration[2:]


@login_required
def download(request, id):

	commafy = lambda num: f"{num:,}"

	ydl_opts = {}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		meta = ydl.extract_info(f"https://www.youtube.com/watch?v={id}", download=False)

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

	URLS.objects.create(user=request.user, url=f'http://www.youtube.com/watch?v={id}')

	if request.method == "POST":
		video_url = f"https://www.youtube.com/watch?v={id}"
		URLS.objects.create(user=request.user, url=video_url)
		if not os.path.exists(video_folder):
			os.mkdir(video_folder)
		os.chdir(video_folder)
		with youtube_dl.YoutubeDL(options) as ydl:
			# messages.success(request, "The video have been successfully downloaded!")
			ydl.download([video_url])
		os.chdir("..")

		# return redirect("search_results")
		return redirect('success_massage')
	return render(request, "youtube_app/download.html", info)


@login_required
def search_results(request):

	if request.method == "POST":
		url = request.POST.get('url')
		if _valid(url):
			URLS.objects.create(user=request.user, url=url)
			ydl_opts = {}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				meta = ydl.extract_info(url, download=False)
			title = meta['title']

			results = YoutubeSearch(title, max_results=1).to_dict()
		else:

			results = YoutubeSearch(url, max_results=100).to_dict()

			videos = URLS.objects.all()
			paginator = Paginator(videos, 8)
			page_number = request.GET.get('page')
			page_obj = paginator.get_page(page_number)

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


def embed_urls(urls):
	embedded_urls = []
	for url_to_be_embedded in urls:
		embedded_urls.append(url_to_be_embedded.replace("watch?v=", "embed/").split("&")[0])
	return embedded_urls


@login_required
def history(request):
	urls_history = URLS.objects.all().filter(user=request.user.id)
	urls_to_send = []

	for url_to_be_embedded in urls_history:
		urls_to_send.append(str(url_to_be_embedded))

	embedded_urls = embed_urls(urls_to_send)
	videos = URLS.objects.all()
	paginator = Paginator(embedded_urls, 8)
	page_number = request.GET.get('page')

	page_obj = paginator.get_page(page_number)

	context = {"page_obj": page_obj}

	if request.method == "POST":
		urls_history.delete()
		return redirect("profile_page")
	return render(request, "youtube_app/history.html", context)


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
		# return redirect("search_results")
		return redirect('success_massage')
	return render(request, "youtube_app/download.html")


@login_required
def success_massage(request):
	return render(request, "youtube_app/success_massage.html")
