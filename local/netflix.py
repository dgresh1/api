from importlib.metadata import requires
from flask import Flask, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
psql_password = os.getenv("PSQL_PASSWORD")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + psql_password + '@34.123.88.202:5432/netflix'

db = SQLAlchemy(app)


class Title(db.Model):
    show_id = db.Column(db.String(8),primary_key=True)
    type = db.Column(db.String(10),  nullable=False)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(30), nullable=True)
    cast = db.Column(db.String(300), nullable=True)
    country = db.Column(db.String(300), nullable=False)
    date_added = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    listed_in = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f"{self.title} - {self.description}"
    

@app.route('/')
def index():
    return 'Hello!'

@app.route("/titles")
def get_titles():
    ROWS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)

    titles = Title.query.paginate(page = page, per_page=ROWS_PER_PAGE)
    paginated_titles = (titles.items)

    results = [{
        'title': title.title,
        'type': title.type,
        'director': title.director,
        'release_year': title.release_year,
        'show_id': title.show_id
        } for title in paginated_titles]

    return jsonify({
        'success': True,
        'results': results,
        'count': len(paginated_titles)
    })

@app.route("/titles/findByDirector")
def findByDirector():
    director_name = request.args.get('director', 'Mike Flanagan', type=str)
    titles = Title.query.filter(Title.director.ilike(director_name))
    

    results = [{
        'title': title.title,
        'type': title.type,
        'director': title.director,
        'release_year': title.release_year,
        'show_id': title.show_id
        } for title in titles]

    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })

@app.route("/titles/findByType")
def findByType():
    type_filter = request.args.get('type', 'TV Show', type=str)
    titles = Title.query.filter(Title.type.ilike(type_filter))
    ordered_titles = titles.order_by(Title.title).all()   

    results = [{
        'title': title.title,
        'type': title.type,
        'director': title.director,
        'release_year': title.release_year,
        'show_id': title.show_id
        } for title in ordered_titles]

    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })


@app.route("/titles/<show_id>")
def get_title(show_id):
    title = Title.query.get_or_404(show_id)
    return {"title": title.title, "description": title.description}

@app.route("/titles", methods=['POST'])
def add_title():
    title = Title( show_id = request.json['show_id'],
    type = request.json['type'],
    title = request.json['title'],
    director = request.json['director'],
    cast =  request.json['cast'],
    country = request.json['country'],
    date_added = request.json['date_added'],
    release_year = request.json['release_year'],
    rating = request.json['rating'],
    duration = request.json['duration'],
    listed_in = request.json['listed_in'],    
    description=request.json['description'])

    db.session.add(title)
    db.session.commit()
    return {"show_id": title.show_id}

@app.route("/titles/<show_id>", methods=['DELETE'])
def delete_title(show_id):
    title = Title.query.get_or_404(show_id)
    if title is None:
        return {"error":  "invalid id"}
    db.session.delete(title)
    db.session.commit()
    return {"message": "title deleted"}



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, debug=True)
