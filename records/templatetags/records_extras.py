from django import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

def twitch_embed(url, width, height):
	match = re.search(r'^(?P<channel>[^/]+)/c/(?P<id>[^/]+)$', url)
	channel = match.group('channel')
	id = match.group('id')

        if channel and id:
		return ('<object bgcolor="#000000" data="http://www.twitch.tv/widgets/archive_embed_player.swf" '
		'height="{0}" id="clip_embed_player_flash" type="application/x-shockwave-flash" '
		'width="{1}"><param name="movie" value="http://www.twitch.tv/widgets/archive_embed_player.swf" />'
		'<param name="allowScriptAccess" value="always" /><param name="allowNetworking" value="all" />'
		'<param name="allowFullScreen" value="true" />'
		'<param name="flashvars" value="channel={2}&start_volume=25&auto_play=false&chapter_id={3}" /></object>').format(height, width, channel, id)
	else:
		return ""

def yt_embed(url, width, height):
	match = re.search(r'^watch\?v=(?P<id>[A-Za-z0-9\-\_]+)$', url)
	id = match.group('id')
	if id:
            return ('<iframe id="ytplayer" type="text/html" width="{0}" height="{1}" '
  'src="http://www.youtube.com/embed/{2}" '
  'frameborder="0"></iframe>').format(width, height, id)
	else:
		return ""

embed_funcs = { "youtube.com": yt_embed, "twitch.tv": twitch_embed }

@register.filter(name='embed', is_safe=True)
@stringfilter
def embed(url, dims_string):
	dims = dims_string.split()
	match = re.search(r'^http://([A-Za-z0-9\-]+\.)?(?P<domain>[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+)/(?P<info>[A-Za-z0-9\-\_/\=\?]+)$', url)
	if match and match.group('domain') in embed_funcs:
		domain = match.group('domain')
		info = match.group('info')
		return embed_funcs[domain](info, dims[0], dims[1])
	else:
		return ""
