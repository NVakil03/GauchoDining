import os
from supabase import create_client, Client
# do pip install supabase
url: str = "https://wyqtpooggygivdqfrrpk.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5cXRwb29nZ3lnaXZkcWZycnBrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMjE2OTksImV4cCI6MjA2MDU5NzY5OX0.1bdEUFYA6PNiWoCT8GEJZooux8Pwf-G9pmKpU--RLiE"
supabase: Client = create_client(url, key)

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
print("Success!")

food_name = "Hash Brown"
rec1 = "Shoestring French Fries"
rec1_loc = "West Side (Cafe)"

rec2 = "Cream Of Wheat"
rec2_loc = "West Side (Cafe)"

rec3 = "Grilled Mozzarella & Basil on Sourdough"
rec3_loc = "West Side (Cafe)"

rec4 = "Chicken Sausage Patty"
rec4_loc = "West Side (Cafe)"
    


#submitFood(food_name, rec1, rec1_loc, rec2, rec2_loc, rec3, rec3_loc, rec4, rec4_loc)
print("Success!")

def output(response):
    print("Recommendations for " + response.food_name + " Lovers!")
def getRecsfor(food_name):
    response = (
    supabase.table("recommenders")
    .select('*')
    .eq('food_name', food_name)
    .execute())
    if not (response):
        return "No Recommendations";
    else:
        return response.data

    
print(getRecsfor(food_name))