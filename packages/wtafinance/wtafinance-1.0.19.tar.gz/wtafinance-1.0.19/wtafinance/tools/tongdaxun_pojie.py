import struct,math,time


class PoJie():
    def ByteToHex(self,bins):
        return ''.join(["%02X" % x for x in bins]).strip()

    def HexToByte(self,hexStr):
        return bytes.fromhex(hexStr)

    def sum_str(self,data):
        s = ""
        for i in data:
            s += i
        return s

    def reverse_list(self,data):
        data.reverse()
        return data

    def hex_to_float(self,h):
        i = int(h, 16)
        return struct.unpack('<f', struct.pack('<I', i))[0]

    def float_to_hex(self,f):
        return struct.unpack('>I',struct.pack('>f', f))[0]


    def hex_to_int(self,h):
        i = int(h, 16)
        return i

    def int_to_hex(self,i):
        h = hex(i)
        return h

    def pojie_day(self,file):
        f = open(file, 'rb')
        n = 0
        s = f.read(1)
        total_list = []
        while s:
            byte = ord(s)
            n = n + 1
            total_list.append('%02x' % (byte))
            s = f.read(1)
        f.close()

        # total_cls_list= [[total_list[k:k + 4] for k in range(0, len(total_list[i:i+32]), 4)] for i in range(0, len(total_list), 32)]
        total_cls_list = [total_list[i:i + 32] for i in range(0, len(total_list), 32)]
        total_cls_list_list = [[total_cls_list[i][k:k + 4] for k in range(0, len(total_cls_list[i]), 4)] for i in
                               range(0, len(total_cls_list))]
        # print(total_cls_list_list[:2])
        for i in total_cls_list_list[-10:]:
            for k in range(0, len(i)):
                if k == 0:
                    # 时间
                    print('时间', round(self.hex_to_int(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 1:
                    # 开盘价
                    print('开盘价', round(self.hex_to_int(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 2:
                    # 最高价
                    print('最高价', round(self.hex_to_int(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 3:
                    # 最低价
                    print('最低价', round(self.hex_to_int(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 4:
                    # 收盘价
                    print('收盘价', round(self.hex_to_int(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 5:
                    # 成交额
                    print('成交额', self.hex_to_float(self.sum_str(self.reverse_list(i[k]))))
                elif k == 6:
                    # 成交量
                    print('成交量', self.hex_to_int(self.sum_str(self.reverse_list(i[k]))))
            print("")

    def pojie_lcl(self,file):
        f = open(file, 'rb')
        n = 0
        s = f.read(1)
        total_list = []
        while s:
            byte = ord(s)
            n = n + 1
            total_list.append('%02x' % (byte))
            s = f.read(1)
        f.close()

        # total_cls_list= [[total_list[k:k + 4] for k in range(0, len(total_list[i:i+32]), 4)] for i in range(0, len(total_list), 32)]
        total_cls_list = [total_list[i:i + 32] for i in range(0, len(total_list), 32)]
        total_cls_list_list = [[total_cls_list[i][k:k + 4] for k in range(0, len(total_cls_list[i]), 4)] for i in
                               range(0, len(total_cls_list))]
        for i in total_cls_list_list[-10:]:
            for k in range(0, len(i)):
                if k == 0:
                    # 时间
                    date = self.reverse_list(i[k])
                    date_1 = date[:2]  # 分时
                    date_2 = date[2:]  # 年月日
                    num = self.hex_to_int(self.sum_str(date_2))
                    year = math.floor(num / 2048) + 2004
                    month = math.floor((num % 2048) / 100)
                    day = (num % 2048) % 100
                    minute = self.hex_to_int(self.sum_str(date_1))
                    match_time = '{year}-{month}-{day} 00:00:00'.format(year=year, month=str(month).rjust(2, '0'),
                                                                        day=str(day).rjust(2, '0'))
                    ans_time_stamp = time.mktime(time.strptime(match_time, "%Y-%m-%d %H:%M:%S"))
                    struct_time = time.localtime(ans_time_stamp + minute * 60)  # 得到结构化时间格式
                    print(time.strftime("%Y-%m-%d %H:%M:%S", struct_time))
                elif k == 1:
                    # 开盘价
                    print('开盘价', round(self.hex_to_float(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 2:
                    # 最高价
                    print('最高价', round(self.hex_to_float(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 3:
                    # 最低价
                    print('最低价', round(self.hex_to_float(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 4:
                    # 收盘价
                    print('收盘价', round(self.hex_to_float(self.sum_str(self.reverse_list(i[k]))), 3))
                elif k == 5:
                    # 成交额
                    print('成交额', self.hex_to_float(self.sum_str(self.reverse_list(i[k]))))
                elif k == 6:
                    # 成交量
                    print('成交量', self.hex_to_int(self.sum_str(self.reverse_list(i[k]))))

    def encode_file(self,file):
        data = 1024.09
        s = self.float_to_hex(data)
        print(s)
        data = hex(s)
        print(data)
        hex_data = [int(data[i:i + 2], 16) for i in range(2, len(data), 2)]

        print(hex_data)

        with open(file, "bw") as f:
            for i in poejie.reverse_list(hex_data):
                f.write(struct.pack('B', i))


if __name__ == '__main__':
    poejie = PoJie()
    # # # pojie_lcl(r"D:\微信\WeChat\WeChat Files\wxid_uujfb1g007pq21\FileStorage\File\2020-07\sh600101.lc1")
    # poejie.pojie_day(r"D:\TDX\vipdoc\sh\lday\sh600100.day")

    s = struct.unpack('>I',struct.pack('>f', 1024.09))
    print(s)
    data = hex(s[0])
    print(data)
    hex_data = [int(data[i:i+2],16) for i in range(2,len(data),2)]

    print(hex_data)


    with open("./day.aaa","bw") as f:
        for i in poejie.reverse_list(hex_data):
            f.write(struct.pack('B',i))






