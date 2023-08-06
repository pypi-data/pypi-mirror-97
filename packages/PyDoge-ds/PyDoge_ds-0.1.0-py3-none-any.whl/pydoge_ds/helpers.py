def get_query_params(query_params):
    params = [f'{key}={value}' for key, value in query_params.items()]
    return '?' + '&'.join(params)
