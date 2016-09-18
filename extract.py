import json

##################################################

question_index = []

answer_index = {
	# question_index : list of answer_index
	# example
	# 0 : [0, 1, 2]
}

##################################################


items = []

# REMEMBER TO CHANGE SOURCE PATH
with open("data/data_2015-07-01-2015-12-31_java.json", "r") as source:
	data = json.load(source)

	for i in question_index:
		items.append({
			"body" : data["items"][i]["body"],
			"tags" : data["items"][i]["tags"],
			"title" : data["items"][i]["title"],
			"link" : data["items"][i]["link"],
			"question_id" : data["items"][i]["question_id"]
		})

	# python 2 only
	for key,value in answer_index.iteritems():
		for i in value:
			items.append({
				"body" : data["items"][key]["answers"][i]["body"],
				"tags" : data["items"][key]["answers"][i]["tags"],
				"title" : data["items"][key]["answers"][i]["title"],
				"link" : data["items"][key]["answers"][i]["link"],
				"answer_id" : data["items"][key]["answers"][i]["answer_id"],
				"question_id" : data["items"][key]["question_id"]
			})

	
	# REMEMBER TO CHANGE TARGET PATH
	with open("api_mention/data_2015-07-01-2015-12-31_java_api_mention.json", "w") as target:
		target.write(json.dumps({"items" : items}))
		
