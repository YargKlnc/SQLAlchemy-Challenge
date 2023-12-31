# SQLAlchemy-Challenge
UofT Data Analytics SQL Alchemy Challenge by YK

![image](https://github.com/YargKlnc/SQLAlchemy-Challenge/assets/142269763/4d1a6891-79dc-4b6b-bd4c-97269e3164db)

# Background

**"A trip planning project! Decided for a long holiday vacation in Honolulu, Hawaii this work will help to plan the trip with climate and precipitation analysis about the area."**


**Part 1: Climate Data Analysis and Exploration**

Python, SQLAlchemy, ORM queries, Pandas, and Matplotlib has been used for climate analysis and data exploration of climate database.  

* Jupyter Notebook Database Connection 

    •	SQLAlchemy create_engine() function used to connect to SQLite database

    •	SQLAlchemy automap_base() function used to reflect the tables into classes

    •	References saved to the classes named as station and measurement

    •	Python linked to the database by creating a SQLAlchemy session

    •	Session closed at the end of notebook


* Precipitation Analysis 

    •	A query created that finds the most recent date in the dataset (8/23/2017)

    •	A query created that collects only the date and precipitation for the last year of data without passing the date as a variable

    •	The query results are saved to a Pandas DataFrame to create date and precipitation columns 

    •	The DataFrame was sorted by date

    •	The results are plotted by using the DataFrame plot method with date as the x and precipitation as the y variables

    •	Pandas used to print the summary statistics for the precipitation data
  

![image](https://github.com/YargKlnc/SQLAlchemy-Challenge/assets/142269763/42a79348-efe8-4982-bcf6-f3007e714874)



![image](https://github.com/YargKlnc/SQLAlchemy-Challenge/assets/142269763/cd8dfa98-bb40-4f2f-ab03-588c15c71a66)



* Station Analysis 

    •	A query designed that correctly finds the number of stations in the dataset (9) 

    • A query designed that correctly lists the stations and observation counts in descending order and finds the most active station (USC00519281)

    •	A query designed that correctly finds the min, max, and average temperatures for the most active station (USC00519281) 

    •	A query designed to get the previous 12 months of temperature observation (TOBS) data that filters by the station that has the greatest number of observations 

    •	Save the query results to a Pandas DataFrame 

    •	Correctly plot a histogram with bins=12 for the last year of data using tobs as the column to count



![image](https://github.com/YargKlnc/SQLAlchemy-Challenge/assets/142269763/1b2a43c4-3915-4d45-96f8-7398bbbdcf06)



**Part 2: Designing a Climate App Flask API Based on Initial Analysis**


* API SQLite Connection & Landing Page 

    •	Correctly generate the engine to the correct sqlite file 

    •	Use automap_base() and reflect the database schema 

    •	Correctly save references to the tables in the sqlite file (measurement and station) 

    •	Correctly create and binds the session between the python app and database 

    •	Display the available routes on the landing page 



* API Static Routes

    A precipitation route that:

    •	Returns json with the date as the key and the value as the precipitation 

    •	Only returns the jsonified precipitation data for the last year in the database 


    A stations route that:

    •	Returns jsonified data of all of the stations in the database 


    A tobs route that:

    •	Returns jsonified data for the most active station (USC00519281) 

    •	Only returns the jsonified data for the last year of data 



* API Dynamic Route 

    A start route that:
  
    •	Accepts the start date as a parameter from the URL
  
    •	Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
  

    A start/end route that:
  
    •	Accepts the start and end dates as parameters from the URL
   
    •	Returns the min, max, and average temperatures calculated from the given start date to the given end date

# References
SQL Alchemy photo taken from and all rights belongs to hackersandslackers.com
https://hackersandslackers.com/database-queries-sqlalchemy-orm/

