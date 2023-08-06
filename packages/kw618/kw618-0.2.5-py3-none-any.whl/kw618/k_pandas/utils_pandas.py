"""
    因为kw618的init中只能导入全局变量/函数/类, 而无法导入类中的函数.
    所以, 其实把该模块作为一个"大的类", 里面都是类中实现某些功能的函数
    所以, docs_2_df 函数, 其实没必要归纳到类中. 这样显得层级很复杂, 而且也不方便外部脚本调用该函数.
"""
import pandas as pd
import numpy as np
import math
import collections
import pymongo
import json
import copy
import hashlib
from io import StringIO

import warnings
warnings.filterwarnings("ignore")

# 导入常用的固定路径(多平台通用)
from kw618._file_path import *

def import_data(
    in_file_name="in", end_index=None, field=None, is_df=True,
    in_file_path=None, encoding="gb18030", index_col=None,
    ):
    """
    in:csv文件
    out:df类型/类mongo类型
    function:  csv → df/mongo (默认转出:类mongo)

    notes: in_file_path 的优先级比 in_file_name 高。

    ttt:0214
    """
    if in_file_path:
        df = pd.read_csv(in_file_path, encoding=encoding, engine='python', index_col=index_col)
    else:
        df = pd.read_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(in_file_name), encoding=encoding, engine='python', index_col=index_col)
    if is_df:
        return df
    # 1.需要返回的是某个字段的lst格式
    if field:
        field_lst = df[field].values[:end_index] # 得到的是np.array格式
        return list(field_lst) # 用list数据格式来返回
    # 2.返回的是mongo支持的docs
    df = df[:end_index]
    docs = df.T.to_dict().values()
    return docs



    #  也可以用于 "mongo → df"
def output_data(
    in_obj, out_file_name="out", ordered_field_lst=None,
    out_file_path=None, output=True, index=False, encoding="gb18030", export_excel=False,
    ):
    """
    in:类mongo/df
    out:csv文件
    function:  1.mongo/df  → csv
               2.mongo → df (这样output设为False即可)

    in_obj:    不管是mongo还是df,自动先转化成df,再用它来转csv

    tips: 如果需要 "mongo → df": output设置为False即可!
    notes: out_file_path 的优先级比 out_file_name 高。

    """

    # 1. 如果是 "类mongo" 类型, 先转化成df
    if isinstance(in_obj, pymongo.cursor.Cursor):
        # total_items = []
        # for doc in in_obj:
        #     # items = {i:str(j).strip() for i, j in zip(list(doc.keys()), list(doc.values()))}
        #     # 以下会按照mongo中存着的顺序进行输出!
        #     items = collections.OrderedDict({i:str(j).strip() for i, j in zip(list(doc.keys()), list(doc.values()))})
        #     total_items.append(items)
        # df = pd.DataFrame(total_items)
        df = pd.DataFrame(list(in_obj))  # 如果in_obj的数据量是上百万条, 其实这个操作很危险的!!
    elif isinstance(in_obj, pd.core.frame.DataFrame):
        df = in_obj

    # 2.确定字段的呈现顺序
    if ordered_field_lst:
        # 如果指定的df字段在df中并不存在,则把该字段remove掉.确保不报错
        for field in ordered_field_lst.copy():
            if field not in df.columns:
                print("字段 {} 不在df中,将其抛弃!".format(field))
                ordered_field_lst.remove(field)
        df = df[ordered_field_lst]  # 指定顺序

    # 3.看是否需要导出csv文件,如果不需要,直接返回df
    if not output:
        return df

    # 4. 最后,将df数据转成csv文件输出
    try:
        if out_file_path:
            if not export_excel:
                df.to_csv(out_file_path, index=index, encoding=encoding)
            else:
                df.to_excel(out_file_path, index=index, encoding=encoding)
        else:
            if not export_excel:
                df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=index, encoding=encoding)
            else:
                df.to_excel(FILE_PATH_FOR_DESKTOP+"/{0}.xlsx".format(out_file_name), index=index, encoding=encoding)
    except Exception as e:
        print(e)
        out_file_name = input("输出文件名出错,请重新键入文件名: ")
        df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=index, encoding=encoding)

    return df


