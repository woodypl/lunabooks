# Lunabooks
Scripts to manage Uber bookkeeping with ifirma.pl
This is a collection of Python scripts to meet a rather esoteric requirement of automated bookkeeping.
It pulls a collection of PDFs (exported from Uber Partner website) and adds them to ifirma.pl accountancy software.

The rationale for the above is that, unfortunately, appropriate APIs are not available.

## Prerequisites

* Python3
* pip
* selenium

## Usage

```
git clone git@github.com:woodypl/lunabooks.git
cd lunabooks
pip install -r REQUIREMENTS
```
Create a file `passwords.py` with the login details for ifirma.pl:

```
IFIRMA_USER = ''
IFIRMA_PASS = ''
```

You can now use `lunabooks.py` for adding invoices and `destroy.py` for removing them (careful!).

## Technical notes

This is based on Selenium and will never be perfect. Some of the code is subject to load timing and weird behaviour might occur.
Thus, this is more a proof-of-concept script (that saved me hours of work) than a real project.

## Feedback

Comments and pull requests are most welcome.
