from wtafinance.finance_api import stock,filedata_source_process


def wta_api(secret_key,secret_id):
    instance = stock.DataApi(secret_key,secret_id)
    return instance

def set_path(str_path):
    with open("./path.config","w",encoding="utf-8") as f:
        f.write(str_path)

def get_path():
    with open("./path.config","r",encoding="utf-8") as f:
        str_path = f.readline()
    return str_path

def get_mainClass():
    '''
    :param RootPath: 数据路径
    :return:
    '''
    instance = filedata_source_process.MainClass(get_path())
    return instance




def wta_file_config_code():
    '''
    获取全部表的编码
    :return:
    '''
    return filedata_source_process.ClassCodeConfig.config

def get_table_field_code(parentTableName=None,isParent=False):
    '''
    获取字段编码
    :param isParent 是否只查询父类，默认False:
    :param parentTableName 父类的表名，isParent为false时必传:
    :return:
    '''
    if not isinstance(isParent,bool):
        isParent=False
    if isParent:
        return [{"ClassCode": i["ClassCode"],
            "ClassName": i["ClassName"]} for i in filedata_source_process.ClassCodeConfig.config]
    else:
        res = [i["TargetUnitCode"]
                for i in filedata_source_process.ClassCodeConfig.config
                if i["ClassName"]==parentTableName]
        if len(res)!=0:
            return res[0]
        else:
            return None