# class KwPd():
#     def __init__(self):
#         pass
#
#     def docs_2_df(self, docs, ordered_field_lst=None):
#         """
#         把mongo的数据转化成df
#         """
#         df = output_data(docs, output=False, ordered_field_lst=ordered_field_lst)
#         return df



def docs_to_df(docs, ordered_field_lst=None):
    """
    把mongo的数据转化成df
    """
    df = output_data(docs, output=False, ordered_field_lst=ordered_field_lst)
    return df


def df_2_mongo(df):
    return df.T.to_dict().values() # 即：docs
def df_to_docs(df, is_lst=False):
    """
        notices:
            1. 这里传入的df的index, 应该只允许 0/1/2...999 的自然数.
                (不确定. 我把datetime对象作为index是会报错的)
            [巨坑]: 一定要注意 pd.concat([df1, df2], axis=0)的情况, 一定要加上 ignore_index=True !!!

            2. //20200812更新: 可以使用pandas自带的方法实现, 方便高效!!!
                (而且这种方式都不用担心出现上面的 判断pd.concat()中的索引重复导致转化缺失的问题)
    """
    # //20200812更新: 可以使用pandas自带的方法实现, 方便高效!!!
    # if is_lst:
    #     return list(df.T.to_dict().values())
    # else:
    #     return df.T.to_dict().values() # 即：docs

    docs = df.to_dict("records") # 高效!!
    return docs


def read_excel(in_file_name="in", in_file_path=None, sheet_name=None, need_to_concat=True):
    """
        params:
            sheet_name:
                传入None: 返回一个有序字典 OrderedDict([("<sheet名字>", <df对象>)])
                        ( 需要用sheet名来按键取值)
            need_to_concat:
                当没有指定"sheet_name"时, 默认把所有sheet合并, 返回合并后的df
                    (当need_to_concat为False时, 不自动合并sheet, 而是返回一个 'excel字典对象')
    """
    # 1. 先读取整个excel文件
    if in_file_path is not None:
        ordered_d = pd.read_excel(in_file_path, sheet_name=None)
    elif in_file_path is None:
        ordered_d = pd.read_excel(f"{FILE_PATH_FOR_DESKTOP}/{in_file_name}.xlsx", sheet_name=None)

    # 2. 读取对应sheet_name (返回df)
    if sheet_name != None:
        df = ordered_d.get(sheet_name)
        del ordered_d # 释放中间过程对象的内存
        return df
    # 3. 合并多个sheet, 返回合并后的df
    elif need_to_concat == True:
        concat_df = pd.concat([sheet for sheet in ordered_d.values()], axis=0, ignore_index=True)
        del ordered_d # 释放中间过程对象的内存
        return concat_df

    # 4. 返回这个excel字典对象 (每个键值对中, 以sheet的名字作为"键", 对应的df对象作为"值")
    return ordered_d


def sort_df(df, ordered_field_lst):
    # 1. 如果指定的字段在df中并不存在,则把该字段remove掉.确保不报错
    ordered_field_lst_copy = ordered_field_lst.copy()
    for field in ordered_field_lst_copy:
        if field not in df.columns:
            print("字段 {} 不在df中, 将其抛弃!".format(field))
            ordered_field_lst.remove(field)

    # 2. 把所需要保留的 "有序字段list" 作用在df上
    return df[ordered_field_lst]  # 指定顺序




# stackoverflow 白嫖来的函数，hhh
def read_mongo(collection_obj, query={}, need_to_show_dict={}, df_name="foo", need_to_convert_date=True):
    """
        params:
            need_to_convert_date: 是否需要在读取mongo数据的时候, 转化日期格式
        note: 白嫖来的函数, hhh

    """

    # 不需要获取"_id"字段
    need_to_show_dict.update({"_id":0})

    # Make a query to the specific DB and Collection
    # print(query, need_to_show_dict)
    cursor = collection_obj.find(query, need_to_show_dict)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    df.df_name = df_name


    if ("crawl_date" in df.columns) and (need_to_convert_date==True):
        df["crawl_date"] = pd.to_datetime(df["crawl_date"])
    if ("date" in df.columns) and (need_to_convert_date==True):
        df["date"] = pd.to_datetime(df["date"])

    return df





def date_to_obj(date_str="today"):
    return pd.to_datetime(date_str)

