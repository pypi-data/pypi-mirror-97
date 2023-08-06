import struct,math,time,datetime,threading,os
import pandas as pd
from wtafinance import ClassCodeConfig
# 格式符        C语言类型	        Python类型	        Standard size
# x             pad byte(填充字节)	no value
# c	            char	            string of length 1	1
# b	            signed              char integer	    1
# B	            unsigned            char integer	    1
# ?	            _Bool	            bool	            1
# h	            short	            integer	            2
# H	            unsigned            short integer	    2
# i	            int	                integer	            4
# I(大写的i)	unsigned            int	integer	        4
# l(小写的L)	long	            integer	            4
# L	            unsigned long	    long	            4
# q	            long long	        long	            8
# Q	            unsigned long long	long	            8
# f	            float	            float	            4
# d	            double	            float	            8
# s	            char[]	            string
# p	            char[]	            string
# P	            void *	            long
class BaseFunc(object):
    def hex_to_int(self,h):
        i = int(h, 16)
        return i
    def int_to_hex(self,i):
        h = hex(i)
        return h

    def sum_str(self,data):
        s = ""
        for i in data:
            s += i
        return s

    def reverse_list(self,data):
        data.reverse()
        return data

    def timeatamp_to_format(self, timeStamp):
        # timearray = time.localtime(timeStamp)
        # res = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
        res = datetime.datetime.fromtimestamp(timeStamp)
        # if "00:00:00" in res:
        #     res = self.timeatamp_to_format(timeStamp+(3600*2))
        if res.hour==0:#若为0点，则将时间+2小时
            res = datetime.datetime.fromtimestamp(timeStamp+(3600*2))
        return res


    def timestr_to_timeatamp(self, timestr):
        if " " in timestr:#2021-03-02 11：39：50
            data_sj = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")  # 定义格式
        else:#2021-03-02
            data_sj = time.strptime(timestr, "%Y-%m-%d")  # 定义格式
        timeatamp = int(time.mktime(data_sj))
        return timeatamp


    def get_unicode_str(self,bytes):
        '''
        :param bytes: 字符列表
        :return:
        '''
        # 目标: 将文件中读到的字符列表转成Unicode的string；Unicode string \u4eec
        # 原始字符列表举例 : e4ce...
        unicode_str_list = ['\\u'+self.sum_str(self.reverse_list(bytes[i:i+2])) for i in range(0,len(bytes),2)]
        return self.sum_str(unicode_str_list).encode('utf-8').decode("unicode_escape")

    def get_ascii_str(self,bytes):
        '''
        获取Ascii码对应字符串
        :param bytes:
        :return:
        '''
        return self.sum_str([chr(self.hex_to_int(i)) for i in bytes])

class TargetUnit(object):
    def __init__(self, code, unit, digit, storage_type,base_class_code):
        '''
        指标实例化
        :param code: 指标代码
        :param unit: 货币单位
        :param digit: 数值位数
        '''
        self.code = str(code)
        self.base_class_code = base_class_code
        # self.name = [i["TargetUnitCode"][self.code] for i in ClassCodeConfig.config if i["ClassCode"] == self.base_class_code][0]
        self.name = [[j for j in i["TargetUnitCode"] if j["Code"] == self.code][0]["AliasName"] for i in ClassCodeConfig.config if
         i["ClassCode"] == self.base_class_code][0]

        self.unit = unit
        self.digit = digit
        self.storage_type = storage_type
        # print("指标代码：",self.code)
        # print("指标单位：",self.unit)
        # print("指标位数：",self.digit)

class FileHead(object):
    '''
    文件头
    '''
    def __init__(self,sec_code,sec_name,market,flag,class_count,class_subset):
        '''
        初始化文件头部参数
        :param sec_code: 股票代码
        :param sec_name: 股票简称
        :param market: 市场
        :param flag: 股票自定义标识
        :param class_count: 大类个数
        :param class_subset: 大类子集   大类指已编码的Table,如:资产负债、日数据、5分钟
        '''
        self.sec_code = sec_code
        self.sec_name = sec_name
        self.market = market
        self.flag = flag #暂时没用到
        self.class_count = class_count
        self.class_subset:list = class_subset

