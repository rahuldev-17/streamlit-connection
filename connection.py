from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

import weaviate
import json
import pandas as pd

class weaviateConnection(ExperimentalBaseConnection[weaviate.client.Client]):
    """Basic st.experimental_connection implementation for weaviate vector database"""

    def _connect(self, **kwargs) -> weaviate.client.Client:
        if 'url' in kwargs:
            _url = kwargs.pop('url')
        else:
            raise KeyError("URL missing")
            # raise error
        if 'api_key' in kwargs:
            _api_key = kwargs.pop('api_key')
        else:
            raise KeyError("Provide API key")
        return weaviate.client.Client(_url,  _api_key)
    
    def client(self) -> weaviate.client.Client:
        return self._instance

    def query(self, target_class: str,properties:list , nearText:dict,limit:int , ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _query(target_class: str,properties:list, nearText:dict,limit:int, **kwargs) -> pd.DataFrame:
            client = self.client() 
            response_data= client.query.get(target_class,properties, **kwargs).with_near_text(nearText).with_limit(limit).do()
            print(type(response_data))
            return response_data
        
        return _query(target_class,properties, nearText, limit,  **kwargs)
    
