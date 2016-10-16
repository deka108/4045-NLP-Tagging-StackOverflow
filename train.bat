SETLOCAL
CALL stanford-ner\init.bat
java edu.stanford.nlp.ie.crf.CRFClassifier -prop train.prop
ENDLOCAL
