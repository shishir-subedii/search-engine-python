This is a simple search engine made in python using web crawling. 
It is not optimized and it can take long time to execute once the data size gets big and it might have some bugs.
You type a prompt in terminal and search.py will find top 10 websites according to your prompt --> No rocket science.

Files:
1. web_crawler.py -> this will crawl the websited from seed_urls to other urls on the internet and adds title, meta description and url links of every web page it finds to crawled_data.csv(it will create one if there is no such file) file.
2. search.py -> this will ask you a prompt and break down that prompt into words and filter out top 10 websites according to your prompt and print it. This is the actual search engine
3. temp_crawler.py -> (ignore this file) This just works it was used to save the progress while creating web_crawler.py

HOW TO USE?
1. install python and required packages:

2. open terminal and run web_crawler.py file to keep extracting and saving url data from internet(This is optional do don't have to run it in order to use search function).

3. open another terminal and run search.py 

->use the search engine. 