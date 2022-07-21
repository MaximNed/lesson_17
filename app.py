from flask import Flask, request, make_response
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
api.app.config['RESTFUL_JSON'] = {
            'ensure_ascii': False
        }


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)

movies_ns = api.namespace('movies')
movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            director_id = request.args.get('director_id')
            genre_id = request.args.get('genre_id')
            if director_id:
                dir_movies = Movie.query.filter(Movie.director_id == director_id).all()
                return movies_schema.dump(dir_movies), 200
            elif genre_id:
                gen_movies = Movie.query.filter(Movie.genre_id == genre_id).all()
                return movies_schema.dump(gen_movies), 200
            else:
                all_movies = Movie.query.all()
                # print(movies_schema.dump(all_movies))
                return movies_schema.dump(all_movies), 200
        except Exception as e:
            return "", 404


@movies_ns.route('/<int:id>')
class MovieView(Resource):
    def get(self, id: int):
        try:
            movie = Movie.query.get(id)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404



if __name__ == '__main__':
    app.run(debug=True)
