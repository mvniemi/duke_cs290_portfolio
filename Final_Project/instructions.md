1. generatemd.py should be placed into the Sakai main directory.
2. Do an initial run of `python generatemd.py build`
3. The `/report` directory will be created, the script will not complete though.
4. In `/report` there will be `csvout.csv`
5. Open it up and fill in the info for each package...it can also be left blank, though the first five columns must have data present(Bug). The order of the data is `packid,name,link,description,category`
6. Name the edited spreadsheet csvin.csv
7. Run `python generatemd.py build` again
8. The markdown reports are now in `/report`, if everything went well!
