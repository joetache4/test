---
layout: default
title: Debug
permalink: /debug/
---

<div class = "debug">

<p>Generated {{ site.time | date: "%F %r %z" }}</p>
<br />

{% for collection in site.collections %}
	{% unless collection.label == "posts" %}
	
		{% assign scenes = collection.docs %}
		
		{% assign err_count = 0 %}
		{% for scene in scenes %}
			{% unless scene.title %}
				{% assign err_count = err_count | plus: 1 %}
			{% endunless %}
		{% endfor %}
		
		{% if err_count == 0 %}
			<p>{{ "✅ " | append: collection.label }}</p>
		{% else %}
			<p>{{ "❌ " | append: collection.label | append: " ... " | append: err_count | append: " failed" }}</p>
			{% for scene in scenes %}
				{% unless scene.title %}
					{% assign path = scene.path | split: "/" %}
					<p>{{ "&emsp;&emsp;&emsp;&emsp;❌ " | append: path[1] }}</p>
				{% endunless %}
			{% endfor %}
		{% endif %}
		
	{% endunless %}
{% endfor %}

</div>