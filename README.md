# Poseidon 

Demo developed for the Citi Venture's Economic Mobility challenge at [MIT-FinTech 2018 hackathon](http://www.mitfintech.com/fintech-hackathon/), which took place April 20-22 at the MIT Media Lab. My team was awarded the second prize. 

[See demo of output for cyber+security here](http://www.keldlundgaard.com/poseidon_scores_cyber_security_USA.html)

We find the competitiveness of hiring for each city by combining number of relevant jobs listed with number of resumes and an affortability factor. 

## Requirements
- python 3.5+
- pip3 install -e requirements.txt

## Order to run notebooks 
0. `jupyter notebook` -- to start jupyter notebook
1. run job_scraping.ipynb  -- to scrape [indeed.com](https://www.indeed.com) for jobs
2. run resume_scraping.ipynb -- to scrape [indeed.com/resumes](https://www.indeed.com/resumes) for resumes
3. run affortability_scraping.ipynb  -- to scrape [numbeo.com](https://www.numbeo.com) for affortability statistics
4. run poseidon_scores_calculator.ipynb  -- to get Poseidon scores for cities and metropolitan areas. 

## Acknowledgement:
Scoping, ideation, and analysis was done in collaboration with Cyril Blank and Danny Fooba.

All code was written by Keld Lundgaard. 
