from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd
from fuzzywuzzy import fuzz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rare_books_database.db'  

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
df = pd.read_sql_table('combined_table', con=engine)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        results = search_books(query)
        return render_template('index.html', results=results, query=query)
    else:
        return render_template('index.html', results=None, query=None)


def search_books(query):
    print(df.columns) 
    print(df.head())    
    title_matches = df[df['Book Name'].apply(lambda x: fuzz.token_sort_ratio(query, x) > 65)]
    author_matches = df[df['Book Author'].apply(lambda x: fuzz.token_sort_ratio(query, x) > 65)]

    results = pd.concat([title_matches, author_matches]).drop_duplicates()

    return results.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
