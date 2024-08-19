from flask import Flask, render_template, request

import pickle
import numpy as np

popular_df = pickle.load(open('C:\\Users\\HP\\Desktop\\Python projects\\Book Recommendation System\\popular.pkl','rb'))
similarity_score = pickle.load(open('C:\\Users\\HP\\Desktop\\Python projects\\Book Recommendation System\\similarity_score.pkl','rb'))
books = pickle.load(open('C:\\Users\\HP\\Desktop\\Python projects\\Book Recommendation System\\books.pkl','rb'))
pt = pickle.load(open('C:\\Users\\HP\\Desktop\\Python projects\\Book Recommendation System\\pt.pkl','rb'))

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
                           book_name = list(popular_df['Book-Title'].values),
                           book_author = list(popular_df['Book-Author'].values),
                           book_publication = list(popular_df['Year-Of-Publication'].values),
                           book_img = list(popular_df['Image-URL-M'].values),
                           book_votes = list(popular_df['Number_of_Rating'].values ),
                           book_rating = list(popular_df['Average_Rating'].values.round(2))
                        #    rounded_numbers = [round(num) for num in book_rating]
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',
                           
                           )

@app.route('/recommend_books', methods=["post"])
def recommend():
    user_input = request.form.get('user_input')
    index_of_book = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index_of_book])), key=lambda x:x[1], reverse=True)[1:6]
    
    data=[]
    for i in similar_items:
        item=[]
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)

if __name__ =='__main__':
    app.run(debug=True)