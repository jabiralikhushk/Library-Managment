class Book:
    def __init__(self, title, author, genre, status="Available"):
        self.title = title
        self.author = author
        self.genre = genre
        self.status = status

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Status: {self.status}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def view_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            for book in self.books:
                print(book)

    def delete_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                self.books.remove(book)
                print(f"Book '{title}' has been deleted.")
                return
        print(f"Book '{title}' not found.")

    def search_book(self, search_term):
        found_books = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower()]
        if found_books:
            for book in found_books:
                print(book)
        else:
            print(f"No books found matching '{search_term}'.")

    def update_book(self, title, new_title=None, new_author=None, new_genre=None, new_status=None):
        for book in self.books:
            if book.title.lower() == title.lower():
                if new_title:
                    book.title = new_title
                if new_author:
                    book.author = new_author
                if new_genre:
                    book.genre = new_genre
                if new_status:
                    book.status = new_status
                print(f"Book '{title}' has been updated.")
                return
        print(f"Book '{title}' not found.")


def menu():
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. View Books")
    print("3. Delete Book")
    print("4. Search Book")
    print("5. Update Book")
    print("6. Exit")

def main():
    library = Library()

    while True:
        menu()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            genre = input("Enter book genre: ")
            book = Book(title, author, genre)
            library.add_book(book)
            print("Book added successfully.")
        
        elif choice == '2':
            library.view_books()
        
        elif choice == '3':
            title = input("Enter book title to delete: ")
            library.delete_book(title)

        elif choice == '4':
            search_term = input("Enter title or author to search: ")
            library.search_book(search_term)

        elif choice == '5':
            title = input("Enter book title to update: ")
            print("Leave blank to keep current values.")
            new_title = input("Enter new title: ")
            new_author = input("Enter new author: ")
            new_genre = input("Enter new genre: ")
            new_status = input("Enter new status (Available/Checked Out): ")
            library.update_book(title, new_title, new_author, new_genre, new_status)

        elif choice == '6':
            print("Exiting the system...")
            break

        else:
            print("Invalid choice! Please select again.")


if __name__ == "__main__":
    main()

