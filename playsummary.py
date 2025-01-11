import pandas as pd
import polars as pl
from datetime import datetime

def data(game_id, release_year=0):
    url = f'https://boardgamegeek.com/playsummary/thing/{game_id}'
    df = (
        pl.from_pandas(
            pd.read_html(url)[1]
        )
        .with_columns(
            pl.col('Date')
                .str.to_date(format='%Y-%m', strict=False)
                .dt.month_end(),
            (pl.col('Number of Plays') / pl.col('Distinct Users'))
                .alias('Plays per User')
        )
        .filter(
            pl.col('Date') < datetime.now()
        )
    )

    if release_year > 0:
        df = df.filter(
            pl.col('Date') > datetime(release_year, 1, 1)
        )

    return df
