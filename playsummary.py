import pandas as pd
import polars as pl

from datetime import datetime
from xmlapi2 import Thing
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential())
def data(game_id):
    url = f'https://boardgamegeek.com/playsummary/thing/{game_id}'
    yearpublished = Thing(game_id).number('yearpublished')
    
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
            pl.col('Date') < datetime.now(),
            pl.col('Date').dt.year() >= yearpublished
        )
    )

    return df
