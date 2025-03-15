import streamlit as st
import pandas as pd
import json

import tkinter as  tk
from tkinter import messagebox
class Book:
    def __init__(self, title, author, genre, publication_year):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = publication_year

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

class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library System")

        # Labels and Entry widgets
        tk.Label(root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(root, text="Genre").grid(row=2, column=0)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(root, text="Year").grid(row=3, column=0)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(root, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Remove Book", command=self.remove_book).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Search Book", command=self.search_book).grid(row=6, column=0, columnspan=2)
        tk.Button(root, text="Display Books", command=self.display_books).grid(row=7, column=0, columnspan=2)

        # Text widget for displaying results
        self.result_text = tk.Text(root, height=10, width=40)
        self.result_text.grid(row=8, column=0, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()

        if title and author and genre and year:
            book = Book(title, author, genre, year)
            self.library.add_book(book)
            messagebox.showinfo("Success", "Book added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled.")

    def remove_book(self):
        title = self.title_entry.get()
        if title:
            if self.library.remove_book(title):
                messagebox.showinfo("Success", "Book removed successfully!")
            else:
                messagebox.showwarning("Error", "Book not found.")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Title field must be filled.")

    def search_book(self):
        title = self.title_entry.get()
        if title:
            book = self.library.search_by_title(title)
            if book:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, str(book))
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Book not found.")
        else:
            messagebox.showwarning("Input Error", "Title field must be filled.")

    def display_books(self):
        books = self.library.display_books()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, books if books else "No books in the library.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


