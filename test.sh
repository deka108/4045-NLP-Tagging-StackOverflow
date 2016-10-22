export CLASSPATH=$(find "./stanford-ner" -name '*.jar' | xargs echo | tr ' ' ':')
for i in {0..3}
do
    java edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier train/api_mention-$i.ser.gz -testFile train/test-$i.tsv 1> train/result-$i.tsv 2> train/score-$i.txt
done