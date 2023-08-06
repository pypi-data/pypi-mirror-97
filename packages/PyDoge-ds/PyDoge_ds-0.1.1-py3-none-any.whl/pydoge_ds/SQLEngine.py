import pandas as pd
from sqlalchemy import create_engine
from pydoge_ds import get_query_params


class SQLEngine:
    def __init__(self, dialect, user, password, host, port, database='', query_dict=None, params={}):
        template_url = '{dialect}://{user}:{password}@{host}:{port}/{database}'

        url = template_url.format(
            dialect=dialect,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

        if query_dict:
            query_params = get_query_params(query_dict)
            url = url + query_params

        self.engine = create_engine(str(url), **params)

    def read_sql(self, query, chunksize=10000):
        with self.engine.connect() as conn:
            li = []
            i = 0
            for df in pd.read_sql(
                query,
                conn,
                chunksize=chunksize,
            ):
                i += 1
                print(f'lap {i}')
                if len(df) > 0:
                    li.append(df)

            return pd.concat(li, ignore_index=True)
