import requests,json
import pandas as pd
from functools import partial

#目前读文件没用到，只有张总那边用到

class DataApi(object):
    _instance = None
    http_url = "http://106.53.251.60/app_finance/apidata"

    def __init__(self,secret_key,secret_id, timeout=15):#第二步
        self._secret_key = secret_key
        self._secret_id = secret_id
        self._timeout = timeout

    def __new__(cls, *args, **kwargs):#实例化一个类时调用的第一步调用方法  *args：多余的参数，如seccode, **kwargs：多余的关键字参数
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            return cls._instance
        else:
            return cls._instance

    def query(self,api_name, **kwargs):#包装 方法 参数
        data={
            "secret_key":self._secret_key,
            "secret_id":self._secret_id,
            "api_name":api_name,
            "api_params":kwargs
        }
        res = requests.get(self.http_url,json=data, timeout=60)
        if res:
            result = json.loads(res.text)
            if result['code'] != 0:
                raise Exception(result['msg'])
            data = result['data']
            if len(data) == 0:
                return pd.DataFrame()
            columns = data[0].keys()#data是一个list[dict()],取第一行dict的keys作为列名
            items = data
            return pd.DataFrame(items, columns=columns)
        else:
            return pd.DataFrame()
    #调用实例的方法、属性时触发
    def __getattr__(self, api_name,**kwargs): # 如:wta.getWtaBalanceSheet(SECCODE="300100") api_name:方法名 如：getWtaBalanceSheet, **kwargs:关键字参数，如：SECCODE="300100"
        return partial(self.query,api_name)

