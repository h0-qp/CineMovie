from flask import Flask, render_template, request,url_for,redirect
import requests,os,json

#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__, template_folder=os.path.dirname(__file__))

try:
	open("file.json", "r").read()
except:
	with open("file.json", "a") as json_file:
		json.dump({},json_file)

def check(movie):
	with open("file.json", "r") as json_file:
		old_data = json.load(json_file)
	if not movie["id"] in old_data:
		add(movie)

def add(movie):
	with open("file.json", "r") as json_file:
		old_data = json.load(json_file)
	
	id = movie["id"]
	title = movie["title"]
	likes = 0
	dislikes = 0
	
	movie = {
		f"{id}": {
			"title": title,
			"likes": likes,
			"dislikes": dislikes
		}
	}
	old_data.update(movie)
	with open("file.json", "w") as json_file:
		json.dump(old_data, json_file)
		return True

def LikesAndDislikes(movie):
	check(movie)
	with open("file.json", "r") as json_file:
		data = json.load(json_file)
	
	info = data[f"{movie['id']}"]
	likes = info["likes"]
	dislikes = info["dislikes"]
	
	return {"likes": likes,"dislikes": dislikes}

def AddLike(movie):
	info = LikesAndDislikes(movie)
	likes = info["likes"]
	dislikes = info["dislikes"]
	
	likes += 1
	movie = {
		str(movie["id"]): {
			"title": movie["title"],
			"likes": likes,
			"dislikes": dislikes
		}
	}
	
	with open("file.json", "r") as json_file:
		data = json.load(json_file)
	
	data.update(movie)
	with open("file.json", "w") as json_file:
		json.dump(data, json_file)
		return True


#AddLike(
#	{"id":"idid83",
#	"title": "hello"}
#)

#print(LikesAndDislikes(
#	{"id":"idid83",
#	"title": "hello"}
#)
#)

@app.route('/')
def index():
    api_key = "ab7f99f1c91419ddefcfa19a67fe2964"
    popular_movies_url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
    response = requests.get(popular_movies_url)
    popular_movies = response.json().get('results', [])
    return render_template('index.html', popular_movies=popular_movies)

@app.route('/search', methods=['POST'])
def search():
    api_key = "ab7f99f1c91419ddefcfa19a67fe2964"
    query = request.form.get('query')
    if query:
        url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
        response = requests.get(url)
        movies = response.json().get('results', [])
        #print(movies[0]["poster_path"])
        return render_template("index.html", movies=movies,query=query)

    return render_template("index.html")


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
	api_key = "ab7f99f1c91419ddefcfa19a67fe2964"
	url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=videos,images'
	response = requests.get(url)
	movie = response.json()
	gen = movie["genres"]
	try:
		trailer = movie["videos"]["results"][0]["key"]
		trailer = "https://www.youtube.com/watch?v="+trailer
	except:
		trailer = None
	genres = ""
	for genre in gen:
		genres += genre["name"]+", "
	url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={api_key}'
	response = requests.get(url)
	similar = response.json()["results"]
	return render_template('movie_detail.html', movie=movie,genres=genres,trailer=trailer,similar=similar)
#@app.route('/like_movie/<int:movie_id>', methods=['POST'])
#def like_movie(movie_id):
#    movie = Movie.query.get_or_404(movie_id)
#    movie.likes += 1
#    db.session.commit()
#    return redirect(url_for('movie_detail', movie_id=movie_id))
#    
#@app.route('/dislike_movie/<int:movie_id>', methods=['POST'])
#def dislike_movie(movie_id):
#	movie = Movie.query.get_or_404(movie_id)
#	movie.dislikes += 1
#	db.session.commit()
#	return redirect(url_for('movie_detail', movie_id=movie_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
