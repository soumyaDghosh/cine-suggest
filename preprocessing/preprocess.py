import ast
import pandas as pd

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    movies: pd.DataFrame = pd.read_csv("data/tmdb_5000_movies.csv")
    credits: pd.DataFrame = pd.read_csv("data/tmdb_5000_credits.csv",)
    return movies, credits

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def format_and_merge(movies: pd.DataFrame, credits: pd.DataFrame) -> pd.DataFrame:
    movies=movies[["id", "genres", "keywords", "overview", "title"]]
    df: pd.DataFrame = movies.merge(credits, left_on=["id", "title"], right_on=["movie_id", "title"])
    df.drop(columns=["id"], inplace=True)
    df.genres=df.genres.apply(deduplicate_rows)
    df.cast=df.cast.apply(deduplicate_rows, max=5)
    df.crew=df.crew.apply(lambda crews: [crew["name"].replace(" ", "").lower() for crew in ast.literal_eval(crews) if crew['job'].lower() in ["screenplay", "director", "producer"]])
    df.keywords=df.keywords.apply(deduplicate_rows)
    df.overview=df.overview.apply(lambda overview: overview.lower().split())
    df["tags"]=df["overview"]+df["genres"]+df["cast"]+df["crew"]+df["keywords"]
    df=df[["movie_id", "title", "tags"]]
    """
    <python-input-161>:1: SettingWithCopyWarning:
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead

    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    """
    df.tags=df.tags.apply(lambda x: " ".join(x))
    return df

def deduplicate_rows(objs, max: int = None) -> list:
    result=[]
    for obj in ast.literal_eval(objs):
        result.append(obj["name"].replace(" ", "").lower())
        if "character" in obj.keys():
            result.append(obj["character"].replace(" ", "").lower())
    return list(set(result))[:max] if max else list(set(result))

def save_processed(df, path="data/processed_tmdb.pkl"):
    df.to_pickle(path)


if __name__ == "__main__":
    movies, credits = load_data()
    movies = clean(movies)
    credits = clean(credits)
    df = format_and_merge(movies, credits)
    save_processed(df)
    print("Preprocessing complete. Saved to data/processed_tmdb.pkl")
