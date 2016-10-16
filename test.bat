SETLOCAL
CALL stanford-ner\init.bat
java edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier api_mention.ser.gz -testFile test.tsv
ENDLOCAL
