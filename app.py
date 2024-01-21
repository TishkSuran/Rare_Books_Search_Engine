from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd
from fuzzywuzzy import fuzz
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rare_books_database.db'  

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
df = pd.read_sql_table('combined_table', con=engine)

def get_random_fun_facts():
    # Your list of fun facts
    fun_facts = [
        "The Gutenberg Bible was the first major book printed using mass-produced movable metal type.",
        "The world's largest book is 'Bhutan: A Visual Odyssey Across the Last Himalayan Kingdom.'",
        "The first novel ever written on a typewriter is 'Tom Sawyer.'",
        "The smell of old books is due to the organic compounds released during paper decomposition.",
        "The Library of Congress is the largest library in the world, with over 170 million items.",
    ]
    # Return a random subset of fun facts (adjust the number based on your preference)
    return random.sample(fun_facts, k=3)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = search_books(query)
        return render_template('index.html', results=results, query=query, fun_facts=get_random_fun_facts())
    else:
        return render_template('index.html', results=None, query=None, fun_facts=get_random_fun_facts())

def search_books(query):
    title_matches = df[df['Book Name'].apply(lambda x: fuzz.token_sort_ratio(query, x) > 65)]
    author_matches = df[df['Book Author'].apply(lambda x: fuzz.token_sort_ratio(query, x) > 65)]

    results = pd.concat([title_matches, author_matches]).drop_duplicates()

    return results.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
