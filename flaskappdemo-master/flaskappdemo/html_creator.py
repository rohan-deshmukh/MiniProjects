from content_management import Content 
import os

TOPIC_DICT = Content()


HTML_TEMPLATE = """
{% extends "header.html" %}
{% block body %}

<body class = "body>

	<div class="container" align="left" style="max-width:800px">
		<div class="progress">
			<div class="progress-bar" role="progressbar" aria-valuenow="{{completed_percentages[%s]}}" \
			aria-valuemin="0" aria-valuemax="100" style="width: {{completed_percentages[%s]}}%;">
				%s Progress: {{completed_percentages[%s]}}%
			</div>
		</div>
		<h2>{{curTitle}}</h2>
		<br>

		<div class="embed-responsive embed-responsive-16by9"></div>

		<p></p>
		<p></p>
		<p></p>
		<p></p>

		<kbd data-toggle="collapse" data-target="#consoleinfo" aria-expanded="false" \
		aria-controls="consoleinfo">console</kbd>

			<div class="collapse" id="consoleinfo">
				<div class="well>
					<p>When someone refers to "the console," they are referring to where information from
					your program is output. You will see an example of "output to console" below. If you 
					want this message to go away, just click again on the "console" button that you 
					originally clicked on.</p>
				</div>
			</div>

			<div class="row">
			<div class="col-md-6">
			<pre class="prettyprint">
CODE HERE
			</pre>
			</div>
			<div class="col-md-6">
			<p>Explanation</p>
			</div>
			</div>

			<p>The next tutorial: <a title="{{nextTitle}}" href="{{nextLink}}?completed={{curLink}}">
			<button class="btn btn-primary">{{nextTitle}}</button></a></p>
	</div>

</body>

{% endblock %}

"""
for each_topic in TOPIC_DICT:
	print(each_topic)
	#os.makedirs(each_topic)
	os.makedirs('/Users/rohan/Documents/code/vagrant/FlaskApp/FlaskApp/templates/tutorials/'+ each_topic)

	for eachele in TOPIC_DICT[each_topic]:
		try:
			filename = (eachele[1]+'.html').replace("/", "")
			print(filename)
			#savePath = each_topic+'/'+filename
			savePath = '/Users/rohan/Documents/code/vagrant/FlaskApp/FlaskApp/templates/tutorials/' +each_topic+'/'+filename
			print(savePath)
			#saveData = (HTML_TEMPLATE.replace("%s", each_topic))
			saveData = ('/Users/rohan/Documents/code/vagrant/FlaskApp/FlaskApp/templates/tutorials/'+HTML_TEMPLATE.replace("%s", each_topic))
			template_save = open(savePath, "w")
			template_save.write(saveData)
			template_save.close()
		except Exception as e:
			print(str(e))


