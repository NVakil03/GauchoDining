import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import os
from supabase import create_client, Client

# do pip install supabase !!
url: str = "https://wyqtpooggygivdqfrrpk.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5cXRwb29nZ3lnaXZkcWZycnBrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMjE2OTksImV4cCI6MjA2MDU5NzY5OX0.1bdEUFYA6PNiWoCT8GEJZooux8Pwf-G9pmKpU--RLiE"
supabase: Client = create_client(url, key)


# Load your uploaded file
dlg_food_items = pd.read_csv('dlgfood.csv', na_values=['null'])

# Look at the first few rows

# Set seed for reproducibility
np.random.seed(42)

#dis is a function that takes in the original food, and spits out 4 recs and their locations.
def submitFood(food_name, rec1, rec1_loc, rec2, rec2_loc, rec3, rec3_loc, rec4, rec4_loc):
	response = (
    supabase.table("recommenders")
    .insert({"food_name": food_name,
             "rec1": rec1, "rec1_loc": rec1_loc,
             "rec2": rec2, "rec2_loc": rec2_loc,
             "rec3": rec3, "rec3_loc": rec3_loc,
             "rec4": rec4, "rec4_loc": rec4_loc,
             })
    .execute()
	)
 
# Define a simple heuristic-based tagging system
def tag_item(item):
    item = item.lower()
    if any(word in item for word in ["cake", "pie", "cobbler", "cookie", "brownie", "bar", "bun", "muffin", "scone"]):
        return "dessert"
    elif any(word in item for word in ["pizza", "burger", "burrito", "taco", "wrap", "sub", "sandwich", "quesadilla", "enchilada"]):
        return "main_fast"
    elif any(word in item for word in ["stir fry", "pasta", "ravioli", "lasagna", "penne"]):
        return "main_entree"
    elif any(word in item for word in ["soup", "chowder", "stew"]):
        return "soup"
    elif any(word in item for word in ["rice", "potato", "beans", "vegetable", "corn", "salad", "spinach", "greens"]):
        return "side"
    elif any(word in item for word in ["oatmeal", "pancake", "waffle", "biscuit", "toast", "cereal", "french toast"]):
        return "breakfast"
    elif any(word in item for word in ["sauce", "salsa", "relish", "bread", "roll", "naan", "tortilla"]):
        return "condiment_or_bread"
    else:
        return "other"

# Rating estimator
def estimate_rating(tag):
    ratings = {
        "dessert": 4.6,
        "main_fast": 4.3,
        "main_entree": 4.4,
        "soup": 4.2,
        "side": 4.0,
        "breakfast": 4.3,
        "condiment_or_bread": 3.9,
        "other": 4.1
    }
    return ratings.get(tag, 4.1)

# Diversified rating generator
tag_std_dev = {
    "dessert": 0.8,
    "main_fast": 1,
    "main_entree": 0.8,
    "soup": 0.8,
    "side": 1,
    "breakfast": 0.8,
    "condiment_or_bread": 1.2,
    "other": 0.8
}

def diversified_rating(row):
    mean = estimate_rating(row["Tag"])
    std_dev = tag_std_dev.get(row["Tag"], 0.2)
    rating = np.random.normal(loc=mean, scale=std_dev)
    return max(1.0, min(5.0, round(rating, 2)))

# Apply tagging and generate ratings
dlg_food_items["Tag"] = dlg_food_items["Food Item"].apply(tag_item)
dlg_food_items["Diversified Rating"] = dlg_food_items.apply(diversified_rating, axis=1)

# Look at the first few rows

# Step 1: One-hot encode 'Tag' and 'Serving Location'
encoder = OneHotEncoder(sparse_output=False)

tag_encoded = encoder.fit_transform(dlg_food_items[['Tag']])
location_encoded = encoder.fit_transform(dlg_food_items[['Serving Location']])

# Step 2: Combine features
rating_array = dlg_food_items[['Diversified Rating']].values
feature_matrix = np.hstack([rating_array, tag_encoded, location_encoded])

# Step 3: Create reverse index mapping
rec_indices = pd.Series(dlg_food_items.index, index=dlg_food_items['Food Item']).drop_duplicates()

# Step 4: Define the recommendation function
def give_recommendation(food_name):
    food_name = food_name.strip()  # remove leading/trailing spaces

    # Check if the food exists
    if food_name not in dlg_food_items['Food Item'].values:
        print(f"Food item '{food_name}' not found in the dataset.")
        return None
    
    idx = rec_indices[food_name]
    input_vector = feature_matrix[idx].reshape(1, -1)  # Reshaping the input vector for similarity
    similarities = cosine_similarity(input_vector, feature_matrix).flatten()

    dlg_food_items['similarity'] = similarities
    recommendations = dlg_food_items[dlg_food_items['Food Item'] != food_name].sort_values(by='similarity', ascending=False).head(4)

    # If fewer than 4 recommendations exist, fill with "None"
    recs = recommendations[['Food Item', 'Serving Location']].values.tolist()
    while len(recs) < 4:
        recs.append(["None", "None"])

    # Unpack the list nicely
    rec1, rec1_loc = recs[0]
    rec2, rec2_loc = recs[1]
    rec3, rec3_loc = recs[2]
    rec4, rec4_loc = recs[3]

    print(f"\nTop 4 recommendations for {food_name} ready to submit!\n")
    return food_name, rec1, rec1_loc, rec2, rec2_loc, rec3, rec3_loc, rec4, rec4_loc

# Seeing the top 10 recommendations for "Hash Browns"


# Function to handle each food item and submit recommendations
def process_food_items():
    for index, row in dlg_food_items.iterrows():
        food_name = row['Food Item']
        # Call the recommendation function for each food item
        recommendations = give_recommendation(food_name)

        if recommendations:
            # Unpack the results and submit them to the database
            submitFood(*recommendations)

# Call the function to process all food items
process_food_items()
