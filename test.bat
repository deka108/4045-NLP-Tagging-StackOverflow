SETLOCAL
CHCP 65001
CALL stanford-ner\init.bat
FOR /L %%i IN (0,1,3) DO (
    java edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier train/api_mention-%%i.ser.gz -testFile train/test-%%i.tsv 1> train/result-%%i.tsv 2> train/score-%%i.txt
)
ENDLOCAL