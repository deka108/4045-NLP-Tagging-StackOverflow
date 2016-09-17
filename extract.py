import json

index = {
	# item index : list of ans index
	0 : [0,1,2],
	1 : []
}

items = []

# REMEMBER TO CHANGE SOURCE PATH
with open("data/data_2015-07-01-2015-12-31_java.json", "r") as source:
	data = json.load(source)

	# REMEMBER TO CHANGE TARGET PATH
	with open("api_mention/data_2015-07-01-2015-12-31_java_api_mention.json", "w") as target:
		# python 2
		for key,value in index.iteritems():

			if (value):
				items.append(
					{
						"body" : data["items"][key]["body"],
						"tags" : data["items"][key]["tags"],
						"title" : data["items"][key]["title"],
						"question_id" : data["items"][key]["question_id"],
						"answers" : [data["items"][key]["answers"][idx] for idx in value]
					})
			else:
				items.append(
					{
						"body" : data["items"][key]["body"],
						"tags" : data["items"][key]["tags"],
						"title" : data["items"][key]["title"],
						"question_id" : data["items"][key]["question_id"]
					})	


		target.write(json.dumps({"items" : items}))
