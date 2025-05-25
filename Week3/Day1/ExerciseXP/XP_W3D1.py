# Ex.1
#  What is Data Analysis?
# Data analysis is the process of collecting, organizing, and examining data to find useful information. It helps people understand what the numbers mean and make better decisions.

# Why is Data Analysis Important Today?
# In today’s world, we create a lot of data every second — from phones, computers, businesses, and sensors. Data analysis helps companies, governments, and individuals turn this raw data into smart actions. It can save time, reduce costs, and lead to better results.

# Three Areas Where Data Analysis Is Used:

# Business:
# Companies use data analysis to understand customer behavior, improve products, and increase profits. For example, online stores like Amazon suggest products based on what customers searched for or bought before.

# Healthcare:
# Doctors and researchers use data to track diseases, improve treatments, and make predictions. For example, during the COVID-19 pandemic, data analysis helped predict virus spread and plan hospital resources.

# Genealogy:
# People researching family history use data analysis to find patterns in records such as birth certificates, immigration documents, and old photos. It helps build family trees, trace ancestors, and discover cultural roots more accurately and efficiently.

# Ex.2
import pandas as pd

df = pd.read_csv(r'C:\DI-Bootcamp\Week3\Day1\ExerciseXP\clean_dataset.csv')
print(df.head())

#print(df.info())

data = {
    'Book Title': ['The Great Gatsby', 'To Kill a Mockingbird', '1984', 'Pride and Prejudice', 'The Catcher in the Rye'],
    'Author': ['F. Scott Fitzgerald', 'Harper Lee', 'George Orwell', 'Jane Austen', 'J.D. Salinger'],
    'Genre': ['Classic', 'Classic', 'Dystopian', 'Classic', 'Classic'],
    'Price': [10.99, 8.99, 7.99, 11.99, 9.99],
    'Copies Sold': [500, 600, 800, 300, 450]
}

