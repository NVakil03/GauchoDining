import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
# Load your uploaded file
dlg_food_items = pd.read_csv('dlgfood.csv', na_values=['null'])

# Look at the first few rows
# Set seed for reproducibility
np.random.seed(42)

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
    """
    Returns the top 10 most similar food items based on diversified rating, tag, and serving location.
    
    Parameters:
        food_name (str): Name of the food item to find recommendations for.
    
    Returns:
        pd.DataFrame: Top 10 most similar food items.
    """
    # Check if the food exists
    if food_name not in dlg_food_items['Food Item'].values:
        return f"Food item '{food_name}' not found in the dataset."
    
    # Find the index of the input food
    idx = rec_indices[food_name]
    
    # Compute similarity
    input_vector = feature_matrix[idx].reshape(1, -1)
    similarities = cosine_similarity(input_vector, feature_matrix).flatten()
    
    # Attach similarity to DataFrame
    dlg_food_items['similarity'] = similarities
    
    # Sort by similarity and exclude the input food itself
    recommendations = dlg_food_items[dlg_food_items['Food Item'] != food_name].sort_values(by='similarity', ascending=False).head(10)
    
    # Create output dictionary
    rec_dic = {
        "No": range(1, len(recommendations) + 1),
        "Food Name": recommendations['Food Item'].values,
        "Similarity Score": recommendations['similarity'].round(4).values,
        "Serving Location": recommendations['Serving Location'].values,
        "Tag": recommendations['Tag'].values,
        "Diversified Rating": recommendations['Diversified Rating'].round(2).values
    }
    
    # Create DataFrame
    dataframe = pd.DataFrame(data=rec_dic)
    dataframe.set_index("No", inplace=True)
    
    # Print heading
    print(f"Recommendations for {food_name} lovers:\n")
    
    # Return nicely styled DataFrame
    return dataframe.style.set_properties(**{
        "background-color": "white",
        "color": "black",
        "border": "1.5px solid black"
    })

# seeing the top 10 recommendations for "Hash Browns"
print(give_recommendation("Hash Browns (vgn)"))