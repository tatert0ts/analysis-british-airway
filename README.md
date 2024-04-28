# British Airways Reviews EDA Dashboard

## Overview

This repository hosts an Exploratory Data Analysis (EDA) dashboard for British Airways reviews, using Plotly Dash. The dashboard provides insights into passenger sentiments, demographics, and trends based on a dataset obtained from Kaggle.

## Data Sources

The dataset is sourced from Kaggle: [British Airways Passenger Reviews 2016-2023](https://www.kaggle.com/datasets/praveensaik/british-airways-passenger-reviews-2016-2023).

## Files
1. **bair_dash.py**: Main file for running the Dash application on local host.
2. **britishairway_eda.ipynb** & **britishairway_sentiments.ipynb**: Jupyter Notebooks used for exploratory analysis and visualization setup before migration to bair_dash.py. These files may contain additional information not included in the dashboard.
3. **British_Airway_Review.csv**: Raw data file downloaded from Kaggle.
4. **British_Airway_Review_cleaned.csv**: Cleaned dataset created by britishairway.ipynb.
5. **style.css**: CSS file for formatting the layout of the webpage.


## Analysis Highlights

### Data Cleaning
- Introduced a new column "verified" based on the review column to enhance consistency.
- Ratings column was not utilized due to inconsistencies and lack of credibility.
    - Although the ratings ranged from 1 to 9 stars, only values of 1, 3, 5, 7, and 9 were observed, which diminishes the credibility of the column.
    - Initially, it was expected that the distribution of ratings would differ between those who recommended yes and those who recommended no. However, upon investigation, it was found that the distribution was rather similar. This raised concerns about the accuracy of the data, leading to the decision not to utilize this particular column.
    - ![newplot](https://github.com/tatert0ts/analysis-british-airway/assets/165807891/e551c8c2-c28a-48ab-9b95-416d5d24cb77)

### Exploratory Analysis
- Identified peaks and troughs in the number of reviews per month, with notable impacts from the COVID-19 pandemic.
    - number of reviews peaked a little shy of 70 reviews per month, around late 2016/early 2017
    - may 2020 to sept 2021 had especially low number of reviews recorded, due to covid 19 which played a major role in the disruotion of travel and flights. need to bear in mind when inferring insights during this time period as it is more variable
- Observed a higher proportion of negative reviews compared to positive ones, indicating areas for improvement in customer satisfaction.
- The majority of the reviews were from the economy class, followed by the business class, which aligns with expectations considering that most of the seats available for flights are in the economy class.
- Additionally, the first class received an average of 2.55 reviews per month, with zero or one review recorded only from July 2019 onwards.
- A significant portion of the sample originates from the UK.
- The demographic with the highest probability of being a consumer is couples who are leisure traveling and opt for economy class flights.


## Getting Started

### 1. Clone the Repository
```
git clone https://github.com/tatert0ts/analysis-british-airway.git
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run the Dashboard
```
python bair_dash.py
```

## Contributors
- Tan Jia Yin

*Potential Next Steps*

*- Analyze the percentage of available seats by seat type and assess correspondence with proportion of reviews from sample.*
*- Investigate significant differences in sentiments between different passenger groups.*
*- Categorize positive and negative reviews into different factors for deeper insights.*
*- Compare seasonal trends, such as holiday periods and pre/post COVID-19.*
