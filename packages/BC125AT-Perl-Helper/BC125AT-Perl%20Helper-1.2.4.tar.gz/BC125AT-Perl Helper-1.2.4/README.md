# BC125AT-Perl Helper

A tool to convert [bc125at-perl](http://www.rikus.org/bc125at-perl)'s output to CSV and back for easy editing.

# Installation
Requires Python 3.6.  
`pip install bc125at-perl-helper`

# Features
* Converts `bc125at-perl`'s hard-to-read output to CSV (and back) for use in any spreadsheet editor.
* Includes **basic** validation (maximum name length, allowed modulations, etc...)
* Automatically read CSV from the scanner.
* Automatically write CSV files to the scanner.
* Clean your BC125AT - Automatically reset channels with no frequency.

# Notes
* *BC125AT-Perl Helper* does **not** support quotations in names.
* *BC125AT-Perl Helper* does **not** support `=>` in names.
* *BC125AT-Perl Helper* is **not** a replacement for `bc125at-perl`. You must properly install [bc125at-perl](http://www.rikus.org/bc125at-perl) first.
* **By default, all channels are offset by 1**. This means Bank 1 starts at row 2, Bank 2 starts at 52, etc...