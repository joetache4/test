import os
import yaml
import shutil
from markdown import markdown
from contextlib import contextmanager


os.chdir(os.path.dirname(os.path.realpath(__file__)))


def slug(text):
	#slug = unicodedata.normalize('NFKD', text)
	#slug = re.sub(r'\'’', '-', slug)
	#slug = slug.encode('ascii', 'ignore').lower()
	#slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
	#slug = re.sub(r'[-]+', '-', slug)
	return text.replace(" ", "-").replace("'","").replace("’","").replace(",","").lower()


@contextmanager
def default_layout(file, title, path="."):
	file.write('<!DOCTYPE html>\n')
	file.write('<html lang="en">\n')
	file.write('<head>\n')
	file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
	file.write(f'<title>{title}</title>\n')
	file.write(f'<meta name="apple-mobile-web-app-title" content="{title}"/>\n')
	file.write(f'<script src="{path}/scripts.js"></script>\n')
	file.write(f'<link rel="stylesheet" href="{path}/style.css"/>\n')
	file.write('<meta name="viewport" content="width=device-width, initial-scale=1"/>\n')
	file.write(f'<link rel="shortcut icon" sizes="200x200" type="image/png" href="{path}/img/icon_200x200.png"/>\n')
	file.write(f'<link rel="shortcut icon" type="image/x-icon" href="{path}/img/favicon.ico"/>\n')
	file.write(f'<link id="icon60" rel="apple-touch-icon" href="{path}/img/icon_60x60.png?v=2"/>\n')
	file.write(f'<link id="icon76" rel="apple-touch-icon" sizes="76x76" href="{path}/img/icon_76x76.png?v=2"/>\n')
	file.write(f'<link id="icon120" rel="apple-touch-icon" sizes="120x120" href="{path}/img/icon_120x120.png?v=2"/>\n')
	file.write(f'<link id="icon152" rel="apple-touch-icon" sizes="152x152" href="{path}/img/icon_152x152.png?v=2"/>\n')
	file.write(f'<link rel="image_src" href="{path}/img/icon_256x256.png"/>\n')
	file.write('<meta name="HandheldFriendly" content="true"/>\n')
	file.write('<meta name="apple-mobile-web-app-capable" content="no"/>\n')
	file.write('<meta name="robots" content="noindex,nofollow,disallow"/>\n')
	file.write('<meta name="referrer" content="none"/>\n')
	file.write('</head>\n')
	file.write('<body>\n')
	yield
	file.write('</body>\n')
	file.write('</html>\n')


def generate_toc_plays(file, title, plays):
	with default_layout(file, title):
		file.write('<div class="play-index">\n')
		nav(file)
		for play in sorted(plays.keys()):
			file.write('<div class="play-title">\n')
			file.write(f'<h1><a href="{os.path.join(slug(play),"index.html")}">{play}</a></h1>\n')
			file.write('</div>\n')
		file.write('</div>\n')


def generate_toc_scenes(file, title, plays):
	with default_layout(file, title, ".."):
		file.write('<div class="scene-index">\n')
		nav(file, prev=None, menu="../index.html", succ=None)
		file.write('<div class="play-title selected">\n')
		file.write(f'<h1><a href="full.html">{title}</a></h1>\n')
		file.write('</div>\n')
		file.write('<div class="scenes">\n')
		lastgroup = 1
		for scene in plays[title]:
			thisgroup = scene.group
			if thisgroup != lastgroup:
				file.write('<br />\n')
			lastgroup = thisgroup
			file.write('<div class="scene-title">\n')
			file.write(f'<h2><a href="{slug(scene.title)+".html"}">{scene.title}</a></h2>\n')
			file.write('</div>\n')
		file.write('</div>\n')
		file.write('<br />\n')
		nav(file, prev=None, menu="../index.html", succ=None)
		file.write('</div>\n')


def generate_full_play(file, title, plays):
	with default_layout(file, title, ".."):
		file.write('<div class="full-play">\n')
		nav(file, prev=None, menu="../index.html", succ=None)
		file.write('<div class="play-title selected">\n')
		file.write(f'<h1>{title}</h1>\n')
		file.write('</div>\n')
		for scene in plays[title]:
			scene_content(file, scene)
		nav(file, prev=None, menu="../index.html", succ=None)
		file.write('</div>\n')


