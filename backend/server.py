import json
from flask import Flask
from flask import request, make_response, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dell5559'
app.config['MYSQL_DB'] = 'library_managements'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#Librarian
@app.route('/add-category',methods=["POST"])
def addCategory():
    cat_name=request.json["cat_name"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO category(cat_name) VALUES (%s) """, [cat_name])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")
    
@app.route('/add-publisher',methods=["POST"])
def addPublisher():
    pub_name = request.json["pub_name"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO publisher(pub_name) VALUES (%s) """, [pub_name])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")

@app.route('/add-author',methods=["POST"])
def addAuthor():
    auth_name = request.json["auth_name"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO Author(auth_name) VALUES (%s) """, [auth_name])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")

@app.route('/add-book',methods=["POST"])
def addBook():
    b_name = request.json["b_name"]
    publisher_id = request.json["pub_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO book(b_name,pub_id) VALUES (%s,%s) """, [b_name,pub_id])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")

@app.route('/add-author-to-book/<int:b_id>',methods=["POST"])
def addAuthorToBook(b_id):
    auth_id = request.json["auth_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO authbook(b_id,auth_id) VALUES (%s,%s) """, [b_id,auth_id])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")
    
@app.route('/add-category-to-book/<int:b_id>',methods=["POST"])
def addCategoryToBook(b_id):
    category_id = request.json["cat_id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO bookcategory(b_id,cat_id) VALUES (%s,%s) """, [b_id,cat_id])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Added Successfully")

@app.route('/getBooks')
def getBooks():
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from book order by b_id desc""")
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/getPublisher')
def getPublisher():
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from publisher order by pub_name""")
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/getCategory')
def getCategory():
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from category order by cat_name asc""")
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/getAuthor')
def getAuthor():
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from author order by auth_name asc""")
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book-authors/<int:b_id>')
def getBookAuthors(b_id):
    cursor = mysql.connection.cursor()
    cursor.execute(""" select auth_name,b_id,auth_id from authbook natural join Author where b_id =(%s)""",[b_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book-categories/<int:b_id>')
def getBookCategories(b_id):
    cursor = mysql.connection.cursor()
    cursor.execute(""" select cat_name,b_id,authbook_id from bookcategory natural join category where b_id =(%s)""",[b_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book/<int:b_id>')
def getBook(b_id):
    cursor = mysql.connection.cursor()
    cursor.execute(""" select b_name,b_id,pub_name from book join publisher on book.pub_id = publisher.pub_id where b_id =(%s)""",[b_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/delete-author-book/<int:authbook_id>',methods=["DELETE"])
def deleteAuthorBook(authbook_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""delete from authbook where authbook_id =(%s)""",[authbook_id])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Delete Successfully")

@app.route('/delete-category-book/<int:bookcategory_id>',methods=["DELETE"])
def deleteCategoryBook(bookcategory_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""delete from bookcategory where  bookcategory_id =(%s)""",[bookcategory_id])
    mysql.connection.commit()
    cursor.close()
    return json.dumps("Delete Successfully")

#Students
@app.route('/get-book-by-name/<b_name>')
def getBookByName(b_name):  
    print(b_name)
    cursor = mysql.connection.cursor()
    book_name1 = str(b_name)
    search_string= f"%{b_name}%"
    cursor.execute(""" select * from book where b_name like (%s) """,[search_string])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book-by-category/<int:cat_id>')
def getBookByCategories(cat_id): 
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from book a natural join bookcategory where cat_id = (%s) """,[cat_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book-by-author/<int:auth_id>')
def getBookByAuthor(auth_id): 
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from book a natural join authbook where auth_id =(%s) """,[auth_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)

@app.route('/get-book-by-publisher/<int:pub_id>')
def getBookByPublisher(pub_id):  
    cursor = mysql.connection.cursor()
    cursor.execute(""" select * from book where pub_id =(%s) """,[pub_id])
    result = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return json.dumps(result)


if __name__ == "__main__":
    app.run(debug = True)
