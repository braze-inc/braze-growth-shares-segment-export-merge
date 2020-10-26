# Braze User Export Segment Merge
This is a python 3 script which simplifies the process of combining multiple Braze Segment CSV export into a single file. The following file format is supported: `.gz`, `.zip`,`.txt`,`.tab`,`.csv`. When using a `tab` or `csv` delimited files, make sure the `delimiter` setting is set correctly.

## Requirements
The following are required:
* [python3](https://www.python.org/) installed
	* Optional, [venv](https://docs.python.org/3/library/venv.html) installed

## Process Steps
The following is an outline of the process:
* Edit the `.env` with any custom `exportfields` for output ie `external_id,email`. If using `combineonly`, then the files will only be combined. **Warning, please make sure all files are in the correct format, and that the header lines up. NO file transformation is done**
* Edit the `.env` with any `delimiter` and  `outputdelimiter` changes. ie `comma` or `tab`
* Run the script using `python3 merge_exports.py` to read the export files, extract the specific fields, and combine the files into one file.
* Results are saves it to the `outpath`

# Setup instructions
To run the script, [python3](https://www.python.org/) is required to be installed. Optionally, having [venv](https://docs.python.org/3/library/venv.html) installed is recommended.

## Configuration
The easiest way to setup the configuration is to create a `.env` file in the same path as the script. See [.sample_env](.sample_env) for an example to copy and `rename`.

### Configuration Settings
|Setting|Description|Example value|
|----|----|----|
|exportfields|Fields to be read from the csv files. **Ensure all capitalization matches the exports**|external_id,attr_1,attr_2|
|combineonly|Boolean - false, enable to only combine the files, and csv columns will not be parsed. **WARNING: Ensure all columns are align in all files** |false|
|outputpath|Folder to place the results in. Make sure the folder exist.|done|
|outputname|Output File prefix name|braze_export|
|fileformat|File format to read the files, set to `comma`,`tab` or `json`| comma|
|outputdelimiter|File format to write the files, set to `comma` or `tab`| comma|

# Running the Script
To run the script use `python3 merge_exports.py`. This will read each export zip file from the `exportdir`, process the files based on the `fileformat`, and place the resulting file into the `outputpath` folder. For file format of `json`, the process will parse the file as `json` prior to converting it to the output format.

## Install dependency
Use `pip3 install -r requirements.txt` to installed the dependencies. See [Using Virtual environment](#using-virtual-environment) below to avoid dependency issues.

## Using Virtual environment
To avoid dependency issues, it's recommend to use venv.
* `python3 -m venv ./.export` - creates the virtual environment
* `source .export/bin/activate` - activate the virtual environment
* `pip3 install -r requirements.txt` - install dependency if not already installed
* `python3 merge_exports.py` - runs the script for processing the export files
