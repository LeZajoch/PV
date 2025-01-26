from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


# Model pro blogový příspěvek
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())


# Inicializace databáze
with app.app_context():
    db.create_all()


# Vytvoření nového blog postu
@app.route('/api/blog', methods=['POST'])
def create_blog():
    data = request.get_json()
    if not data or 'content' not in data or 'author' not in data:
        abort(400, 'Content and author required')

    new_post = BlogPost(content=data['content'], author=data['author'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'id': new_post.id}), 201


# Zobrazení všech blog postů
@app.route('/api/blog', methods=['GET'])
def get_all_blogs():
    posts = BlogPost.query.all()
    return jsonify(
        [{'id': post.id, 'content': post.content, 'author': post.author, 'created_at': post.created_at} for post in
         posts])


# Zobrazení blog postu podle ID
@app.route('/api/blog/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    return jsonify({'id': post.id, 'content': post.content, 'author': post.author, 'created_at': post.created_at})


# Smazání blog postu podle ID
@app.route('/api/blog/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204


# Částečná aktualizace blog postu
@app.route('/api/blog/<int:blog_id>', methods=['PATCH'])
def update_blog(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    data = request.get_json()

    if 'content' in data:
        post.content = data['content']
    if 'author' in data:
        post.author = data['author']

    db.session.commit()
    return jsonify({'id': post.id, 'content': post.content, 'author': post.author, 'created_at': post.created_at})


if __name__ == '__main__':
    app.run(debug=True)
