# 4045-NLP
## Data collection
Our datasets include top voted 100 StackOverflow question posts included with their answer posts collected from 6 months period between 2011-2015. The data is obtained from [StackExchange API](https://api.stackexchange.com) and will be stored as JSON.

To generate the files:

1. Uncomment `generate_json_per_halfyear_java_tag(2015)` at line 207 of `filter.py`, and runs `python filter.py` to generate JSON files of SO posts **with Java tag**.
2. Uncomment `generate_json_per_halfyear(2015)` at line 204 of `filter.py`, and runs `python filter.py` to generate JSON files of SO posts without any tags.

## Data Preprocessing
### Data Viewing
To view the generated JSON file in a human-readable format, open `index.html`. Then, open the developer console and call one of the following methods:

1. `displayJsonData(path_to_post_json)` to display the raw JSON data. Replace `path_to_post_json` with either:
  * `path_name_javatag[index]` to display top voted 100 question posts with answers that are tagged with Java and replace `index` with a number from 0-9.
  * `path_name_notag[index]` to display any top voted 100 question posts with answers and replace `index` with a number from 0-9.

2. `displayJsonApiMention(path_to_api_mention_json)` to display the extracted API mention for ground truth. Replace `path_to_api_mention_json` with `api_mention_javatag[index]` and replace `index` with a number from 0-9.

Todo @pciang, @stefan0010
- [ ] clean JSON data
- [ ] summary statistics

## Data Analysis
