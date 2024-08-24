from flask import Flask, request, jsonify

app = Flask(__name__)


books = [
    {
        "id": 0,
        "title": "Things fall apart",
        "author": "Chinua Achebe",
    },
    {
        "id": 1,
        "title": "Things didn't fall apart",
        "author": "Achebe Chinua",
    },
    {
        "id": 2,
        "title": "Last days at Forcados high school",
        "author": "Jerry Lincoln",
    }
]


@app.route("/books", methods=["GET", "POST"])
def book_function():
    if request.method == "GET":
        if len(books) > 0:
            return jsonify({
                "responseCode": "00",
                "responseMessage": "Books retrieved successfully",
                "bookData": books
            }), 201
        else:
            return jsonify({
                "responseCode": "01",
                "responseMessage": "No available books",
                "boolData": []
            }), 404
    elif request.method == "POST":
        request_obj = {}
        if request.is_json:
            request_obj = request.get_json()
        elif len(request.form) > 0:
            request_obj = request.form
        if len(request_obj) == 0:
            return jsonify({
                "error": True,
                "desc": "request data is empty",
            }), 400
        if len(books) > 0:
            id_ = books[-1]["id"] + 1
            title = request_obj["title"]
            author = request_obj['author']

            book = {
                "id": id_,
                "title": title,
                "author": author,
            }

            books.append(book)

            return jsonify({
                "responseCode": "00",
                "responseMessage": "Book successfully added",
                "bookData": books
            }), 201
        else:
            id_ = 0
            title = request.form["title"]
            author = request.form['author']

            book = {
                "id": id_,
                "title": title,
                "author": author,
            }

            books.append(book)

            return jsonify({
                "responseCode": "00",
                "responseMessage": "Book successfully added",
                "bookData": books
            }), 201


@app.route('/books/<int:book_id>', methods=["GET", "PUT", "DELETE"])
def update_books(book_id):
    if request.method == "GET":
        for book in books:
            if book["id"] == book_id:
                return jsonify({
                    "responseCode": "00",
                    "responseMessage": "Book retrieved successfully",
                    "bookData": book,
                }), 201
        return jsonify({
            "error": True,
            "desc": "Book with the id {} not found".format(book_id),
        }), 402
    elif request.method == "PUT":
        for book in books:
            if book["id"] == book_id:
                request_obj = {}
                if request.is_json:
                    request_obj = request.get_json()
                elif len(request.form) > 0:
                    request_obj = request.form
                if len(request_obj) == 0:
                    return jsonify({
                        "error": True,
                        "desc": "request data is empty",
                    }), 400
                title = request_obj["title"]
                author = request_obj['author']
                book["title"] = title
                book['author'] = author

                return jsonify({
                    "responseCode": "00",
                    "responseMessage": "Book successfully updated",
                    "bookData": books
                }), 201
        else:
            return jsonify({
                "error": True,
                "desc": "Book with the id {} not found".format(book_id),
            }), 402
    elif request.method == "DELETE":
        for i in range(len(books)):
            if books[i]["id"] == book_id:
                # del books[i]
                books.pop(i)
                return jsonify({
                    "responseCode": "00",
                    "responseMessage": "Book successfully deleted",
                    "bookData": books
                }), 201
        else:
            return jsonify({
                "error": True,
                "desc": "Book with the id {} not found".format(book_id),
            }), 402


if __name__ == "__main__":
    app.run(debug=True)

