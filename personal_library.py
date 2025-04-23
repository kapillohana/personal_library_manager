import streamlit as st

import json
import os

# File path for saving library data
LIBRARY_FILE = "library_data.json"

def load_library():
    """Load library data from file if it exists"""
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_library():
    """Save current library to file"""
    with open(LIBRARY_FILE, 'w') as f:
        json.dump(st.session_state.library, f)

# Initialize the library from file
if 'library' not in st.session_state:
    st.session_state.library = load_library()

def add_book():
    st.header("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        
        if st.form_submit_button("Add Book"):
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read
            }
            st.session_state.library.append(book)
            save_library()  # Save after adding
            st.success("Book added successfully!")

def remove_book():
    st.header("Remove a Book")
    if not st.session_state.library:
        st.warning("Your library is empty.")
        return
    
    titles = [book['title'] for book in st.session_state.library]
    selected_title = st.selectbox("Select book to remove", titles)
    
    if st.button("Remove Book"):
        st.session_state.library = [book for book in st.session_state.library 
                                  if book['title'] != selected_title]
        save_library()  # Save after removing
        st.success("Book removed successfully!")

def search_books():
    st.header("Search Books")
    search_type = st.radio("Search by:", ["Title", "Author"])
    search_term = st.text_input(f"Enter {search_type} to search")
    
    if search_term:
        if search_type == "Title":
            results = [b for b in st.session_state.library 
                      if search_term.lower() in b['title'].lower()]
        else:
            results = [b for b in st.session_state.library 
                      if search_term.lower() in b['author'].lower()]
        
        if results:
            st.subheader("Matching Books")
            for book in results:
                status = "✓ Read" if book['read'] else "✗ Unread"
                st.write(f"**{book['title']}** by {book['author']} ({book['year']})")
                st.write(f"Genre: {book['genre']} | Status: {status}")
                st.write("---")
        else:
            st.warning("No matching books found.")

def display_books():
    st.header("Your Library")
    if not st.session_state.library:
        st.warning("Your library is empty.")
        return
    
    for i, book in enumerate(st.session_state.library, 1):
        status = "✓ Read" if book['read'] else "✗ Unread"
        st.subheader(f"{i}. {book['title']}")
        st.write(f"**Author:** {book['author']}")
        st.write(f"**Year:** {book['year']} | **Genre:** {book['genre']} | **Status:** {status}")
        st.write("---")

def display_stats():
    st.header("Library Statistics")
    total = len(st.session_state.library)
    
    if total == 0:
        st.warning("Your library is empty.")
        return
    
    read_count = sum(1 for book in st.session_state.library if book['read'])
    percentage = (read_count / total) * 100
    
    st.metric("Total books", total)
    st.metric("Percentage read", f"{percentage:.1f}%")
    
    # Visual progress bar
    st.progress(percentage/100)

# Main app layout
st.title("📚 Personal Library Manager")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", 
                           ["Add Book", "Remove Book", "Search Books", 
                            "View Library", "Statistics"])

if menu == "Add Book":
    add_book()
elif menu == "Remove Book":
    remove_book()
elif menu == "Search Books":
    search_books()
elif menu == "View Library":
    display_books()
elif menu == "Statistics":
    display_stats()