import streamlit as st

class Book:
    def __init__(self, title, author, genre, publication_year):
        self.title = "english"
        self.author = "Sabir ali"
        self.genre = "new"
        self.publication_year = 2025
        

    def __str__(self):
        return f"{self.title} by {self.author} ({self.genre}, {self.publication_year})"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                return True
        return False

    def search_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def display_books(self):
        return "\n".join(str(book) for book in self.books)

library = Library()
import streamlit as st


# Streamlit interface
st.title("Library System")

option = st.selectbox("Choose an action", ["Add Book", "Remove Book", "Search Book", "Display Books"])

if option == "Add Book":
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.text_input("Publication Year")
    if st.button("Add"):
        if title and author and genre and year:
            book = Book(title, author, genre, year)
            library.add_book(book)
            st.success("Book added successfully!")
        else:
            st.error("All fields must be filled.")

elif option == "Remove Book":
    title = st.text_input("Title of the book to remove")
    if st.button("Remove"):
        if title and library.remove_book(title):
            st.success("Book removed successfully!")
        else:
            st.error("Book not found.")

elif option == "Search Book":
    title = st.text_input("Title of the book to search")
    if st.button("Search"):
        book = library.search_by_title(title)
        if book:
            st.write(str(book))
        else:
            st.error("Book not found.")

elif option == "Display Books":
    books = library.display_books()
    st.text(books if books else "No books in the library.")
