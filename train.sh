export CLASSPATH=$(find "./stanford-ner" -name '*.jar' | xargs echo | tr ' ' ':')
for i in {0..3}
do
	java edu.stanford.nlp.ie.crf.CRFClassifier -prop train/train-$i.prop
done