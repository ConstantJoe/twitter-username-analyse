from flask import Flask, render_template, url_for
app = Flask(__name__, static_url_path='/static')

#url_for('static', filename='blog.css')

@app.route('/')
def index():
    return 'Index Page'

#@app.route('/hello')
#def hello_world():
#    return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<username>')
def hello_name(username=None):
    return render_template('hello.html', name=username)

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/projects/twitter/')
def twitter():
    return render_template('twitter_usernames.html')

if __name__ == '__main__':
    app.run(debug=True)

