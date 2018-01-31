#!/bin/bash

pushd . > /dev/null
cd pdfs
for pdf in *; do
	pdftotext "$pdf" "../invoices/${pdf}.txt" && rm "$pdf"
done
popd > /dev/null

./lunabooks.py