def obj_to_date(date_obj, format_="%Y-%m-%d"):
    return date_obj.strftime(format_)

def get_today_obj(date_str="today"):
    return pd.to_datetime(date_str)

def get_days(days_str="1 d"):
    "1天的时间段"
    return pd.to_timedelta(days_str)

def get_this_time():
    "此刻的时间"
    today_obj = pd.to_datetime("today")
    return today_obj.strftime("%X") # 转成“15:43:36”这样的str形式

def get_this_date_time():
    "此刻的时间"
    today_obj = pd.to_datetime("today")
    return today_obj.strftime("%Y-%m-%d %X") # 转成 '2020-07-29 14:13:30' 这样的str形式


def get_today_date(date_str="today", format_="%Y-%m-%d"):
    "今天的日期"
    today_obj = pd.to_datetime(date_str)
    return today_obj.strftime(format_) # 转成“2019-02-28”这样的str形式
# 简化版的当前日期
def get_sim_today_date(date_str="today"):
    return get_today_date(date_str=date_str ,format_="%m%d") # 转成“0228”这样的str形式
# 简化版的昨天日期
def get_sim_yesterday_date(date_str="today"):
    return get_yesterday_date(date_str=date_str, format_="%m%d") # 转成“0228”这样的str形式

def get_sim_this_time():
    this_time_str = get_this_time() # '03:05:49'
    return this_time_str.replace(":", "") # '030549'

def get_yesterday_obj(date_str="today"):
    today_obj = pd.to_datetime(date_str)
    yesterday_obj = today_obj - pd.to_timedelta("1 d")
    return yesterday_obj

def get_yesterday_date(date_str="today", format_="%Y-%m-%d"):
    " 昨天的日期"
    today_obj = pd.to_datetime(date_str)
    yesterday_obj = today_obj - pd.to_timedelta("1 d")
    yesterday_date = yesterday_obj.strftime(format_) # 转成“20190228”这样的str形式
    return yesterday_date

def get_previous_date(date_str="today", days_str="10 d", format_="%Y-%m-%d"):
    today_obj = pd.to_datetime(date_str)
    days_obj = get_days(days_str)
    previous_date_obj = today_obj - days_obj
    previous_date = previous_date_obj.strftime(format_)
    return previous_date

def get_later_date(date_str="today", days_str="10 d", format_="%Y-%m-%d"):
    today_obj = pd.to_datetime(date_str)
    days_obj = get_days(days_str)
    previous_date_obj = today_obj + days_obj
    previous_date = previous_date_obj.strftime(format_)
    return previous_date



def get_this_month_first_date(date_str="today"):
    " 本月第一天的日期"
    today_obj = get_today_obj(date_str)
    this_month_first_obj = get_today_obj(today_obj.strftime("%Y-%m"))
    this_month_first_date = obj_to_date(this_month_first_obj)
    return this_month_first_date


def get_delta_days(start_date=get_yesterday_date(), end_date=get_today_date()):
    start_date_obj = get_today_obj(date_str=start_date)
    end_date_obj = get_today_obj(date_str=end_date)
    delta_days = (end_date_obj - start_date_obj).days
    return delta_days


def get_period_df(start_date=None, end_date=None, is_crawl_date=False):
    " 获取一段时间内的 <日期扩充表> "
    if start_date is None:
        this_month_first_date = get_this_month_first_date()
        start_date = this_month_first_date
    if end_date is None:
        end_date = get_today_date()

    # 两种方式截取 "日期范围"
    datetime_index = pd.date_range(start_date, end_date, freq="1d")
    if is_crawl_date: # 用"crawl_date"来选择 "日期范围"
        df = pd.DataFrame({"crawl_date":datetime_index})
        df["true_date"] = df.crawl_date - get_days("1 d")
    else: # 用"true_date"来选择 "日期范围"
        df = pd.DataFrame({"true_date":datetime_index})
        df["crawl_date"] = df.true_date + get_days("1 d")

    # 生成4中 str格式的日期  (用于后期透视)
    df["日期"] = df.true_date.dt.strftime("%Y-%m-%d")
    df["日期-年"] = df.true_date.dt.strftime("%Y") # series类型正常来说是不能直接strftime成str类型的, 必须要用.dt 方法才行
    df["日期-月"] = df.true_date.dt.strftime("%Y-%m")
    # 计算"日期-周"这个 '周度日期 '
    weekly_date_lst = []
    for count, date_str in enumerate(df["日期"][-1::-1]): # 对'日期'的series逆序
        if count % 7 == 0:
            tmp = date_str
        weekly_date_lst.append(tmp)
    df["日期-周"] = weekly_date_lst[-1::-1] # 上面逆序了, 现在逆序回来
    df["sim_true_date"] = df.true_date.dt.strftime("%m%d")
    df["sim_crawl_date"] = df.crawl_date.dt.strftime("%m%d")

    return df





