def Content():
	TOPIC_DICT = {"Basics": [["Introduction to Python", "/introduction-to-python-programming/"],
							["Print functions and Strings", "/python-tutorial-print-function-strings/"],
							["Math basics with Python 3", "/math-basics-python-3-beginner-tutorial/"],
							["Variables", "/python-3-variables-tutorial"]],
				  "Web Dev":[["Intro and environment creation", "/flask-web-development-introduction/"],
				  			["Basics, init.py, and your first Flask App!", "/creating-first-flask-web-app/"]]}

	return TOPIC_DICT

if __name__ == "__main__":
	x = Content()

	print(x["Basics"])

	for each in x["Basics"]:
		print(each[1])

	# for each in x["Web Dev"]:
	# 	print(each[1])