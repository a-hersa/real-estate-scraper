# real-estate-scraper
- [real-estate-scraper](#real-estate-scraper)
      - [Disclaimer:](#disclaimer)
  - [1. The code](#1-the-code)
  - [2. The deployment](#2-the-deployment)
  - [3. The Bash script](#3-the-bash-script)

#### Disclaimer:
<sub>This project is made for educational purposes as part of my learning journey. Although scraping publicly available data is legal in my country, you should inform yourself first.
I take no responsibility for what others may do with the code and I advise against intensive scraping which may take a toll on scraped websites.</sub>

## 1. The code
This code used Beautifulsoup and Requests fundamentally. These libraries were chosen against Scrapy as they provide more customization and allow for a more 'adhoc' implementation.

The idea behind the code is to introduce a 'root' url or url from the area we want to get propierties from. For example, Barcelona. The code will then find an 'index' or a list of areas that are part of the root. Then, the code will find all the result pages for each of the areas. These will be called 'page lists'. Finally, the code will scrap every page list and generate a csv with the results. The scraping process can be summarized as:

1. Finding an 'index' for each given 'root' urls.
2. Finding a 'page list' with all the result pages for each element of the index.
3. Scraping all 'page lists' or result pages.
4. Extract all data into a csv.

## 2. The deployment
I think it is worth mentioning how we can deploy the code and generate data periodically for later use in analysis or ML projects.

In my case, I had an old Raspberry Pi 2B at home. This devices are great for this purpose as they cost around 35€ and the electricity bill is only 1-2€ a year. The alternative would be paying for a virtual machine (VM) or a deployment platform such as AWS, Azure or Railway.app but that could easily cost 5-10€ a month.

Whether you opt for a Raspberry Pi or a VM, you could deploy easily for project following these simple steps:

1. Install Raspberry Pi OS or any other Linux distribution into your machine. If you don't want to use a monitor, set up SSH when creating the image. Later, you can connect through VNC if you find it easier.
2. Clone your code from github and set the '.env' file. You can use the 'env-template' file included in this repository. Set the root urls you want to scrap.
3. Install all dependencies from requirements.txt. I also recommend using pipenv if you plan to add more projects.
4. Create a bash script. I will share an example of bash script below.
5. Set up a cron job that executes the bash script. For example, use '0 0 1 * *' to run you code every first of the month.

## 3. The Bash script

```
#! /usr/bin/bash

cd /home/user/pi-share/real-estate-scraper
pipenv shell
python main.py
```
