from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="MovieLens Ratings", layout="wide")
st.title("MovieLens Ratings Dashboard")
st.caption("Explore movie genres, rating patterns, and top-rated films.")


@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "data" / "movie_ratings.csv"
    data = pd.read_csv(data_path)
    data["year"] = pd.to_numeric(data["year"], errors="coerce")
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    return data.dropna(subset=["movie_id", "rating", "genres"])


ratings = load_data()
genre_rows = ratings.assign(genre=ratings["genres"].str.split("|")).explode("genre")
genre_rows = genre_rows[genre_rows["genre"].notna() & genre_rows["genre"].ne("")]

st.sidebar.header("Filters")
selected_genres = st.sidebar.multiselect(
    "Genres", sorted(genre_rows["genre"].unique()), default=[]
)
minimum_ratings = st.sidebar.select_slider(
    "Minimum ratings per movie", options=[50, 100, 150, 200], value=50
)

if selected_genres:
    genre_rows = genre_rows[genre_rows["genre"].isin(selected_genres)]

st.subheader("1. Genre Breakdown")
st.caption(
    "Counts are distinct rated movies per genre. Movies with multiple genres count once in each; "
    "therefore these counts do not sum to the number of movies."
)
genre_counts = (
    genre_rows.groupby("genre")["movie_id"]
    .nunique()
    .sort_values(ascending=True)
    .rename("Rated movies")
    .reset_index()
)
st.plotly_chart(
    px.bar(
        genre_counts,
        x="Rated movies",
        y="genre",
        orientation="h",
        title="Number of Rated Movies by Genre",
        labels={"genre": "Genre"},
    ),
    width="stretch",
)

st.subheader("2. Genre Satisfaction")
genre_means = (
    genre_rows.groupby("genre")["rating"]
    .mean()
    .sort_values(ascending=True)
    .rename("Mean rating")
    .reset_index()
)
st.caption("A rating for a multi-genre movie contributes to each of its genres.")
st.plotly_chart(
    px.bar(
        genre_means,
        x="Mean rating",
        y="genre",
        orientation="h",
        title="Average Rating by Genre",
        labels={"genre": "Genre", "Mean rating": "Mean rating (1-5)"},
    ),
    width="stretch",
)

st.subheader("3. Ratings Over Release Years")
year_rows = ratings.dropna(subset=["year"])
if selected_genres:
    selected_genre_set = set(selected_genres)
    year_rows = year_rows[
        year_rows["genres"].str.split("|").map(
            lambda movie_genres: not selected_genre_set.isdisjoint(movie_genres)
        )
    ]
year_means = year_rows.groupby("year", as_index=False)["rating"].mean()
st.caption("Mean individual rating grouped by the movie's release year, not the rating date.")
st.plotly_chart(
    px.line(
        year_means,
        x="year",
        y="rating",
        title="Mean Rating by Movie Release Year",
        labels={"year": "Release year", "rating": "Mean rating (1-5)"},
    ),
    width="stretch",
)

st.subheader("4. Best Movies, With a Rating-Count Floor")
movie_stats = (
    ratings.groupby(["movie_id", "title"], as_index=False)
    .agg(mean_rating=("rating", "mean"), rating_count=("rating", "count"))
)
if selected_genres:
    selected_movie_ids = genre_rows["movie_id"].unique()
    movie_stats = movie_stats[movie_stats["movie_id"].isin(selected_movie_ids)]

top_columns = st.columns(2)
for chart_index, (column, floor) in enumerate(zip(top_columns, (minimum_ratings, 150))):
    top_movies = (
        movie_stats[movie_stats["rating_count"] >= floor]
        .sort_values(["mean_rating", "rating_count", "title"], ascending=[False, False, True])
        .head(5)
        .sort_values("mean_rating", ascending=True)
    )
    with column:
        st.markdown(f"**At least {floor} ratings**")
        st.plotly_chart(
            px.bar(
                top_movies,
                x="mean_rating",
                y="title",
                orientation="h",
                hover_data={"rating_count": True, "mean_rating": ":.2f"},
                labels={"title": "Movie", "mean_rating": "Mean rating (1-5)", "rating_count": "Ratings"},
            ),
            key=f"top_movies_{chart_index}",
            width="stretch",
        )