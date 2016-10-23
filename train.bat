SETLOCAL
CALL stanford-ner\init.bat
FOR /L %%i IN (0,1,3) DO (
    java edu.stanford.nlp.ie.crf.CRFClassifier -prop train/train-%%i.prop 2> train/train-log-%%i.txt
)
ENDLOCAL
