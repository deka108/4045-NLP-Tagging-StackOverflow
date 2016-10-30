import nltk

with open("sentence.txt", "r") as source, open("result.txt", "a") as target:
 	for line in source:
 		text = nltk.word_tokenize(line)
 		target.write( "%s\n" % nltk.pos_tag(text) )