class ClassHead(BaseFunc):
    '''
    大类头部
    '''
    def __init__(self,class_head_hexs):
        self.code, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[:4]))) # 大类代码
        self.code = str(self.code)
        self.name = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.code][0]["ClassName"]
        self.target_count, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[4:8])))   # 指标个数
        self.DataLen, = struct.unpack("H", bytes.fromhex(self.sum_str(class_head_hexs[8:10]))) # 数据长度
        self.latest_time, = struct.unpack("I", bytes.fromhex(self.sum_str(class_head_hexs[10:14])))   # 指标最新时间
        self.latest_time = self.timeatamp_to_format(self.latest_time)
        self.target_subset = []
        # print("大类：",self.code)
        for i in range(self.target_count):
            limit = i*21
            target_code, = struct.unpack("q", bytes.fromhex(self.sum_str(class_head_hexs[14+limit:22+limit])))
            target_unit = self.get_unicode_str(class_head_hexs[22+limit:26+limit])
            target_digit, = struct.unpack("q", bytes.fromhex(self.sum_str(class_head_hexs[26+limit:34+limit])))
            target_storage_type = self.get_ascii_str(class_head_hexs[34+limit:35+limit])
            self.target_subset.append(TargetUnit(target_code, target_unit, target_digit, target_storage_type,self.code))

class ClassUnit(BaseFunc):
    def __init__(self,class_code,class_start_address,class_head_hexs=None,class_body_hexs=None):
        '''
        初始化大类
        :param class_code: 大类编码
        :param class_start_address: 大类起始地址
        :param class_head_hexs: 大类头部内容
        :param class_body_hexs: 大类数据内容
        '''
        self.class_code = str(class_code)
        self.class_target_code_conf = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.class_code][0]["TargetUnitCode"]
        self.class_name = [i for i in ClassCodeConfig.config if i["ClassCode"] == self.class_code][0]["ClassName"]
        self.class_start_address = class_start_address
        self.class_head_hexs = class_head_hexs
        self.class_body_hexs = class_body_hexs
        self.class_head: ClassHead = None  # 大类头部内容
        self.class_body: pd.DataFrame = None  # 大类数据内容

    def init_class_data(self,limit):

        # columns = [self.class_target_code_conf[str(target.code)] for target in self.class_head.target_subset]
        file_code_dict = {i["Code"]: i["AliasName"] for i in self.class_target_code_conf}
        columns = [file_code_dict[str(target.code)] for target in self.class_head.target_subset]
        columns.insert(0, "time")
        # data = [self.class_body_hexs[i:i+limit] for i in range(0, len(self.class_body_hexs), limit) if self.class_body_hexs[i:i+limit][:8]]
        data = []
        # 循环每一行
        for i in range(0, len(self.class_body_hexs), limit):
            # 判断是否为最后一条数据
            if struct.unpack('q', bytes.fromhex(self.sum_str(self.class_body_hexs[i:i + limit][:8])))[0] == 0:
                break
            # 把每一行的数据加入到一个列表
            data.append(self.class_body_hexs[i:i+limit])

        for data_index in range(len(data)):
            #  解析字段数据
            # data[data_index] = [struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i+8])))[0]
            #                     if i == 0
            #                     else
            #                     struct.unpack(self.class_head.target_subset[int(i/8)-1].storage_type, bytes.fromhex(self.sum_str(data[data_index][i:i+8])))[0]
            #                     for i in range(0, len(data[data_index]), 8)
            #                     if int(i / 8) - 1 < self.class_head.target_count]
            l = [struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][0:8])))[0]]
            for i in range(0,self.class_head.target_count):
                item = self.class_head.target_subset[i]
                if item.storage_type == "q":
                    l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i*8+8:i*8 + 16])))[0])
                elif item.storage_type == "T":
                    l.append(self.timeatamp_to_format(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i * 8+8:i * 8 + 16])))[0]))
                else:
                    l.append(struct.unpack("d",bytes.fromhex(self.sum_str(data[data_index][i*8+8:i*8 + 16])))[0])
            # for i in range(0, len(data[data_index]), 8):
            #     if int(i / 8)-1 == self.class_head.target_count:
            #         break
            #     elif i==0:
            #         l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            #     elif self.class_head.target_subset[int(i / 8)].storage_type=="T":
            #         l.append(struct.unpack('q', bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            #     elif self.class_head.target_subset[int(i / 8)].storage_type=="d":
            #         l.append(struct.unpack(self.class_head.target_subset[int(i / 8)].storage_type,
            #                                bytes.fromhex(self.sum_str(data[data_index][i:i + 8])))[0])
            data[data_index] = l
        self.class_body = pd.DataFrame(data, columns=columns)

