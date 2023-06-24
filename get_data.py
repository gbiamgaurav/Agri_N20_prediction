import os
import pymongo
import pandas as pd

# Define the path to the "data" folder
data_folder_path = os.path.join(os.getcwd(), "notebook", "data")

# Create the "data" folder if it doesn't exist
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

MONGO_DB_URL = "mongodb+srv://cloud-gaurav:Kabali1234@cluster0.5scda40.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_DB_URL)

# Database connection
db = client["collab-projects"]
collection = db["agri-data"]

all_records = collection.find()

# Iterate over all records
for row in all_records:
    print(row)

all_records = collection.find()

list_cursor = list(all_records)

# Read as a DataFrame
df = pd.DataFrame(list_cursor)

df.drop(columns="_id", axis=1, inplace=True)

# Define the path to the CSV file
csv_file_path = os.path.join(data_folder_path, "dataset.csv")

# Export as a CSV file in the "data" folder
df.to_csv(csv_file_path, index=False)

# Print the shape of the data
print("Data shape:", df.shape)
print("Data exported successfully")
