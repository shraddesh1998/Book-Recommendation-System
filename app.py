from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

# Home Page to display popular books
@app.route('/')
def index():
    # Prepare popular books data
    books_data = zip(
        popular_df['Book-Title'].values,
        popular_df['Book-Author'].values,
        popular_df['Image-URL-M'].values,
        popular_df['num_ratings'].values,
        popular_df['avg_rating'].values
    )
    return render_template('index.html', books_data=books_data)

# Recommendation Page UI
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

# Recommendation Logic
@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    try:
        # Find the book in the pivot table index
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:5]

        # Gather recommendation data
        data = [
            {
                "title": pt.index[i[0]],
                "similarity_score": i[1],
                 "image_url": popular_df.loc[popular_df['Book-Title'] == pt.index[i[0]], 'Image-URL-M']
    .values[0] if not popular_df.loc[popular_df['Book-Title'] == pt.index[i[0]], 'Image-URL-M'].empty else 'default_image_url_or_placeholder.jpg'

            }
            for i in similar_items
        ]

        return render_template('recommend.html', data=data, user_input=user_input)
    except Exception as e:
        # Handle cases where the book is not found
        return render_template('recommend.html', error="Book not found. Please try another title.", user_input=user_input)

#if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))

