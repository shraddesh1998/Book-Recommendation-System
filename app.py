from flask import Flask, render_template, request, url_for
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
        data = []
        for i in similar_items:
            title = pt.index[i[0]]
            similarity_score = i[1]
            
            # Get the image URL or fallback to the default image
            image_url = popular_df.loc[popular_df['Book-Title'] == title, 'Image-URL-M']
            image_url = image_url.values[0] if not image_url.empty else url_for('static', filename='Default_Book.jpg')
            
            # Append the data dictionary to the list
            data.append({
                "title": title,
                "similarity_score": similarity_score,
                "image_url": image_url
            })

        return render_template('recommend.html', data=data, user_input=user_input)
    except Exception as e:
        # Handle cases where the book is not found
        return render_template('recommend.html', error="Book not found. Please try another title.", user_input=user_input)

#if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
