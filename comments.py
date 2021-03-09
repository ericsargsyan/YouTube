
	# print('format      : ', meta['format'])

# class SearchResult(LoginRequiredMixin, ListView):
# 	template_name = 'search_download/download.html'
# 	paginate_by = 3
#
# 	# def get_queryset(self):
# 	# 	return self.model.objects.all().filter(user=self.request.user)


# class SearchResults(LoginRequiredMixin, ListView):
#
# 	template_name = "search_download/search_results.html"
# 	model = URLS
# 	paginate_by = 8
#
# 	# def get(self, request, *args, **kwargs):
# 	# 	return reverse("search_results")
#
# 	def get_success_url(self):
# 		return reverse("download_page")
#
# 	def post(self, request, *args, **kwargs):
# 		url = request.POST.get('url')
# 		if _valid(url):
# 			URLS.objects.create(user=request.user, url=url)
# 			ydl_opts = {}
# 			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 				meta = ydl.extract_info(url, download=False)
# 			title = meta['title']
#
# 			results = YoutubeSearch(title, max_results=1).to_dict()
# 		else:
# 			results = YoutubeSearch(url, max_results=22).to_dict()
# 			urls = []
# 			image_urls = []
#
# 			# extract video url and image url
#
# 			for line in results:
# 				urls.append(line['url_suffix'])
# 				image_urls.append(line['thumbnails'][0].strip("\'"))
#
#
# 		context = {
# 			'results': results
# 		}
#
# 		return redirect(self.success_url)
#
# 	def get(self, request):
# 		return reverse("search_results")
#
# 	def get_queryset(self):
# 		return self.model.objects.all().filter(user=self.request.user)






# def download(request):
# 	# url = request.GET.get('url')
# 	# # try:
# 	# if _validate(url):
# 	# 	youtube_object = YouTube(url)
# 	# # except VideoUnavailable:
# 	# # 	return render(request, "search_download/unavailable.html")
# 	#
# 	# 	embedded_url = url.replace("watch?v=", "embed/").split("&")[0]
# 	# 	resolutions = _get_resolutions(youtube_object)
# 	#
# 	# 	if request.method == "POST":
# 	# 		video = youtube_object.streams.first()
# 	#
# 	# 		downloaded = video.download()
# 	# 		# print(downloaded)
# 	# 		context = {
# 	# 			"resolutions": resolutions,
# 	# 			"embedded_url": embedded_url
# 	# 		}
# 	#
# 	# 	return render(request, "search_download/search_results.html")
# 	# else:
# 	# 	# results = youtube_search(url)
# 	# 	return render(request, "search_download/search_results.html")
# 	url = "https://www.youtube.com/watch?v=brdEmknYFmY"
# 	embedded_url = url.replace("watch?v=", "embed/").split("&")[0]
#
# 	videosSearch = VideosSearch('iriknajam', limit=5)
# 	context = {
# 		"url": embedded_url
# 	}
# 	return render(request, "search_download/search_results.html", context)





	# if request.method == "POST":
	# 	url = request.POST.get('url')
	# 	if _valid(url):
	# 		URLS.objects.create(user=request.user, url=url)
	# 		ydl_opts = {}
	# 		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	# 			meta = ydl.extract_info(url, download=False)
	# 		title = meta['title']
	#
	# 		results = YoutubeSearch(title, max_results=1).to_dict()
	# 	else:
	#
	# 		results = YoutubeSearch(url, max_results=20).to_dict()
	# 		urls = []
	# 		image_urls = []
	#
	#
	# 		for line in results:
	# 			urls.append(line['url_suffix'])
	# 			image_urls.append(line['thumbnails'][0].strip("\'"))
	#
	#
	# 	context = {
	# 		'results': results
	# 	}
	#
	# 	return render(request, 'search_download/search_results.html', context)
	#
	#
	# return render(request, "search_download/home.html")


			# paginator = Paginator(image_urls, 8)
			# page = request.GET.get('page', '1')
			# try:
			# 	page = paginator.page(page)
			# except PageNotAnInteger:
			# 	page = paginator.page(1)
			# except EmptyPage:
			# 	page = paginator.page(paginator.num_pages)
			# embedded_urls = []
			#
			# # embed urls for <iframe>
			#
			# for url_to_be_embedded in urls:
			# 	embedded_urls.append("https://www.youtube.com" + url_to_be_embedded.replace("watch?v=", "embed/").split("&")[0])