def output_excel(df_lst, out_file_name="out", out_file_path=None, sheet_name_lst=None):
    from pandas import ExcelWriter
    if out_file_path is None:
        # 如果没有out_file_path: 默认放在桌面
        out_file_path = f"{FILE_PATH_FOR_DESKTOP}/{out_file_name}.xlsx"
    with ExcelWriter(out_file_path) as writer:
        for i, df in enumerate(df_lst):
            if sheet_name_lst:
                sheet_name = sheet_name_lst[i]
            else:
                sheet_name = f"sheet_{i}"
            df.to_excel(writer, sheet_name, index=False)
        writer.save()















def avg(lst):
    if isinstance(lst, list):
        if len(lst) <1:
            # raise myError("元素小于1!")
            return 0
    elif isinstance(lst, type(pd.Series())):
        if lst.size <1:
            # raise myError("元素小于1!")
            return 0
    sum = 0
    for count, e in enumerate(lst):
        # print(count, e)
        sum += int(float(e))
    lst_avg = sum/(count+1)
    # print(lst_avg)
    return int(lst_avg)


def merge_df(
    x_name, y_name, out_file_name="out",
    is_df=None, join_field="house_id", output=True):
    """
    function: 不仅可以合并df/csv, 还附带输出csv的功能
    """
    print(">>>1")
    if not is_df:
        # 如果 不是df， 就把这个当做文件名，导入
        x_df = import_data(x_name, is_df=True)
        y_df = import_data(y_name, is_df=True)
    else:
        # 如果 是df， 就直接把传入的x、y当做 df对象来使用
        x_df = x_name
        y_df = y_name
    print(">>>2")
    # pd.merge() 返回的不是df类型，而是function类型。 但这个function可以使用to_csv导出文件
    #  ??????   什么情况？ 之前测试的时候返回的不是df对象，现在测试发现又确实是df对象了。。。见鬼！
    merged_df = pd.merge(x_df, y_df, how="left", on=join_field)
    if not output:
        return merged_df
    print(">>>3")
    merged_df.to_csv(FILE_PATH_FOR_DESKTOP+"/{0}.csv".format(out_file_name), index=False, encoding="gb18030")
    print("合并成功!")

# merge_df("aaa", "bbb", out_file_name="zzzz")
# exit()


# def k_top(lst, top=1):
#     if isinstance(lst, list):
#         if len(lst) <1:
#             # raise myError("元素小于1!")
#             return 0
#     elif isinstance(lst, type(pd.Series())):
#         if lst.size <1:
#             # raise myError("元素小于1!")
#             return 0
#
#     lst = sorted(lst)
#     return lst[top-1]


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for np types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)










