# fec_linker
Using the bulk public data downloadable here https://www.fec.gov/data/browse-data/?tab=bulk-data from the FEC I have created a script to link all donations to and from politicians together. (~50 gbs)
 - doing this creates a huge network that can't be rendered above like .5 fps so a search script was designed

Step 1: run fec.py in the directory with your downloded data
Step 2: depending on what you want to do run either search.py or fec_processing.py
 - search.py allows you to search a politicians name and presents the user with a network centered around just that candidate ex: biden, joseph
 - fec_processing.py creates a huge network that takes forever to make and even longer to view up close, best for just a screenshot
