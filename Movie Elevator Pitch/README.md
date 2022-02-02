# movie-success-prediction-nlp


**File Descriptions**
* _NLP_baseline.ipynb_ - File for the baseline model
* _NLP_models.ipynb_ - File for Model01 and Model 02.
* _/scraping/webScraping.py_ - Python script for web-scraping IMDB data
* _/data/IMDb_rating.csv_ - Input for the webScraping.py from which the IMDB ids are obtained.
* _/data/imdb_scraped.csv_ - Scraped data which is our final dataset. 



**Running the file**

1) Open the .ipynb file "NLP_baseline.ipynb" and "NLP_models.ipynb"

2) Import the CSV file "data/imdb_df.csv" (Kindly modify the path to your respective file locations' relative path)

3) All the required library installations, have been hardcoded in the notebook. 

4) Hence, execute the jupyter notebook cell by cell, would inturn reproduce the showcased results.

5) Running the python WebScraping.py 
```buildoutcfg
python /scraping/webScraping.py --config_file /scraping/config.ini
```