class DataSource(BaseFunc):
    def __init__(self):
        self.file_head:FileHead = None
        self.file_body = dict()

    # 初始化头部
    def init_head(self, head_data):
        '''
        初始化文件头部
        :param data:
        :return:
        '''
        sec_code = str(struct.unpack("q", bytes.fromhex(self.sum_str(head_data[:8])))[0]).zfill(6)
        sec_name = self.get_unicode_str(head_data[8:24])
        market = self.get_ascii_str(head_data[24:26])
        flag = bool(struct.unpack("h", bytes.fromhex(self.sum_str(head_data[26:28])))[0])
        class_count, = struct.unpack("I", bytes.fromhex(self.sum_str(head_data[28:32])))
        class_subset = []
        for i in range(class_count):
            limit = i*12
            class_code, = struct.unpack("I", bytes.fromhex(self.sum_str(head_data[32+limit:36+limit])))
            class_start_address, = struct.unpack("q", bytes.fromhex(self.sum_str(head_data[36+limit:44+limit])))
            class_subset.append(ClassUnit(class_code,class_start_address))
        # market, flag, class_count, class_subset
        # 实例化头部类
        self.file_head = FileHead(sec_code=sec_code, sec_name=sec_name, market=market, flag=flag,
                                  class_count=class_count, class_subset=class_subset)

    #初始化内容
    def init_body(self, body_data):
        i = 0
        for classUnit in self.file_head.class_subset:
            limit = (8*200*4*50+6400)*i
            body_len = 8*200*4*50
            if self.file_head.class_count==1:
                body_len = len(body_data)
            classUnit.class_head_hexs = body_data[0+limit:6400+limit]
            classUnit.class_body_hexs = body_data[6400+limit:body_len+limit]
            classUnit.class_head = ClassHead(classUnit.class_head_hexs)
            classUnit.init_class_data(classUnit.class_head.DataLen)
            self.file_body[str(classUnit.class_head.code)] = classUnit.class_body
            i += 1

    def search_data(self, start,end,class_code):
        res_data = pd.DataFrame()
        if len(self.file_body.keys()) == 0:
            return res_data

        if class_code is None:#目前只有三大财报需要传class_code 因为三大财报是一个股票写一个文件
            for key in self.file_body.keys():
                res_data = self.file_body[key]
        else:
            res_data = self.file_body[class_code]
        start_time=start
        end_time=end
        if start_time is not None:
            start_time = self.timestr_to_timeatamp(start_time)
            res_data = res_data.loc[res_data["time"]>=start_time]#文件里的time是时间戳
        if end_time is not None and end_time!='':
            end_time = self.timestr_to_timeatamp(end_time)
            res_data = res_data.loc[res_data["time"] <= end_time]
        res_data.drop(['time'],axis=1,inplace=True)
        return res_data.reset_index(drop=True) #data frame 自带方法 重置行号

    # def search_data(self, param):
    #     res_data = {}
    #     date_time = param["date_time"]
    #     class_list = param["param_data"]["classList"]
    #     class_list = [{"code": str(class_.class_code), "field": "*"} for class_ in self.file_head.class_subset] if class_list == "*" else class_list
    #     for class_ in class_list:
    #         field_code_conf = [i for i in ClassCodeConfig.config if i["ClassCode"] == class_["code"]][0]["TargetUnitCode"]
    #         if class_["code"] in self.file_body.keys():
    #             res_data[class_["code"]] = self.file_body[class_["code"]]
    #         else:
    #             res_data[class_["code"]] = []
    #             continue
    #         if date_time is not None:
    #             start_time = date_time["startTime"] if "startTime" in date_time.keys() else None
    #             end_time = date_time["endTime"] if "endTime" in date_time.keys() else None
    #             if start_time is not None:
    #                 start_time = self.timestr_to_timeatamp(start_time)
    #                 res_data[class_["code"]] = res_data[class_["code"]].loc[res_data[class_["code"]]["time"]>=start_time]
    #             if end_time is not None:
    #                 end_time = self.timestr_to_timeatamp(end_time)
    #                 res_data[class_["code"]] = res_data[class_["code"]].loc[res_data[class_["code"]]["time"] <= end_time]
    #         if class_["field"] != "*":
    #             field_list = [field_code_conf[str(i)] for i in class_["field"]]
    #             if "time" not in field_list:
    #                 field_list.insert(0,"time")
    #             res_data[class_["code"]] = res_data[class_["code"]][field_list]
    #         if "time" in res_data[class_["code"]].columns.values.tolist():
    #             res_data[class_["code"]]["time"]=res_data[class_["code"]]["time"].apply(self.timeatamp_to_format)
    #
    #     return res_data

    def read_file(self, path):
        '''
        文件读取
        :param path: 路径
        :return:
        '''
        try:
            total_list = []
            with open(path,'rb') as f:
                s = f.read(1024) #1024 bit
                while s:
                    # byte = ord(s)
                    # total_list.append('%02x' % (byte))
                    total_list += ['%02x' % (i) for i in s] #转16进制
                    s = f.read(1024)

            self.init_head(total_list[:1024])#0-1023 header
            self.init_body(total_list[1024:])#1024 - end body
        except IOError as e:
            raise Exception("目标文件夹没有该文件,可能是参数传递错误,路径为："+path)

