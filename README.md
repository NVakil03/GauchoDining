# GauchoDining
Fostering a community in UCSB's dining halls. Our objective was to build a user-friendly dining hall review and recommendation website that allows students to leave ratings on food items and decide where to go based on preferences

Try it out -> https://gaucho-dining.vercel.app/

## Our Data Collection
- Dining Hall Menu API + Line Worksheets 
- we collected over 3000 food item data and about 100 real user review data.

## Recommender System Methodology
1. Organized and cleaned data (dropping duplicates and incomplete rows)
2. Modified the data to have an estimated diversified average rating for each food item
3. Used the calculated rating, tag, and serving location to calculate a cosine similarity matrix with each item
4. Found the top 4 closest recommendations for each item in terms of cosine similarity for our recommendations

## Our project features:
- Live website + secure integrated Google login system
- Menus that updates each meal
- Top 4 recommendations for each food with over 90% accuracy
- Real-time comments and ratings
- Simple and beautiful UI/UX on mobile or desktop
