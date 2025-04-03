from flask import Blueprint,request,jsonify
from sqlalchemy.orm import query
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
import validators
from app.models.author_model import Author
from app.models.book_model import Book
from app.models.company_model import Company
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity

#books blueprint
books= Blueprint('books', __name__,url_prefix='/api/v1/books')

#creating a book
@books.route('/create',methods=['POST'])
@jwt_required()
def createBook():

    #storing request data
    data = request.get_json()
    title = data.get('title')
    pages = data.get('pages')
    genre = data.get('genre')
    price = data.get('price')
    price_unit = data.get('price_unit')
    isbn = data.get('isbn')
    description = data.get('description')
    image = data.get('image')
    publication_date = data.get('publication_date')
    company_id = data.get('company_id')
    author_id = get_jwt_identity()


    #validations of the incoming request data
    if not title or not pages or not description or not price or not publication_date or not isbn or not price_unit or not not genre or not company_id:
        return jsonify({'error':'All fields are required'}),HTTP_400_BAD_REQUEST

    if Book.query.filter_by(title=title).first() is not None:
        return jsonify({'error':'Book with this title and authorID already exists'}),HTTP_400_BAD_REQUEST
    
    if Book.query.filter_by(isbn=isbn).first() is not None:
        return jsonify({'error':'Book isbn already in use'}),HTTP_400_BAD_REQUEST
    
    try:

       #creating a new book
        new_book = Book(title,description=description,pages=pages,genre=genre,price=price,price_unit=price_unit,
                        publication_date=publication_date,company_id=company_id,author_id=author_id,isbn=isbn,image=image)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({
            'message': title + ' has been created successfully as an ',
            'book':{
                 'title':new_book.title,
                 'pages':new_book.pages,
                 'price':new_book.price,
                 'price_unit':new_book.price_unit,
                 'publication_date':new_book.publication_date,
                 'description':new_book.description,
                 'image':new_book.image,
                 'genre':new_book.genre,
                 'isbn':new_book.isbn,
                 'created_at':new_book.created_at,
                 'updated_at':new_book.updated_at,

                 'company':{
                     'id':new_book.company.id,
                     'name':new_book.company.first_name,
                     'origin':new_book.company.origin,
                     'description':new_book.company.description,
                     'created_at':new_book.created_at
                 },
                 'author':{
                          'first_name':new_book.author.first_name,
                          'last_name':new_book.author.last_name,
                           'username':new_book.author.get_full_name(),
                           'email':new_book.author.email,
                           'contact':new_book.author.contact,
                           'type':new_book.author.author_type,
                           'biography':new_book.author.biography,
                           'created_at':new_book.author.created_at,
                 }
  
            }
            }),HTTP_201_CREATED 

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

  #Getting all books 
@books.get('/')
@jwt_required()
def getAllBooks():
    
    try:

        all_books = Book.query.all()

        books_data = []

        for book in all_books:
            book_info = {
                 'title':book.title,
                 'pages':book.pages,
                 'price':book.price,
                 'price_unit':book.price_unit,
                 'publication_date':book.publication_date,
                 'description':book.description,
                 'image':book.image,
                 'genre':book.genre,
                 'isbn':book.isbn,
                 'created_at':book.created_at,
                 'company':{
                     'id':book.company.id,
                     'name':book.company.first_name,
                     'origin':book.company.origin,
                     'description':book.company.description,
                     'created_at':book.created_at
                    },
                }

        return jsonify({
            "message":"All books retrieved successfully",
            "total_books": len(books_data),
            "books": books_data

            

        }),HTTP_200_OK
             

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    

   #Get book by id
