import streamlit as st
import pickle
import requests

# Load pre-trained data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch movie poster using TMDB API
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ea44810c1315695b3d0cf94bf164b24b&language=en-US")
    data = response.json()
    if 'poster_path' not in data or not data['poster_path']:
        return 'https://via.placeholder.com/500'  # Fallback image
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset!")
        return [], []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# App title and description
st.title("🎬 Movie Recommender System")
st.markdown("""
    **Find movies similar to your favorites!**  
    Search for a movie, and we’ll recommend 5 similar movies based on your preferences.
""")

# Inject custom CSS for the select box hover effect on the dropdown arrow
st.markdown("""
    <style>
    .css-1yqz5w1.e8zbici1 {
        font-size: 18px;
        padding-right: 30px;
        cursor: pointer;
    }

    /* Styling the arrow on hover */
    .css-1yqz5w1.e8zbici1:hover {
        color: blue;
    }
    </style>
""", unsafe_allow_html=True)

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    "Enter or select a movie",
    movies['title'].values,
    help="Start typing to search for a movie"
)

# Recommend button
if st.button('🎥 Recommend Movies'):
    names, posters = recommend(selected_movie_name)

    # Enhanced layout with rows and columns
    if names:
        st.markdown("### Recommended Movies")
        cols = st.columns(5)  # Dynamically generate 5 columns
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, use_container_width=True, caption=name)
    else:
        st.warning("No recommendations found!")

# Footer
st.markdown("---")
st.markdown("Made by Siddhant👨‍💻| [GitHub](https://github.com)")
