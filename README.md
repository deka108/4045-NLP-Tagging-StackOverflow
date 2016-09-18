# 4045-NLP
## Data collection
Our datasets include top voted 100 StackOverflow question posts included with their answer posts collected from 6 months period between 2011-2015. The data is obtained from [StackExchange API](https://api.stackexchange.com) and will be stored as JSON.

To generate the files:

1. Uncomment `generate_json_per_halfyear_java_tag(2015)` at line 207 of `filter.py`, and runs `python filter.py` to generate JSON files of SO posts **with Java tag**.
2. Uncomment `generate_json_per_halfyear(2015)` at line 204 of `filter.py`, and runs `python filter.py` to generate JSON files of SO posts without any tags.

## Data Preprocessing
### Data Viewing
To view the generated JSON file in a human-readable format, edit `index.html`. Select the JSON file by changing the index at line 77 `var path_to_file = path_name_javatag[indexToChange]`. Open `index.html` in your browser.

Todo @pciangm, @stefan0010
- [ ] clean JSON data
- [ ] summary statistics

## Data Analysis
