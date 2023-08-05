# Description on how the script works

translateFeedback is a python script that parses strings in a column of a spreadsheet, send them to Bing translator and store the translation back in another column in the spreadsheet.

## Standalone use

You can pull down the [translateFeedback.py](https://github.com/ericvt/feedback_autotranslate/blob/master/script/translateFeedback.py) module directly and execute it in python environment
It uses Python 3.x and you'll need openpyxl, requests, uuid modules to be installed

## Automated via Github Action

A github action has been enable in this repo. Whenever a new check-ins occur, translateFeedback.py will be executed against the spreadsheet [text.xlsx](https://github.com/ericvt/feedback_autotranslate/blob/master/test.xlsx).
Feel free to overwrite this text.xlsx spreasheet with your own.

* note: at the moment, the script will run the translation against column#20 from Japanese to English (more to come)

## Usage

python3 translateFeedback.py {spreadsheet} {Column number to translate from} {Column number to translate to} {source language} {target language} {subscription key}

* note: the source language and target language code must be compliant with the Translation API language code, see [https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/language-support)
