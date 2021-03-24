# Install

Installation process for Linux, Mac and Windows WSL users:

## 1. Create virtual environment:

```
python -m venv .venv
```

Do it only when you creating project. Dont create it each time.

Sometimes it could be `python3`, `py`, `py3`

## 2. Activating virtual environment:

```
source .venv/bin/activate
```

## 3. Install libraries:

```
pip install -r requirements.txt
```

## 4. Create .env file:

Create `.env` file and add your credentials for DataForSEO API

```
LOGIN="your@email.com"
PASSWORD="y0uRpa5Sw0rD"
```

## 5. Create logs folder

Create `logs` folder in the same directory where you unpacked sripts
Then add `main.log` file to this category

# Usage

Don't forget that you need to activate virtual environment <b>before</b> using scripts

## How to Save results to file

To save result add `> filename.filetype` at the end of run string

Example:

```
python script_name.py > filename.csv
```

## keywords_search_volume.py

Will collect search volume from file and print out results.

It uses standart task method. That means that up to 700 keywords will be added to one task. Cost efficient
Returns json file with keyword/volume pairs

```
python keywords_search_volume.py
```

## keywords_for_keywrods.py

Collects keyword idias for given keyword
Add your keywords to `keywords.txt` and you good to go
Buy default script will look for `keywords.txt` file, but if you want you can add other file with the help of `--file` argument, but it's not mandatory to use

```
python keywords_for_keywrods.py
```

OPTIONAL:

```
python keywords_for_keywrods.py --file yourfilename.txt
```

## keywords_for_site.py

Script will collect keywords for entered domain name

You need to add --domain as argument when you will run the script

Will print results in terminal as an outcome

```
python keywords_for_site.py --domain youdomain.com
```

## keywords_for_category.py

Will collect keywords for category
You can find list of categories in `category.csv` file
Use file `category.txt` to enter categories

Result will be printed to terminal

```
python keywords_for_category.py
```

# SERP parsing

## google_live_advanced_treads.py

This scrip is experimental. It uses live method (most expencive one).
Will work in threads

Required arguments:

`--keywords` - path to file with keywords. by defalut it's `keywords.txt`
`--line` - index of row with keywords. Index, not number. Index starts from 0

Supported arguments:
`--delimiter` - specify delimier. By default it's `|`
