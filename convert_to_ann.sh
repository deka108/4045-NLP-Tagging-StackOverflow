for i in {0..3}
do
	cp train/test-$i.txt brat/data/gold/test-$i.txt
	python2 brat/tools/BIOtoStandoff_utf8.py train/test-$i.txt train/result-$i.tsv 0 1 > brat/data/gold/test-$i.ann
	cp train/test-$i.txt brat/data/classifier/test-$i.txt
	python2 brat/tools/BIOtoStandoff_utf8.py train/test-$i.txt train/result-$i.tsv 0 2 > brat/data/classifier/test-$i.ann
done