class MainClass():
    def __init__(self, RootPath,PoolSize = 3):
        self.PoolSize = PoolSize
        self.RootPath = os.path.join(RootPath,"System")
        self.day_fqt= {  # 日数据
                "0": "dat",
                "1": "ldat",
                "2": "rdat",
            }
        self.fzline_fqt={
                "0": "fat",
                "1": "lfat",
                "2": "rfat",
            }
        self.finance_fqt={
                "0":"fin"
            }

    def _do_something_data(self,file_path,start,end,class_code=None):
        data_source = DataSource()
        data_source.read_file(file_path)
        return data_source.search_data(start,end,class_code)#从file body 找table code为class code的表

    def _get_market(self,code):
        return "SH" if code[0] == "6" else "SZ"

    def _get_data_path(self,data_type,ktype,fqt,code):
        '''
        获取资源路径
        :param data_type: [INDEX,SH,SZ]
        :param ktype: [day,5,finance]
        :param fqt:
        :return:
        '''
        day_path ={
            "path":"day", #文件夹名称
            "suffix":self.day_fqt
        }
        fzline_path = {
            "path": "fzline", # 五分钟
            "suffix": self.fzline_fqt
        }
        finance_path={
            "path": "finance",  # 三大财报
            "suffix":self.finance_fqt
        }
        data_path_dict = {
            "INDEX":{
                "path":"INDEX",
                "D":day_path,
                "5":fzline_path
            },
            "SH":{
                "path": "SH",
                "D":day_path,
                "5":fzline_path,
                "finance":finance_path
            },
            "SZ":{
                "path": "SZ",
                "D":day_path,
                "5":fzline_path,
                "finance":finance_path
            }
        }
        path_1 = data_path_dict[data_type]
        path_2 = path_1[ktype]
        path_3 = path_2["suffix"]
        return os.path.join(self.RootPath,path_1["path"],path_2["path"],code+'.'+path_3[fqt])

    def get_hist_data(self,code,start,end='',fqt="0",ktype='D'):#ktype只有 D:日数据 5:5分钟
        '''行情数据'''
        data_type = self._get_market(code)#SH SZ
        file_path = self._get_data_path(data_type,ktype,fqt,code)
        return self._do_something_data(file_path,start,end)

    def income(self, code, start, end=''):
        '''
        非金融利润表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end,"1001")

    def cashflow(self, code, start, end=''):
        '''
        非金融现金表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end, "1002")

    def balancesheet(self, code, start, end=''):
        '''
        非金融资产负债表数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        data_type = self._get_market(code)
        file_path = self._get_data_path(data_type, "finance", "0", code)
        return self._do_something_data(file_path, start, end, "1003")

    def get_index(self, code,start,end='',fqt="0",ktype='D'):
        '''
        指数数据
        :param code:
        :param start:
        :param end:
        :return:
        '''
        file_path = self._get_data_path("INDEX", ktype, fqt, code)
        return self._do_something_data(file_path, start, end)

    def get_stockIndex_data(self,code,base_code,start,end='',fqt="0",ktype='D',bFillNA=False):
        '''
        指数股票数据
        :param code:
        :param base_code:
        :param start:
        :param end:
        :param fqt:
        :param ktype:
        :param bFillNA: 是否处理None值
        :return:
        '''
        k_data = self.get_hist_data(code,start,end,fqt,ktype)#拿到行情数据，包括日数据或5分钟数据
        index_data = self.get_index(base_code,start,end,fqt,ktype)#读指数文件数据 body
        base_stock_data = index_data.loc[:, ['date', 'close']] #只拿出指数的时间、收盘价
        base_stock_data.rename(columns={'close': 'base_close'}, inplace=True)#改列名
        #相当于行情数据跟指数数据以date做join 效果是在行情数据加一列base_close
        result = pd.concat([k_data.set_index('date'), base_stock_data.set_index('date')], axis=1).reset_index()

        if (bFillNA):
            result = result.fillna(axis=0, method='ffill')#axis=0 单元格为None则用上一行同一列数据填充；axis=1 单元格为None则用前一列同一行数据填充

        result = result.dropna(axis=0, how='any')#只要行内有单元格值为None则去掉该行
        result.reset_index(drop=True, inplace=True)#重置行号
        result.rename(columns={'index': 'date'}, inplace=True)#把date列名改成index
        if (len(result) <= 0):
            return pd.DataFrame()
        return result

    def change_field_code(self,oldFieldName,newFieldName,classCode=None,className=None,tableName=None):
        '''
        变更本地编码字段别名
        :param oldFieldName:
        :param newFieldName:
        :param classCode:
        :param className:
        :param tableName:
        :return:
        '''
        #TableInfo TableCode有值的Table 在FieldInfo里有Code编码 TushareName->AliasName
        if classCode!=None:
            where_field="ClassCode"
            where_val=classCode
        elif className!=None:
            where_field = "ClassName"
            where_val = className
        elif tableName!=None:
            where_field = "TableName"
            where_val = tableName
        else:
            return False
        for i in ClassCodeConfig.config:
            if i[where_field] == where_val:
                for j in i["TargetUnitCode"]:
                    if j["AliasName"] == oldFieldName:
                        j["AliasName"] = newFieldName
                        ClassCodeConfig.dump_config(ClassCodeConfig.config)
                        return True



if __name__ == '__main__':
    # code_list = ["000001.sz","000002.sz","000004.sz","000005.sz","000006.sz","000007.sz","000008.sz","000009.sz",
    #              "000010.sz","000011.sz","000012.sz","000014.sz","000016.sz","000017.sz","000018.sz","000019.sz",
    #              "000020.sz","000021.sz","000023.sz","000024.sz","000025.sz","000026.sz","000027.sz","000028.sz"]
    code_list = ["000001"]
    mainclass= MainClass(r"D:\tby_svn\wta_finance\trunk\2 项目实施阶段\2.4 系统开发\2.4.1 系统实现\WtaFinancePlatform\WtaFinancePlatform_WPF\bin\x86\Debug\Data")
    System = {
        "classList":"*"
        #     [
        #     {
        #         "code": "1007",  # 大类编码
        #         "field": ["1007002","1007003","1007004"] #"*"  # "*"表示所有
        #     }
        # ]
    }
    date_time={
        "startTime": "2015-01-01 00:00:00",
        "endTime": "2021-01-01 00:00:00"
    }
    s = time.time()
    res_data = mainclass.get_data(code_list, fqt='2',date_time=None,system=None,custom=System)
    e = time.time()
    print(res_data)
    print(e-s)


