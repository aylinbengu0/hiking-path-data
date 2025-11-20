## A Multi-Modal Machine Learning Approach for Predicting Hiking Route Difficulty Using Geographic and User Generated Data

The study aims to classify hiking paths using an objective approach to handle identified problems. Combining user-generated data from the Wikiloc platform with quantified geographical data obtained from the GPX file sought to create a more consistent approach.




Our methodology consists of three primary components:
1) Data collection and processing consist of GPX files, user-generated interpretation, and image extraction.
2) Data analysis approaches include the Haversine formula, which determines the distance between two points, as well as the computation of elevation change.
3) Development and evaluation of machine learning models to detect trail complexity based on the data obtained. (On going)

This study seeks to improve route selection for hikers of all experience levels using a more consistent framework for assessing hiking trails, therefore strengthening the accuracy of difficulty ratings. This work offers the possibility to enhance usability, safety, and accessibility in hiking apps using a data-driven categorization system. Future uses might be real-time difficulty modifications depending on terrain changes, weather, and even user fitness levels, therefore changing the way hikers engage with digital trail maps.


##  Project Flow: Execution Sequence

The pipeline runs sequentially, ensuring data integrity at each step.

| Sequence | Script Name | Primary Function |
| :--- | :--- | :--- |
| **01** | `01_extract_metadata.py` | Initiates the pipeline by scraping the title, region, locality, and description for new path URLs. |
| **02** | `02_download_gpx.py` | Downloads the raw GPX files from Wikiloc using the URLs collected in the main data file. |
| **03** | `03_convert_gpx_to_excel.py` | Converts the downloaded raw GPX data (KML format) into structured CSV files for calculation. |
| **04** | `04_calc_small_data_metrics.py` | Calculates initial distance and slope metrics specifically for small/test CSV datasets. |
| **05** | `05_calc_initial_metrics.py` | Calculates base metrics like total length, highest, and lowest elevation points for the main dataset. |
| **06** | `06_calc_main_complexity.py` | Performs core calculations including elevation gain/loss, slope, and counting direction changes on the main CSV files. |
| **07** | `07_extract_photos.py` | Uses Selenium to scrape photo count and associated URLs for each hiking path. |
| **08** | `08_extract_comments.py` | Scrapes user comments from each path's URL, performing a crucial check for missing values. |
| **09** | `09_extract_difficulty.py` | Scrapes the "Technical difficulty" rating from the Wikiloc webpage for each path. |

---

## Technical Stack

* **Language:** Python
* **Libraries:** Pandas, NumPy, requests, BeautifulSoup, Selenium (for scraping)


## Future Work & Impact

This project is currently at the stage of **Data Preparation and Feature Engineering**.

Next Steps in Modeling: **Multimodal Comparison**
The final phase will focus on comparing and integrating distinct feature sets to establish the most reliable classification:

Geospatial Features (GPX Data): Metrics from scripts 04, 05, and 06 (Elevation Gain, Slope, Total Length).

User-Generated Features (Scraped Data): Data from scripts 07, 08, and 09 (Photo Count, Comment Sentiment Analysis, and Official Difficulty Rating).

The ultimate goal is to train a model to predict the final trail difficulty by identifying which feature set the objective geographical data or the subjective user data has a greater predictive power.
