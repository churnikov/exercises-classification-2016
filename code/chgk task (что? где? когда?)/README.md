# What? Where? When? database downloader (Что? Где? Когда?)

With this script you can download all questions from "http://db.chgk.info/"

In terminal run this script by typing `load_chgk_database.py -o <FOLDER>`

#### Options in command:
- `-h` `--help`                 Show help screen.
- `--version`                   Show version.
- `-o FOLDER` `--output=FOLDER` Where to save images and pickle of questions
- `-s START` `--start=START`    Page to start parsing
- `-e END` `--end=END`          Page to end parsing

If neither **start page number** nor **end page number** is specified, then all database will be loaded.<br>
**start page number** and **end page number** are selected from [main page](http://db.chgk.info/) in the bottom