def generate_scene(file, title, plays):
	with default_layout(file, title, ".."):
		play_title, scene_title = title.split(": ")
		scenes = plays[play_title]
		scene = next(s for s in scenes if scene_title==s.title)
		try:
			prev = next(f"{slug(s.title)}.html" for s in scenes if s.order==scene.order-1)
		except StopIteration:
			prev = ""
		try:
			succ = next(f"{slug(s.title)}.html" for s in scenes if s.order==scene.order+1)
		except StopIteration:
			succ = ""		
		file.write('<div class="single-scene">\n')
		nav(file, prev=prev, menu="index.html", succ=succ)
		file.write('<div class="play-title selected">\n')
		file.write(f'<h1>{play_title}</h1>\n')
		file.write('</div>\n')
		scene_content(file, scene)
		nav(file, prev=prev, menu="index.html", succ=succ)
		file.write('</div>\n')


def scene_content(file, scene):
	file.write('<div class="scene">\n')
	file.write(f'<div class="scene-title"><h2>{scene.title}</h2></div>\n')
	file.write('<table class="scene-table" onclick="javascript:toggle_col();">\n')
	for item in scene.text:
		try:
			file.write('<tr>\n')
			if item.os and item.ms:
				file.write('<td class="left stage">\n')
				file.write(f'{markdown(item.os)}\n')
				file.write('</td>\n')
				file.write('<td class="right stage secondary">\n')
				file.write(f'{markdown(item.ms)}\n')
				file.write('</td>\n')
			elif item.os:
				raise Exception()
			elif item.ms:
				raise Exception()
			else:
				file.write('<td class="left">\n')
				if item.sp:
					file.write(f'<b>{item.sp}</b>\n')
				for line in item.o:
					file.write(f'{markdown(line)}\n')
				file.write('</td>\n')
				file.write('<td class="right secondary">\n')
				if item.sp:
					file.write(f'<b>{item.sp}</b>\n')
				for line in item.m:
					file.write(f'{markdown(line)}\n')
				file.write('</td>\n')
			file.write('</tr>\n')
		except Exception as e:
			print(item)
			raise e
	file.write('</table>\n')
	file.write('</div>\n')


def nav(file, prev=None, menu=None, succ=None):
	file.write('<div class="nav no-print">\n')
	file.write('<h3>\n')
	if prev is None:
		file.write('<span class="hidden">PREV |</span>\n')
	elif prev == "":
		file.write('<span class="disabled">PREV</span> |\n')
	else:
		file.write(f'<a href="{prev}">PREV</a> |\n')
	if menu:
		file.write(f'<a href="{menu}"> MENU </a>\n')
	else:
		file.write('<span class="hidden"> MENU </span>\n')
	if succ is None:
		file.write('<span class="hidden">| NEXT</span>\n')
	elif succ == "":
		file.write('| <span class="disabled">NEXT</span>\n')
	else:
		file.write(f'| <a href="{succ}">NEXT</a>\n')
	file.write('</h3>\n')
	file.write('</div>\n')



plays = {}
for play in os.listdir('plays'):
	play_dir = os.path.join('plays', play)
	if not os.path.isdir(play_dir):
		continue
	plays[play] = []
	for scene in os.listdir(play_dir):
		scene_path = os.path.join(play_dir, scene)
		with open(scene_path, 'r', encoding="utf-8") as file:
			plays[play].append(yaml.safe_load(file))
	plays[play].sort(key=lambda x: x['order'])

class AttrDict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def __missing__(self, key):
		return None
	def __getattr__(self, attr):
		return self[attr]
	def __setattr__(self, attr, value):
		self[attr] = value

def convertDict(a):
	if type(a) is list:
		return [convertDict(b) for b in a]
	elif type(a) is dict:
		return AttrDict({x:convertDict(y) for x,y in a.items()})
	else:
		return a

plays = convertDict(plays)

site_dir = 'docs'

with open(os.path.join(site_dir, 'index.html'),'w', encoding="utf-8") as outfile:
	generate_toc_plays(outfile, "Shakespeare Translated", plays)
for play,scenes in plays.items():
	play_dir = os.path.join(site_dir, slug(play))
	os.makedirs(play_dir, exist_ok=True)
	with open(os.path.join(play_dir,'index.html'), 'w', encoding="utf-8") as file:
		generate_toc_scenes(file, play, plays)
	for scene in scenes:
		scene_path = os.path.join(play_dir,slug(scene.title)+".html")
		with open(scene_path, 'w', encoding="utf-8") as file:
			print(f"{play}: {scene.title}")
			generate_scene(file, f"{play}: {scene.title}", plays)
	full_path = os.path.join(play_dir,'full.html')
	with open(full_path, 'w', encoding="utf-8") as file:
		generate_full_play(file, play, plays)

input("Build Complete")