def k_divide(lst, piece=5):
    """
    function: 按lst从小到大的顺序, 等分成piece份 小lst 返回
    return: 返回等分节点的lst (即:按照这几个值去截取, 就是5等分了)
    """
    if isinstance(lst, list):
        if len(lst) <1:
            # raise myError("元素小于1!")
            return 0
    elif isinstance(lst, type(pd.Series())):
        if lst.size <1:
            # raise myError("元素小于1!")
            return 0

    lst = sorted(lst)
    # 1. 打印原lst
    print(lst)
    node_order_lst = []
    node_lst = []
    for count in range(1, piece):
        node_order_value = round(len(lst) * (1/piece) * count) - 1 # 减一别忘了 (另外,这里返回的是顺序值,不是真实值)
        node_order_lst.append(node_order_value)
        node_lst.append(lst[node_order_value])
    # 2. 打印分好piece后的, 节点的顺序
    print(node_order_lst) # 是顺序
    print("值的lst: {}".format(node_lst)) # 是值

    piece_dict = {}
    count = 0
    while True:
        if count == piece:
            break
        elif count == 0:
            piece_dict.update({count+1 : lst[ : node_order_lst[count]+1]})
        elif count == piece-1:
            piece_dict.update({count+1 : lst[node_order_lst[count-1]+1 : ]})
        else:
            piece_dict.update({count+1 : lst[node_order_lst[count-1]+1 : node_order_lst[count]+1]})
        count += 1
    # 3. 打印根据上面的顺序, piece等拆分了lst后的dict
    print(piece_dict)
    return node_lst
    # return piece_dict


    # piece_lst = [] count = 0
    # while True:
    #     if count == piece:
    #         break
    #     elif count == 0:
    #         piece_lst.append(lst[ : node_order_lst[count]+1])
    #     elif count == piece-1:
    #         piece_lst.append(lst[node_order_lst[count-1]+1 : ])
    #     else:
    #         piece_lst.append(lst[node_order_lst[count-1]+1 : node_order_lst[count]+1])
    #     count += 1
    # # 3. 打印根据上面的顺序, piece等拆分了lst后的lst
    # print(piece_lst)
    # return piece_lst

# k_divide([3, 4, 5, 7, 2, 4, 46, 6, 7, 84, 4,5], 5)




def is_notnan_numeric(x):
    """
        numeric: 指所有数值: int/float (包括np.nan) (不包括None) (不包括'可以转成float的str')
        notnan_numeric: 指所有'非nan'的数值: int/float (不包括np.nan, 不包括None)
    """
    # 1. 若是数据集, 则直接返回False
    if isinstance(x, list) or isinstance(x, dict) or isinstance(x, set) or isinstance(x, tuple) or isinstance(x, np.ndarray):
        return False
    # 2. 是否为 None
    if x is None:
        return False
    # 3. 是否为 np.nan
    elif pd.isnull(x):
        return False
    # 4. 是否为 str
    elif isinstance(x, str):
        ### 注意: 这里防止x为可以被转成float的str, 先对str类型单独处理 (避免下一步造成错误判断)
        return False
    else:
        try:
            # 4. 如果可以被float()转化成float, 则x是为数值型, 返回True
            return isinstance(float(x), float)
        except:
            # 5. 不能转化, 则说明不是数值型
            return False


def safely_to_int(x, need_to_print=False):
    """
        save: 表示可以'安全'转化成'int'. 如果x为不能转化成int的数据, 则保留原样
        notice: 该函数是以'四舍五入'的方式转成int
    """
    # 如果是'非nan数值型', 则直接round()
    if is_notnan_numeric(x):
        ### 为了保证转成int, 需要先四舍五入, 再转成int
        ### 注意: 如果x=np.float(3.5000) , round(x, 0)  >>> 4.0 (还是会带个小数点,很烦,所以干脆转成int是最省心/最干净的)
        return int(round(x, 0))
    # 否则: 原样return回去
    else:
        if need_to_print:
            print(f"x: {x}, 类型为: {type(x)}, 不能保留整数!\n")
        return x







def round_df(df, round_digit=0, inplace=False, included_columns=[], excluded_columns=[]):
    """
        params:
            round_digit: 保留的小数位数
            inplace: 是否在原df上操作?
            excluded_columns: 排除某些不需要转化的列
            included_columns: 只有这些列 需要被转化


        默认:
            1. 四舍五入到整数
            2. 列名为"xx率"的, 一律以附带"百分号", 以str的形式呈现
    """
    if inplace is False:
        df = copy.deepcopy(df)

    for column, dtype in df.dtypes.items():
        # 1. 有些'率'是需要转化成'百分数'的
        if "率" in column:
            df[column] = df[column].apply(lambda x: format(x, ".2%"))
        # 2. 若发现df中的某列是 int型或者float型, 则按照round_digit四舍五入
        else:
            # 1. 当仅仅需要某几个列需要转化时:
            if included_columns:
                if column in included_columns:
                    if dtype == np.dtype(np.float64) or dtype == np.dtype(np.int64):
                        df[column] = df[column].round(round_digit)
            # 2. 当某几个列 一定不能转化时:
            elif excluded_columns:
                if column not in excluded_columns: # 只有'不被排除列'才需要保留两位小数
                    if dtype == np.dtype(np.float64) or dtype == np.dtype(np.int64):
                        df[column] = df[column].round(round_digit)
            # 3. 当都没有限制条件时:
            else:
                if dtype == np.dtype(np.float64) or dtype == np.dtype(np.int64):
                    df[column] = df[column].round(round_digit)
    return df



