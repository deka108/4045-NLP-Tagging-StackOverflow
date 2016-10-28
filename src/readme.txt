[//TODO:
	1. Explain Dependencies
	2. The step by step process]

+=========================+
| Data Collection Process |
+=========================+
1. Dependencies:
	Python Requests
	StackExchange API

2. Download
	run python X.py

3. Use the HTML Viewer to select the posts
	3.1. Open index.html
	3.2. Open Developer console
		displayJsonData(datajavatag[x]);
		x can be replaced with any number from 0-9 depending on the half year between 2011-2016.
	3.3. Run extract.py to extract the posts.

+===============+
| Preprocessing |
+===============+
	At root folder:
		* Run preprocess.bat

	It will populate api_preprocessed/ with preprocessed post in text files for each half year from 2011-2015.


+========================+
| The Annotation Process |
+========================+
Using Brat annotation tool:
1. Dependencies:
	1.1. Git clone from https://github.com/nlplab/brat
	1.2. Install file_lock 
		pip install file_lock
	1.3. Python2, Brat tool is implemented using Python 2.7.11

2. Setup:
	2.1. Copy and replace into brat/ directory
		annotation.py
	2.2. Copy these files into brat/tools/ directory
		- BIOtostandoff_utf8.py
		- anntoconll_utf8.py
	2.3. Copy the text files and the configurations into data/ directory
	2.4. Run ./.install.sh
	2.5. Run python2 standalone.py to run the server

3. Annotation
	3.1. Navigate to home, and access to StackOverflow collection
		[insert link here]
	3.2. Annotate the api mention in the text
	3.3. Run ./anntoconll_utf8.sh to convert the brat .ann files to .conll and generates tokenize words with their respective BIO tags. Conll file is  a tabbed separated file consist of key term in the first column and the I, O, B tags in the second column.

+==========+
| Training |
+==========+
	Requirements:
		* JDK 1.8
		* Stanford NER (http://nlp.stanford.edu/software/CRF-NER.shtml#Download)

	- Windows
		At root folder:
			* Run split_all.bat
			* Run train.bat
			* Run test.bat

+======================+
| Evaluation Analysis  | 
+======================+
	Results and confusion matrices can be found in:
		* %ROOT%\train\result-0.tsv
		* %ROOT%\train\score-0.txt

		* %ROOT%\train\result-1.tsv
		* %ROOT%\train\score-1.txt

		* %ROOT%\train\result-2.tsv
		* %ROOT%\train\score-2.txt

		* %ROOT%\train\result-3.tsv
		* %ROOT%\train\score-3.txt

	result-*.tsv contains list of tokens with gold standard annotation and predicted annotation
	score-*.txt contains the confusion matrix for respective fold


Diff and Compare the Classification Results on Brat
	1. Run ___.sh
	Copy both the annotated gold standard and the annotated classifier results directories into data/ directory
	2. Run Brat Server
	3. Open
		http://localhost:8001/diff.xhtml#/gold/test-0?diff=/classifier
		The left will show the Gold Standard annotation and the Right will show the Classifier annotation results