@books.get('/book/<int:id>')
@jwt_required()
def getBook(id):

    try:

        book = Book.query.filter_by(id=id).first()
        
        if not book:
            return jsonify({"error":"Book not found"}),HTTP_404_NOT_FOUND

        return jsonify({
            "message":"Book details retrieved successfully",
        
            "Book":{
               'title':book.title,
                 'pages':book.pages,
                 'price':book.price,
                 'price_unit':book.price_unit,
                 'publication_date':book.publication_date,
                 'description':book.description,
                 'image':book.image,
                 'genre':book.genre,
                 'isbn':book.isbn,
                 'created_at':book.created_at,
                 'company':{
                     'id':book.company.id,
                     'name':book.company.first_name,
                     'origin':book.company.origin,
                     'description':book.company.description,
                     'created_at':book.created_at
                 },
                 'author':{
                          'first_name':book.author.first_name,
                          'last_name':book.author.last_name,
                           'authorname':book.author.get_full_name(),
                           'email':book.author.email,
                           'contact':book.author.contact,
                           'type':book.author.author_type,
                           'biography':book.author.biography,
                           'created_at':book.author.created_at,
                 }
  
            }
            }),HTTP_201_CREATED 
             
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    

    #update book details
@books.route('/edit/<int:id>',methods=['PUT','PATCH'])
@jwt_required()
def updateBookDetails(id):

    try:

        current_author= get_jwt_identity()
        loggedInauthor= Author.query.filter_by(id=current_author).first()
         
         #get book by id
        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({"error":"Book not found"}),HTTP_404_NOT_FOUND
        
        elif loggedInauthor.author_type!='admin' and book.author_id!=current_author:
            return jsonify({'error':'You are not authorised to update the book details'}),HTTP_403_FORBIDDEN
        
        else:
             #Store request data
             title = request.get_json().get('title',book.tile)
             pages = request.get_json().get('pages',book.pages)
             price = request.get_json().get('price',book.price)
             publication_date = request.get_json().get('publication_date',book.publication_date)
             price_unit = request.get_json().get('price_unit',book.price_unit)
             description = request.get_json().get('description',book.description)
             genre = request.get_json().get('genre',book.genre)
             isbn = request.get_json().get('isbn',book.isbn)
             image = request.get_json().get('image',book.image)
             company_id = request.get_json().get('company_id',book.company_id)


             if isbn!= book.isbn and Book.query.filter_by(isbn=isbn).first():
                  return jsonify({
                      'error':'ISBN already in use'
                  }),HTTP_409_CONFLICT
             
             if title!= book.isbn and Book.query.filter_by(title=title,author_id=current_author).first():
                  return jsonify({
                      'error':'Title already in use'
                  }),HTTP_409_CONFLICT


             book.title = title
             book.pages = pages
             book.price = price
             book.price_unit = price_unit
             book.image = image
             book.isbn = isbn
             book.genre = genre
             book.publication_date = publication_date
             book.company_id = company_id
             book.description = description
             
             db.session.commit()
             
             return jsonify({
                'message':title + " 's details have been successfully updated",
                "book":{
                     'title':book.title,
                 'pages':book.pages,
                 'price':book.price,
                 'price_unit':book.price_unit,
                 'publication_date':book.publication_date,
                 'description':book.description,
                 'image':book.image,
                 'genre':book.genre,
                 'isbn':book.isbn,
                 'created_at':book.created_at,
                 'company':{
                     'id':book.company.id,
                     'name':book.company.first_name,
                     'origin':book.company.origin,
                     'description':book.company.description,
                     'created_at':book.created_at
                 },
                 'author':{
                          'first_name':book.author.first_name,
                          'last_name':book.author.last_name,
                           'authorname':book.author.get_full_name(),
                           'email':book.author.email,
                           'contact':book.author.contact,
                           'type':book.author.author_type,
                           'biography':book.author.biography,
                           'created_at':book.author.created_at,
                 }
  
                 }
             })

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
    
       #Deleting a book
@books.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deleteBook(id):

    try:
        current_author= get_jwt_identity()
        loggedInauthor= Author.query.filter_by(id=current_author).first()
         
         #get book by id
        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({"error":"Book not found"}),HTTP_404_NOT_FOUND
        
        elif loggedInauthor.author_type!='admin' and book.author_id!=current_author: 
            return jsonify({'error':'You are not authorised to delete the book details'}),HTTP_403_FORBIDDEN
        
        else:

            db.session.delete(book)
            db.session.commit()


            return jsonify({'message':'Book has been deleted successfully'})
            

    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
    
    
    
    