def get_random_num():
    "获取一个 [0.0, 1.0) 的随机数"
    return np.random.rand(1)[0]


def get_random_df(df):
    "对df的每一行打乱顺序"
    random_df = pd.DataFrame(np.random.permutation(df), columns=df.columns)
    return random_df



def k_md5(s: str):
    """
        function: 获取md5哈希编码后的值;
        输入类型: 必须为str (因为需要encode, 其他类型都不能encode)
        返回类型: 为str
        notes: md5是不可逆的加密 (不属于对称加密和非对称加密)
    """
    if isinstance(s, str) is False:
        raise Exception("[error]: 输入类型不是str\n")
    MD5 = hashlib.md5()
    MD5.update(s.encode("utf-8"))
    encrypted_s = MD5.hexdigest()
    print(f"加密后的值为: {encrypted_s}\n")
    return encrypted_s

def k_sha256(s: str):
    """
        function: 获取sha256哈希编码后的值;
        输入类型: 必须为str (因为需要encode, 其他类型都不能encode)
        返回类型: 为str
        notes: sha256是不可逆的加密 (不属于对称加密和非对称加密)

        (方法与上面的md5基本一样..)
    """
    if isinstance(s, str) is False:
        raise Exception("[error]: 输入类型不是str\n")
    SHA256 = hashlib.sha256()
    SHA256.update(s.encode("utf-8"))
    encrypted_s = SHA256.hexdigest()
    print(f"加密后的值为: {encrypted_s}\n")
    return encrypted_s


def k_hmac_sha256(key, data):
    """
    (网上白嫖来的方法)
        function: 根据 hmac sha256 算法, 使用 key 作为密钥, 对 data 进行加密 (应该是包含了哈希加密和对称加密两部分)
                (应该是比单纯的sha256更安全?)
        params:
            key: 密钥
            data: 需要加密的数据
        return: 加密后的数据
    """

    import hmac
    data = data.encode('utf-8')
    encrypted_data = hmac.new(key.encode('utf-8'), data, digestmod=hashlib.sha256).hexdigest().upper()
    print(f"\n\n加密后的数据: {encrypted_data}\n\n")
    return encrypted_data


def get_binance_sign(secret_key, ori_params):
    """
        function: 生成币安的签名
        params:
            secret_key: 使用 SECRETKEY 作为密钥
            ori_params: str格式的'原请求参数'
        return: str格式的'签名'
    """
    signature = k_hmac_sha256(key=secret_key, data=ori_params)
    print(f"\n\n该请求的币安签名为: {signature}\n\n")
    return signature


def create_encrypted_cookie(key: str, salt="618"):
    "通过加盐, 加时间数, 加随机数, 获得一个md5加密后的随机cookies (其实也没必要加密,只是用于记录登录状态,并没有其他作用)"
    "应用场景: 服务端记录这个哈希值, 用于验证浏览器的30分钟有效登录"
    s = key + salt + get_sim_this_time() + str(np.random.randint(10, 1000000))
    encrypted_s = k_md5(s)
    return encrypted_s





def kplot(df, kind="line"):
    """
        params:
            kind:
                line: 折线图
                bar: 条形图📊 (竖直型, 如左图标) [index上的索引, 就代表的是坐标轴上的标签]
                barh: 条形图 (水平型)
                hist: 直方图 (每个值的频率图) (类似于曝光直方图)
                pie: 饼状图

        todo:
            1. 如何对df中的某一列, 标注红色, 且加粗?? (其他设置成灰色/浅色虚线?)

    """
    import matplotlib.pyplot as plt
    plt.figure()
    df.plot()
    plt.show()








if __name__ == '__main__':
    print("start!")
    df = import_data("业务反馈调价", is_df=True)
    print(df)
    print(df.shape)
    print("end!")
