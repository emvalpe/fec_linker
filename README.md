# fec_linker
Using the bulk public data downloadable here https://www.fec.gov/data/browse-data/?tab=bulk-data from the FEC I have created a script to link all donations to and from politicians together. 

Sadly this large of a network is impossible to render and use so its just a pretty piture for now.
 - working on a script to search the files for politician names to track donations to specific people

Notes:
 - data is approximately 50 GB so it will need a good amount of space on a drive.

Steps:
 - Run fec.py to extract all important information from the raw data and save it to new files
 - fec_processing.py is used to generate the full network, that really only works to create a nice screenshot.
