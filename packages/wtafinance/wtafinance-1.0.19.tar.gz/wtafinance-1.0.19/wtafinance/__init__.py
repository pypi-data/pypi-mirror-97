import requests, json, os,copy

class ClassCodeConfig():
    config = []
    fieldConfig_url = "./fieldConfig.json"

    @classmethod
    def initConfig(cls):#cls 静态方法中的当前类
        url = "http://106.53.251.60/app_finance/getcodeconfig"
        res = requests.get(url, timeout=60)
        req_data = json.loads(res.text)
        if os.path.exists(cls.fieldConfig_url):
            file_data = cls.load_config()
            res_data = copy.deepcopy(file_data)

            # 把新增的大类编码提取加入
            file_data_classcode_set = set([i["ClassCode"] for i in file_data])
            for class_item in req_data:
                classCode = class_item["ClassCode"]
                if classCode not in file_data_classcode_set:#数据库的classcode不在本地文件中 说明本地无此大类 直接加入即可
                    break
                # 获取该大类在本地文件中的所有字段
                file_data_targetUnitCode_list = [i for i in file_data if i["ClassCode"]==classCode][0]["TargetUnitCode"]
                # 筛选名称与别名不一致的字段
                diff_dict = {i["Name"]:i["AliasName"] for i in file_data_targetUnitCode_list if i["Name"]!=i["AliasName"]}
                for targetUnitCode in class_item["TargetUnitCode"]:
                    #  修改替换字段
                    if targetUnitCode["Name"] in diff_dict.keys():
                        targetUnitCode["AliasName"] = diff_dict[targetUnitCode["Name"]]
        cls.dump_config(req_data)
        cls.config = req_data

    @classmethod
    def dump_config(cls,data):
        with open(cls.fieldConfig_url, 'w', encoding='utf-8') as f:
            json.dump(data, f)#json 写


    @classmethod
    def load_config(cls):
        with open(cls.fieldConfig_url, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

ClassCodeConfig.initConfig()


if __name__ == '__main__':
    con = ClassCodeConfig.config

    print([i for i in ClassCodeConfig.config if i["ClassCode"] == "1001"][0]["ClassName"])
    s = [i for i in ClassCodeConfig.config if i["ClassCode"] == "1001"][0]["TargetUnitCode"]

    # columns = [self.class_target_code_conf[str(target.code)] for target in self.class_head.target_subset]
    columns = [i["AliasName"] for i in s if
               i["Code"] in [target for target in ["1001001","1001002"]]]


    print(s)

