import streamlit as st
import pandas as pd
import json
import os
import time
import random
import requests
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Personal Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem !important;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem !important;
        color: #3BB2F6;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        border-radius: 0.375rem;
    }
    .warning-message {
        padding: 1rem;
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
    }
    .book-card {
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
        transition: transform 0.3s ease;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    .read-badge {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .unread-badge {
        background-color: #F87171;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .action-button {
        margin-right: 0.5rem;
    }
    .st button>button {
        border-radius: 0.375rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Lottie animation (optional)
def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize session state
if 'library' not in st.session_state:
    st.session_state.library = []

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if 'books_added' not in st.session_state:
    st.session_state.books_added = False

if 'books_removed' not in st.session_state:
    st.session_state.books_removed = False

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'library'


# Load library from JSON file
def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
            return True
        return False
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False


# Save library to JSON file
def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
        return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False


# Add a book to the library
def add_book(title, authors, publication_year, genre, read_status):
    book = {
        'title': title,
        'authors': authors,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.now().strftime("%y-%d-%m %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.books_added = True
    time.sleep(0.5)  # Animation delay


# Remove a book from the library
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.books_removed = True
        return True
    return False


# Search books in the library
def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []
    for book in st.session_state.library:
        if search_by == "title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "authors" and search_term in book['authors'].lower():
            results.append(book)
    st.session_state.search_results = results


# Get the state of the library
def get_library_state():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    genres = {}
    authors = {}
    decades = {}
    for book in st.session_state.library:
        # Count genres
        if book['genre'] in genres:
            genres[book['genre']] += 1
        else:
            genres[book['genre']] = 1

        # Count authors
        if book['authors'] in authors:
            authors[book['authors']] += 1
        else:
            authors[book['authors']] = 1

        # Count decades
        decade = (book['publication_year'] // 10) * 10
        if decade in decades:
            decades[decade] += 1
        else:
            decades[decade] = 1

    # Sort by count
    genres = dict(sorted(genres.items(), key=lambda x: x[1], reverse=True))
    authors = dict(sorted(authors.items(), key=lambda x: x[0]))
    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'genres': genres,
        'authors': authors,
        'decades': decades
    }

def create_visulation(stats):
    if stats['total_books'] > 0:  # Fixed the key to 'total_books'
        # The code inside the 'if' block must be indented
        fig_read_status = go.Figure(data=[go.Pie(
            labels=['read', 'unread'],
            values=[stats['read_books'], stats['total_books'] - stats['read_books']],
            hole=.4,
            marker_colors=['#163981', '#F87171']
        )])
        fig_read_status.update_layout(
            title_text="Read vs Unread Books",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_read_status, use_container_width=True)
        
        # BAR chart genres
        if stats['genres']:
            genres_df = pd.DataFrame({
                'genre': list(stats['genres'].keys()),
                'count': list(stats['genres'].values())
            })
            fig_genres = px.bar(
                genres_df,
                x='genre',
                y='count',
                color='count',
                color_continuous_scale=px.colors.sequential.Blues
            )
            fig_genres.update_layout(
                title_text="Books by Genre",
                xaxis_title="Genres",
                yaxis_title="Number of Books",
                height=400
            )
            st.plotly_chart(fig_genres, use_container_width=True)

        # Line chart for decades
        if stats['decades']:
            decade_df = pd.DataFrame({
                'decade': [f"{decade}s" for decade in stats['decades'].keys()],
                'count': list(stats['decades'].values())
            })
            fig_decades = px.line(
                decade_df,
                x='decade',
                y='count',
                markers=True,
                line_shape="spline"
            )
            fig_decades.update_layout(
                title_text="Books by Publication Decade",
                xaxis_title="Decade",
                yaxis_title="Number of Books",
                height=400
            )
            st.plotly_chart(fig_decades, use_container_width=True)

            # load library 
            load_library

            st.sidebar.markdown("ch1 style= 'text.algie: center':> navigation</h1>",
                                unsafe_allow_html=True)
        lottie_book= load_lottie_url("http://assests9.lottiefiles.com/temp/1f20_aAafin.json")
        if lottie_book:
            with st.sidebar:
                st.lottie(lottie_book, height=200, key ='book_animation')
                nav_option= st_sidebar.radio(
                    "choose in option:",
                    ["view library", "add book", "search books", "library statistic"]
                )
                if new_options== "view library":
                    st.session_state.current_view = "library"
                elif new_options== "add_book":
                    st.session_state.current_view= "add"
                elif new_option== "search_books":
                    st.session_state.current_view= "search"
                elif new_option== "library statistics":
                    st.session_state.current_view= "stats"
# Example of properly indented code:
if st.session_state.current_view == "library":
    st.markdown("<h1 class='main-header'> Personal Library Manager </h1>", unsafe_allow_html=True)
    # other code...

               # Example: If inside a function
def some_function():
    if st.session_state.current_view == "add":
        # indented properly inside the if block
        st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)

                    # adding books input form 
if some_condition:
    # Indent the function correctly inside the if block
def some_function():
    # Inside some_function, we define add_book_form with proper indentation
    def add_book_form():
        title = st.text_input("Book title", max_chars=100)
        author = st.text_input("Author", max_chars=100)
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Technology", "Fantasy", "Romance", "Poetry", "Art"])
        read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
        
        submit_button = st.form_submit_button(label="Add Book")
        
        if submit_button and title and author:
            # Add book logic here
            pass


                                    add_book(title,author,publication_year,genre,read_status)
                                    if st.session_state.book_added:
                                        st.markdown("<div class= 'sucess.message'>book added sucessfully! </div>", unsafe_allow_html=True)
                                        st.balloons()
                                        st.session_state.book_added=False
                                    elif st.session_state.current_view=="library":
                                        st.markdown("<h2 class= 'sub.header'> your library </h2>",unsafe_allow_html=True)
                                        if not st.session_state.library:
                                            st.markdown("<div class= 'warning.message'> your library is empty is empty. add some book to get started! </div>",
                                                        unsafe_allow_html=True)
                                        else:
                                            cols= st.column(2)
                                            for i, book in enumerate(st.session_state.library):
                                                with cols(i % 2):
                                                    st.markdown(f"""<div class ='book.card>
                                                                <h3> {book['title']}</h3>
                                                                <p><strong> author:</strong>
                                                                {book['author']}</p>
                                                                <p><strong> publication year:</strong>
                                                                {book['publication year']}</p>
                                                                <p> <strong> genre: </strong>
                                                                {book['genre']}</p>
                                                                <p> <span class ='{"read badge'"}
if book ["read_status"]
else {"unread.badge"}'> {
    "read" if book ["read_status"]
    else "un read"
}
</span> </p>
</div>
                                                           
""", unsafe_allow_html=True)
                                                    col1,col2= st.columns(2)
                                                    with col1:
                                                        if st.button(f"remove",key=f"remove{i}",use_container_width=True):
                                                            if remove_book(i):
                                                                st.rerun()
                                                                with col2:
                                                        new_status = not book['read_status']
                                                        status_label="mark is read"
                                                      if not book ['read_status']:
                                                     else   ("mark is unread")
                                                    if st.button (status_label,key= f"status_(i)",use_container_width=True):
                                               st.session_state.library[i]['read status']= new_status
                                            save_library()
                                            st.rerun()
                                            if st.session_state.book_removed:
 st.markdown("<div class='sucess.message'> book removed sucessfully!</div>", unsafe_allow_html= True)
st.session_state.book_removed=False
elif st.session_state.current_view=="search":
st.markdown("<h2 class ='sub.header'>search books </h2> ", unsafe_allow_html=True)
search_by= st.selectbox("search_by:",["title", "author", "genre"])
search_term= st.text_input("enter search term:")
if search_term:
    with st.spinner("searching..."):
        time.sleep(0.5)
        search_books(search_term, search_by)
        if hasattr(st.session_state, 'search_results'):
          if  st.session_state.search_results:
              st.markdown(f"<h3> found{len(st.session_state.search_results)} results:</h3>", unsafe_allow_html= True)
              for i, book in enumerate(st.session_state.search_results):
                  st.markdown(f"""<div class ='book-card'>
                                                                <h3> {book['title']}</h3>
                                                                <p><strong> author:</strong>
                                                                {book['author']}</p>
                                                                <p><strong> publication year:</strong>
                                                                {book['publication year']}</p>
                                                                <p> <strong> genre: </strong>
                                                                {book['genre']}</p>
                                                                <p> <span class ='{"read badge'"}
if book ["read_status"]
else {"unread.badge"}'> {
    "read" if book ["read_status"]
    else "un read"
}
</span> </p>
</div>
                                                           
""", unsafe_allow_html=True)
              elif search_term:
st.markdown("div class = 'warning-messsage'> no books found matching in search.</div>",unsafe_allow_html= True)
elif st.session_state.current_view =="stats":
st.markdown("<h2 class= 'sub.header'> library statistics</h2>", unsafe_allow_html=True)
if not st.session_state.library:
    st.markdown("<div class='warning-message'> your library is empty. add some books to see stats! </div>", unsafe_allow_html=True)
else: 
    stats= get_library_state()
    col1,col2,cols = st.columns(3)
    with col1:
        st.matric("total books", stats['total_books'])
        with col2:
            st.matric("book read",stats['read_book'])
            with cols:
                st.matric("percentage read", f"{stats['percentage_read']:.if}%")
                create_visulation()
                if stats['authors']:
                    st.markdown("<h3> top authors</h3>",unsafe_allow_html=True)
                    top_authors= dict(list(stats['authors'].items())[:5])
                    for authors, count in top_authors.items():
                        st.markdown(f"**{authors}**:{count} book{'s' if count> 1 else''}")
                        st.markdown("_ _ _")
                        st.markdown("copyright @ 2025 jabir Ali personal library manager", unsafe_allow_html=True)

                                      
                    
                                      
                  


                                                                                
                                                                                
                                                                                            
                                                                        
 

                                






                      
                  
                      
                  
