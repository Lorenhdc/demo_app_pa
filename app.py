#from socket import J1939_PGN_ADDRESS_COMMANDED
from flask import Flask, jsonify, request
from datos_dummy import books

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
@app.route('/api/v0/resources/books/all', methods=['GET'])
def get_all():
    return jsonify(books) # Para que te lo jsonifique

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/api/v0/resources/book', methods=['GET'])
def book_id():
    results = []
    if 'id' in request.args:
        id = int(request.args['id'])
        for book in books:
            if book['id']==id:
                results.append(book)
        if results == []:
            return "Book not found with the id requested"
        else:
            return jsonify(results)
    else:
        return "No id field provided"

# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
@app.route('/api/v0/resources/book/<string:title>', methods=['GET'])
def book_request(title):
    results = []
    for book in books:
        if book['tittle']==title:
            results.append(book)
    if results != []:
        return jsonify(results)
    else:
        return "Book title not found"


# 4.Ruta para obtener un libro concreto mediante su título dentro del cuerpo de la llamada
@app.route('/api/v1/resources/book/', methods=['GET'])
def book_tittle():
    results = []
    title = request.get_json()['title']
    for book in books:
        if book['tittle']==title:
            results.append(book)
    if results != []:
        return jsonify(results)
    else:
        return "Book title not found"

# 5.Ruta para añadir un libro mediante parámetros en la llamada
@app.route('/api/v1/resources/book/add', methods=['POST'])
def post_book():
    data = request.get_json()
    books.append(data)
    return jsonify(books)


# 6.Ruta para añadir un libro de otra forma 1
@app.route('/api/v1/resources/book/addbyparemeters', methods=['POST'])
def add_book():
    data = {}
    data['id'] = request.args['id']
    data['title'] = request.args['title']
    data['author'] = request.args['author']
    data['first_sentence'] = request.args['first_sentence']
    data['published'] = request.args['published']
    books.append(data)
    return jsonify(books)

# 7.Ruta para modificar un libro
@app.route('/api/v1/resources/book/update', methods=['PUT'])
def update_book():
    year = request.args['published']
    title = request.args['title']
    for book in books:
        if book['title'] == title:
            book['published'] = year
    return jsonify(books)

# 8.Ruta para eliminar un libro
@app.route('/api/v1/resources/book/delete', methods=['DELETE'])
def delete_book():
    title = request.args['title']
    i = 0
    for book in books:
        if book['title'] == title:
            books.pop(i)
        i +=1  
    return jsonify(books)


app.run()