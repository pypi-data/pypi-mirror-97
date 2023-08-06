import json
import pandas as pd


# 导入常用的固定路径(多平台通用)
from kw618._file_path import *
# 本脚本依赖很多 utils_requests的函数和模块, 直接用*  (注意要避免循环导入问题)
from kw618.k_requests.utils_requests import *
from kw618.k_requests.ocr import *
from kw618.k_python.utils_python import *
from kw618.k_pandas.utils_pandas import *

from kw618.k_finance.const import ulist_change_name_dict, A_Zqmc_lst, ETF_Zqmc_lst

req = myRequest().req
client = pymongo.MongoClient(f'mongodb://kerwin:kw618@{HOST}:27017/')
db_for_quant = client["quant"]
remote_client = pymongo.MongoClient(f'mongodb://kerwin:kw618@{REMOTE_HOST}:27017/')
remote_db_for_quant = remote_client["quant"]


def show_formatted_df(df):
    """
        function: 当需要输出打印时, 可以呈现地'更加人性化' (便于人眼观看)
                    (比如: 把JRZF中的浮点小数, 用'百分号'的形式呈现. 但底层的数据仍是浮点型, 不影响后期调用时的数据处理)
    """
    copied_df = deepcopy(df)
    if "JRZF" in copied_df.columns:
        copied_df["JRZF"] = copied_df["JRZF"].apply(lambda x: format(x, ".2%"))
    if "Ykbl" in copied_df.columns:
        copied_df["Ykbl"] = copied_df["Ykbl"].astype("float").apply(lambda x: format(x, ".2%"))
        #当日晚上8点以后, 东财会把Dryk数据清零, 变成''空字符串, 所以这里强行转成float会报错. (而当df为空df时, 反倒不会报错.因为根本没有值传进去)
    if "Drykbl" in copied_df.columns:
        copied_df["Drykbl"] = copied_df["Drykbl"].astype("float").apply(lambda x: format(x, ".2%"))
    if "CcsLjykbl" in copied_df.columns:
        copied_df["CcsLjykbl"] = copied_df["CcsLjykbl"].astype("float").apply(lambda x: format(x, ".2%"))
    if "ROA" in copied_df.columns:
        copied_df["ROA"] = copied_df["ROA"].astype("float").apply(lambda x: format(x, ".2%"))


    print(copied_df) # 自带打印功能





class ReqStockData():
    """
        function: 专门获取数据的类 (爬虫类)

        类组件函数:
            1. 私有函数:
                - Zqdm <===互换===> stock_code
                - Zqdm ==========> 得到f1的值  (2:A股, 3:ETF基金)
                - Zqmc ==========> stock_code  ("大康农业" ---> "0.002505")
            2. req: (请求数据)
                - req_hist_data   (历史所有数据)
                - req_trend_data  (今日分时数据)
                - req_newest_data (所有股票的最新价格)(单条)
                - req_index       (获取大盘指数)
                - req_my_stock    (获取指定zx的stock)
                - live            (调用req_my_stock函数, 获取指定zx的stock) (10s刷新频率)
            3. store: (存储数据)
                - store_hist_allstock        (存储所有A股&ETF的'历史价格数据')
                - store_hist_zxstock        (存储zx的stock的'历史价格数据')
                - store_hist_index           (存储所有大盘指数的'历史价格数据')
                - store_trend_zxstock        (存储zx的stock的'今日分时数据')
                - store_newest_allstock      (存储所有A股&ETF的'当前最新价格') (批量存)(实际也就一个req就得到了)
            4. get: (在'mongo取数'或者'内存计算' 等)
                - get_A_df  # 好像使用场景不多, 暂不实现 (f1=2)
                - get_ETF_df # 好像使用场景不多, 暂不实现 (f1=3)
                - merge_Zqmc # 把原有'隐晦'的Zqdm, 直接匹配上'显式'的Zqmc
            5. overview: (总览数据)
                - overview_asset     (记录个人每日的ROA)
                - overview_deal      (记录每只股的总盈亏)
    """

    def __init__(self, host="local"):
        # 默认的host是用"本地的"
        if host == "local":
            self.db = db_for_quant
        elif host == "remote":
            self.db = remote_db_for_quant



    def _Zqdm_to_StockCode(self, Zqdm_lst):
        """
            function: 把 002505 转变成 0.002505  的形式
                        (即: 'sim_stock_code' --> 'stock_code')
            # TODO: 当输入159915这类ETF的Zqdm时候, 在mongo数据中就找不到了..... (有点坑, 想想办法....) (已经实现)
        """
        # Zqdm_lst = ["002505", "000002", "600002"]
        df = read_mongo(
            self.db["newest_allstock"],
            query={"Zqdm":{"$in":Zqdm_lst}},
            need_to_show_dict={"Zqdm":1, "stock_code":1}
        )
        print(df)
        stock_code_lst = list(df["stock_code"])
        return stock_code_lst
    def _StockCode_to_Zqdm(self, stock_code_lst):
        """
            function: 把 0.002505 转变成 002505  的形式
                        (即: 'stock_code' --> 'sim_stock_code')
        """
        # stock_code_lst = ["0.002505", "0.000002", "1.600002"]
        lst = []
        for stock_code in stock_code_lst:
            sim_stock_code = stock_code[2:]
            lst.append(sim_stock_code)
        print(lst)
        return lst
    def _Zqdm_to_Zqmc(self, Zqdm_lst):
        # Zqdm_lst = ["002505", "000002", "600002"]
        df = read_mongo(
            self.db["newest_allstock"],
            query={"Zqdm":{"$in":Zqdm_lst}},
            need_to_show_dict={"Zqdm":1, "Zqmc":1}
        )
        print(df)
        Zqmc_lst = list(df["Zqmc"])
        return Zqmc_lst

    def _Zqdm_to_f1(self, Zqdm_lst):
        """
            function: 输入 002505 得到 f1=2;  输入 159902 得到 f1=3;
                        (即: 'Zqdm' --> 'f1')
        """
        # Zqdm_lst = ["002505", "000002", "600002"]
        df = read_mongo(
            self.db["newest_allstock"],
            query={"Zqdm":{"$in":Zqdm_lst}},
            need_to_show_dict={"Zqdm":1, "f1":1}
        )
        print(df)
        stock_code_lst = list(df["f1"])
        return stock_code_lst


    def _store_ETF_launch_date(self):
        """
            function: 存入每个ETF基金的上市日期 (不常用)
                        (更新频次: 年)
                        (因为 store_newest_allstock 中无法获取到ETF的上市日期, 所以使用了'歪招'....)
                            # 歪招: 从 hist_allstock 中获取每个ETF的第一条数据, 这条数据中的日期就是这个ETF的'上市日期'
        """

        ETF_df = Q.get_ETF_df()
        docs = df_to_docs(ETF_df)
        for doc in docs:
            stock_code = doc.get("stock_code")
            launch_date_dict = self.db["hist_allstock"].find_one({"stock_code":stock_code})
            if launch_date_dict:
                launch_date = launch_date_dict.get("market_date")
                update_dic = {"stock_code":stock_code, "上市日期":launch_date}
                self.db["newest_allstock"].update_one({"stock_code":stock_code}, {"$set":update_dic}, upsert=True)
        print(f"所有ETF的上市日期已经成功存储...")

    def Zqmc_to_stock_code(self, Zqmc_lst=["大康农业"]):
        df = read_mongo(
            self.db["newest_allstock"],
            query={"Zqmc":{"$in":Zqmc_lst}},
            need_to_show_dict={"Zqmc":1, "stock_code":1}
        )
        print(df)
        stock_code_lst = list(df["stock_code"])
        return stock_code_lst
    def Zqmc_to_Zqdm(self, Zqmc_lst=["大康农业"]):
        df = read_mongo(
            self.db["newest_allstock"],
            query={"Zqmc":{"$in":Zqmc_lst}},
            need_to_show_dict={"Zqmc":1, "Zqdm":1}
        )
        print(df)
        stock_code_lst = list(df["Zqdm"])
        return stock_code_lst


    def req_hist_data(self, stock_code="0.002505", period=30, pt=True, beg="0", end="20500000"):
        """
            function: 从'xxxx'获取xxxx
            params:
                stock_code: stock代码
                period: 区间 (0代表全部区间) (其他任意整数表示: 从今天开始往回取x天)
                beg: DC接口中指定的'开始日期'参数 (包含当日) # 20200722  (非标准时间格式)
                end: DC接口中指定的'结束日期'参数 (包含当日) # 20200803  (非标准时间格式)
                pt: 是否格式化打印输出

        """
        # 1. 请求数据
            # beg:0(开始日期); end:20500101(结束日期);  lmt:120(限制呈现的天数)
        url = (
            "http://push2his.eastmoney.com/api/qt/stock/kline/get"
            "?fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf61&klt=101&fqt=1"
            f"&secid={stock_code}&beg={beg}&end={end}"
        )
        j = req(url)
        # 2. 把结果转化成可处理的df
        d = json.loads(j)
        all_stock_data = d.get("data", {})
        k_lines_lst = all_stock_data.get("klines", [])
        k_lines_lst = [k_info_str.split(",") for k_info_str in k_lines_lst]
        df = pd.DataFrame(
            k_lines_lst, columns=[
                "market_date", "start_price", "end_price", "max_price", "min_price",
                "trading_volumn", "trading_money", "swing_rate", "turnover_rate"
                ],
            dtype="float64",
            )
        df["market_date"] = pd.to_datetime(df["market_date"])
        start_index = -period -100 if period else 0 # note: 这里-100是为了方便后面计算30日移动平均值
        df = df[start_index:]
        # 3. 处理数据
            # df: 源数据
            # k_lines_df: 历史完整的"k线图"数据df
            # growth_df: 增量/增幅的df (使用shift平移)
            # rolling_df: 移动平均的df (使用rolling平移/求均值)
            # show_df: 最终呈现的df (方便我查看走势的)
        k_lines_df = df.set_index("market_date")

        s = k_lines_df["end_price"]
        growth_amount = s-s.shift(1)
        growth_rate = growth_amount / s.shift(1)
        growth_df = pd.DataFrame({"growth_amount":growth_amount, "growth_rate":growth_rate})

        s1 = df["end_price"].rolling(5).mean()
        s2 = df["end_price"].rolling(10).mean()
        s3 = df["end_price"].rolling(20).mean()
        s4 = df["end_price"].rolling(30).mean()
        rolling_df = pd.DataFrame({"market_date":k_lines_df.index, "5d_avg":s1, "10d_avg":s2, "20d_avg":s3, "30d_avg":s4})
        rolling_df["market_date"] = pd.to_datetime(rolling_df["market_date"])
        rolling_df = rolling_df.set_index("market_date")

        show_df = pd.concat([k_lines_df[["end_price"]], growth_df, rolling_df], axis=1)
        show_df = round_df(show_df[-period:], 3) # 取3位小数
        if pt == True:
            print(f"\n\n\n代码 - {stock_code} - '历史数据' 如下:")
            print(show_df)
        return show_df


    # req爬取'任一个股(包括ETF)的分时数据'
    def req_trend_data(self, stock_code="0.002505", period=0, pt=True):
        """
            function: 从'xxxx'获取xxxx
        """
        sprint(stock_code=stock_code)
        # 1. 请求数据
        url = ("http://push2.eastmoney.com/api/qt/stock/trends2/get"
                "?fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11%2Cf12%2Cf13"
                "&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58"
                f"&secid={stock_code}&&ut=e1e6871893c6386c5ff6967026016627"
                )
        j = req(url)
        # 2. 把结果转化成可处理的df
        d = json.loads(j)
        all_stock_data = d.get("data", {})
        trends_lst = all_stock_data.get("trends", [])
        trends_lst = [trends_info_str.split(",") for trends_info_str in trends_lst]
        df = pd.DataFrame(
            trends_lst, columns=[
                "market_date_time", "start_price", "end_price", "max_price", "min_price",
                "trading_volumn", "trading_money", "avg_price???"
                ],
            dtype="float64",
            )
        df["market_date_time"] = pd.to_datetime(df["market_date_time"])
        opening_price = df["end_price"].iloc[0] if len(df["end_price"]) else None # 开盘价格 (实际上是9:15集合竞价的价格)

        start_index = -period -100 if period else 0 # note: 这里-100是为了方便后面计算30日移动平均值
        df = df[start_index:]
        # 3. 处理数据
            # df: 源数据
            # trends_df: 今天的"分时图"数据df
            # growth_df: 增量/增幅的df (使用shift平移)
            # rolling_df: 移动平均的df (使用rolling平移/求均值)
            # show_df: 最终呈现的df (方便我查看走势的)
        trends_df = df.set_index("market_date_time")
        end_price_ss = trends_df["end_price"]
        if opening_price:
            today_growth_rate_ss = end_price_ss/opening_price -1 # 数据类型为:float
            growth_amount_ss = end_price_ss-end_price_ss.shift(1)
            growth_rate_ss = growth_amount_ss / end_price_ss.shift(1)
            growth_df = pd.DataFrame({"end_price":end_price_ss, "JRZF":today_growth_rate_ss, "growth_amount":growth_amount_ss, "growth_rate":growth_rate_ss})
            growth_df.insert(0, "stock_code", stock_code)

            ss1 = end_price_ss.rolling(5).mean()
            ss2 = end_price_ss.rolling(10).mean()
            ss3 = end_price_ss.rolling(20).mean()
            ss4 = end_price_ss.rolling(30).mean()
            ss5 = end_price_ss.rolling(60).mean()
            rolling_df = pd.DataFrame({"market_date_time":trends_df.index, "5min_avg":ss1, "10min_avg":ss2, "20min_avg":ss3, "30min_avg":ss4, "60min_avg":ss5})
            rolling_df["market_date_time"] = pd.to_datetime(rolling_df["market_date_time"])
            rolling_df = rolling_df.set_index("market_date_time")

            show_df = pd.concat([growth_df, rolling_df], axis=1)
            show_df = round_df(show_df[-period:], 3) # 取3位小数
            if pt == True:
                print(f"\n\n\n代码 - {stock_code} - '分时数据' 如下:")
                print(show_df)
            return show_df
        else:
            print({"k_msg":"\n还没开盘, 无法获取开盘价, 无法得到df.\n"})


    def req_newest_data(self, secids_lst=["1.603042", "0.159995", "0.002048"], extend_fields_lst=[]):
        """
            function: 获取个股的最新数据 (主要是最新价/最新今日涨幅) (使用sse的方式获取数据)
                    [20200802-update:找到了另一个接口, 不需要sse的方式来获取'最新数据'了!!] [沿用自己习惯的方式, 更加的方便]

            params:
                secids_lst: ["1.603042", "0.159995"]  (传入的是stock_code:即'有前缀')
                extend_fields_lst: ['f102', 'f103'] (表示新增的fields, 已经默认有以下的fields了)

            tips:
                # python获取SSE的实时数据!!!  (这个库好像不能与charles同时开启, 否则爬取的时候会报错...)

        """

        # 将参数转成str格式
        secids_str = ",".join(secids_lst)
        default_fields_lst = ['f1', 'f2', 'f3', 'f4', 'f9', 'f12', 'f13', 'f14', 'f15', 'f16', 'f18','f100', 'f102', 'f103']
        default_fields_lst.extend(extend_fields_lst) # 在默认lst上扩展 extend_fields_lst
        fields_lst = default_fields_lst
        fields_str = ",".join(fields_lst)

        # # 方法一: SSE方式获取数据
        # # ======================
        # # 使用SSE方式获取realtime的数据 (是一种特殊的http请求!)
        # from sseclient import SSEClient
        # url = (
        #     "https://84.push2.eastmoney.com/api/qt/ulist/sse?"
        #     "invt=3&pi=0&pz=109&mpi=2000&po=1&"
        #     # "secids=1.603042,0.159995,1.600855,0.000651,1.601318,0.002048,1.515030,1.600016,0.002959,0.002594,0.002415,1.600685,0.002142,1.600757,0.002168,1.600977,0.159995,0.002230,0.002505&"
        #     # "fields=f12,f13,f19,f14,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100,f103,f102,f15,f16,f38,f39,f113,f40,f41,f42,f44,f45,f46,f50,f51,f52,f53,f54,f55,f56,f57,f49,f26"
        #     f"secids={secids_str}&"
        #     f"fields={fields_str}"
        # )
        # messages = SSEClient(url)
        # for msg in messages:
        #     print(msg)
        #     msg_json = msg.data
        #     msg_dic = json.loads(msg_json)
        #     print(msg_dic)
        #     break
        # kkprint(msg_dic=msg_dic)

        # 方法二: requests方式获取数据 (最常用最熟悉的方式) [推荐]
        # ======================
        url = (
            "https://push2.eastmoney.com/api/qt/ulist.np/get?"
            "invt=3&pi=0&pz=109&mpi=2000&po=1&"
            f"secids={secids_str}&"
            f"fields={fields_str}"
        )
        txt = req(url)
        msg_dic = json.loads(txt)

        # 构造成df
        if msg_dic.get("data") != None:
            print("最新数据获取成功!\n")
        stock_newest_info_lst = msg_dic.get("data", {}).get("diff", [])
        df = pd.DataFrame(stock_newest_info_lst)

        # 加工处理'列'
        df["stock_code"] = df["f13"].astype(str) + "." + df["f12"]
        df["JRZF"] = df["f3"] / 10000 #f3
        df["JRZE"] = df["f4"] / 100 #f4
        df["PE"] = df["f9"] / 100 #f9
        df["HighestPrice"] = df["f15"] / 100 #f15
        df["LowestPrice"] = df["f16"] / 100 #f16
        df["LastPrice"] = df["f18"] / 100 #f18
            # 计算最新价格('元'为单位)  [注意]: A股的f2的数值是以'分'为单位; ETF的f2数值是以'0.001元'为单位.... (很无语, 不知道DC为啥这样设计)
        query_df = df.query("f1 == 2")
        df.loc[query_df.index, "NewestPrice"] = df["f2"] / 100 # 当该Zq类型是'A股'时, 除以100
        query_df = df.query("f1 == 3")
        df.loc[query_df.index, "NewestPrice"] = df["f2"] / 1000 # 当该Zq类型是'ETF'时, 除以1000

        ordered_field_lst = [
            # "Zqdm",
            # "NewestPeice", "JRZF", "JRZE", "PE",
            # "HighestPrice", "LowestPrice", "LastPrice",
            # "行业板块"

            "f12", "f13",
            "NewestPrice", "JRZF", "JRZE", "PE",
            "HighestPrice", "LowestPrice", "LastPrice",
            "f100"
        ]
        ordered_field_lst.extend(extend_fields_lst) # 扩充'新增的fields'
        df = sort_df(df, ordered_field_lst)
        df = df.rename(columns=ulist_change_name_dict)
        df["stock_code"] = df["SecSe"].astype("str") + "." + df["Zqdm"]

        return df


    def req_index(self, pt=True):
        """
            function: 获取市场上主要的指数
            tips:
                - 带有 "req" 开头的函数, 都是有 "爬虫/http请求" 成分的
        """
        # 000001:上证; 000300:沪深300; 399001:深证成指; 399006:创业; 399005:中小板; HSI:恒生; NDX:纳斯达克;
        # secids_lst = ['1.000001', '0.399001', '0.399006', '0.399005', '8.040120', '104.CN00Y', '100.HSI', '100.DJIA', '100.FTSE', '100.N225', '100.NDX', '100.GDAXI', '102.CL00Y', '101.GC00Y', '100.UDI', '133.USDCNH', '120.USDCNYC', '142.scm&']
        secids_lst = ['1.000001', '1.000300', '0.399001', '0.399006', '0.399005', '100.HSI', '100.NDX']
        df = self.req_newest_data(secids_lst=secids_lst, extend_fields_lst=["f14"]) # f14:Zqmc
        if pt == True:
            show_formatted_df(df)
        return df


    def req_my_stock(self, stock_code_lst=[], pt=True):
        """
            function: 获取zxstock的最新价格 (用req_my_stock的别名,快速获取最新数据[其实是因为没有想好叫啥函数名])
        """
        if len(stock_code_lst) == 0:
            stock_code_lst = [
                "1.000001", "0.002505", "0.002168", "1.600757", "0.159995",
                "1.600977",
                "1.600855", "1.603042",
                "1.601398", "0.002230", "1.600016",
                "0.002415",
                "0.002959",
                "1.600685", "0.002594",

            ]

        newest_df = Q.req_newest_data(secids_lst=stock_code_lst)
        newest_df.pop("行业板块")
        newest_df = newest_df.sort_values("JRZF")
        if pt == True:
            show_formatted_df(newest_df)
        return newest_df


    def live(self, stock_code_lst=[]):
        """获取自动清屏的'个股-实时数据'!"""
        count = 0
        while True:
            count += 1
            print(f"count: {count}")
            self.req_my_stock(stock_code_lst=stock_code_lst)
            time.sleep(10)
            os.system("clear")





    # 爬取&存取'所有个股的历史数据: 冷启动后, 只需要每个月更新一次即可'
    def store_hist_allstock(self, period=0):
        """
            使用场景: 可以月度存储一次! (用于跑回测用的) [更新频次:每月]
        """
        # 从DC爬取所有stock的历史数据
        df = read_mongo(self.db["newest_allstock"], {}, {"stock_code":1, "Zqdm":1})
        docs = df_to_docs(df)
        today_date = get_today_date(format_="%Y%m%d") # "20200803"
        previous_60_date = get_previous_date(today_date, days_str="60 d", format_="%Y%m%d") # "20200704"

        # 遍历每一个stock
        count = 0
        for doc in docs:
            count += 1
            Zqdm = doc.get("Zqdm", "")
            stock_code = doc.get("stock_code", "")
            # 调用外部接口, 得到该stock的历年所有日k线数据 (除了第一次需要历年所有数据外, 之后只需每月更新当月数据即可!!)
            df = self.req_hist_data(stock_code=stock_code, period=period, pt=False, beg=previous_60_date, end=today_date)

            # 添加两类stock名称
            df["Zqdm"] = Zqdm
            df["stock_code"] = stock_code
            # 处理日期字段
            df = df.reset_index()
            df["market_date"] = df["market_date"].dt.strftime("%Y-%m-%d")

            # 遍历该stock的所有历史数据, 一条条存入mongo
            docs = df_to_docs(df)
            for doc in docs:
                market_date = doc.get("market_date")
                self.db["hist_allstock"].update_one(
                    # 使用 "stock_code"和"markget_date" 作为该表的复合索引
                    {"stock_code":stock_code, "market_date":market_date},
                    {"$set":doc},
                    upsert=True,
                )
            random_num = get_random_num()
            print(f"{count}: 已成功存入'{Zqdm}'的hist_data....   {get_this_time()}....   休眠{round(random_num,2)}...")
            time.sleep(random_num)
            # break
            # if count == 10:
                # break


    # 爬取&存取'自选股的历史数据'
    def store_hist_zxstock(self, period=0, stock_code_lst=[]):
        """
            function: 获取指数的历史数据 (其实是把他从 hist_allstock 中抽离出来的) (周度爬取)

            note:
                1.000001:上证指数; 1.000300:沪深300; 0.399001:深圳成指;
                0.399006:创业板指; 0.399005:中小板指; 1.000905:中证500;

        """
        # 1. 每次更新时, 先把整个表给删了... (因为后续不想用update的方式,性能太慢...insert_many会快很多...)
        self.db["hist_zxstock"].remove({})
        print("已清空hist_zxstock...")

        # 设置默认要爬的'自选股'
        if len(stock_code_lst) == 0:
            # 使用'const.py'脚本中的'zx股'
            A_stock_code_lst = Q.Zqmc_to_stock_code(Zqmc_lst=A_Zqmc_lst)
            ETF_stock_code_lst = Q.Zqmc_to_stock_code(Zqmc_lst=ETF_Zqmc_lst)
            stock_code_lst = A_stock_code_lst + ETF_stock_code_lst

        # 遍历每一个stock
        count = 0
        for stock_code in stock_code_lst:
            count += 1
            Zqdm = stock_code[2:]

            # 调用外部接口, 得到该stock的历年所有日k线数据
            df = self.req_hist_data(stock_code=stock_code, period=period, pt=False, beg=0, end="20300101")

            # 添加两类stock名称
            df["Zqdm"] = Zqdm
            df["stock_code"] = stock_code
            # 处理日期字段
            df = df.reset_index()
            df["market_date"] = df["market_date"].dt.strftime("%Y-%m-%d")

            # 遍历该stock的所有历史数据, 一条条存入mongo
            docs = df_to_docs(df)
                # 1. 使用update_one的方式,可以只爬增量数据!
            # for doc in docs:
            #     market_date = doc.get("market_date")
            #     self.db["hist_index"].update_one(
            #         # 这里的上证指数是1.000001, 如果没有前缀可能会被误导, 所以使用'stock_code'来做唯一索引!
            #         {"stock_code":stock_code, "market_date":market_date},
            #         {"$set":doc},
            #         upsert=True,
            #     )
                # 2. 使用insert_many的方式,提高插入速度!
            self.db["hist_zxstock"].insert_many(docs)
            random_num = get_random_num()
            print(f"{count}: 已成功存入'{Zqdm}'的hist_data....   {get_this_time()}....   休眠{round(random_num,2)}...")
            time.sleep(random_num*10)


    # 爬取&存取'指数的历史数据'
    def store_hist_index(self, period=0):
        """
            function: 获取指数的历史数据 (其实是把他从 hist_allstock 中抽离出来的) (周度爬取)
        """

        # 从DC爬取所有index的历史数据
        # 1.000001:上证指数; 1.000300:沪深300; 0.399001:深圳成指; 0.399006:创业板指; 0.399005:中小板指; 1.000905:中证500;
        # 主要关注3个指数: 1.000001, 1.000300, 1.000905
        stock_code_lst = ['1.000001', '1.000300', '0.399001', '0.399006', '0.399005', "1.000905"]
        today_date = get_today_date(format_="%Y%m%d") # "20200803"
        # previous_60_date = get_previous_date(today_date, days_str="60 d", format_="%Y%m%d") # "20200704" [toggle]: 开启这段: 意味着只截取该指数的一小段数据
        previous_60_date = 0 # [toggle]: 开启这段: 意味着把该指数的所有历史数据都获取过来 (由于每个月存一次, 其实可以暴力读取所有历史数据!!)

        # 遍历每一个stock
        count = 0
        for stock_code in stock_code_lst:
            count += 1
            Zqdm = stock_code[2:]
            # 调用外部接口, 得到该stock的历年所有日k线数据
            df = self.req_hist_data(stock_code=stock_code, period=period, pt=False, beg=previous_60_date, end=today_date)

            # 添加两类stock名称
            df["Zqdm"] = Zqdm
            df["stock_code"] = stock_code
            # 处理日期字段
            df = df.reset_index()
            df["market_date"] = df["market_date"].dt.strftime("%Y-%m-%d")

            # 遍历该stock的所有历史数据, 一条条存入mongo
            docs = df_to_docs(df)
            for doc in docs:
                market_date = doc.get("market_date")
                self.db["hist_index"].update_one(
                    # 这里的上证指数是1.000001, 如果没有前缀可能会被误导, 所以使用'stock_code'来做唯一索引!
                    {"stock_code":stock_code, "market_date":market_date},
                    {"$set":doc},
                    upsert=True,
                )
            random_num = get_random_num()
            print(f"{count}: 已成功存入'{Zqdm}'的hist_data....   {get_this_time()}....   休眠{round(random_num,2)}...")
            time.sleep(random_num)



    def store_trend_zxstock(self, period=0, stock_code_lst=[]):
        """
            function: 获取'zx'部分的'今日所有'分时数据 (**zx:自选)
                (如果要发挥作用, 必须每天爬取更新) (因为分时数据每次只能获取到'当日的分时数据')
        """

        # 设置默认要爬的'自选股'
        if len(stock_code_lst) == 0:
            # 使用'const.py'脚本中的'zx股'
            A_stock_code_lst = Q.Zqmc_to_stock_code(Zqmc_lst=A_Zqmc_lst)
            ETF_stock_code_lst = Q.Zqmc_to_stock_code(Zqmc_lst=ETF_Zqmc_lst)
            stock_code_lst = A_stock_code_lst + ETF_stock_code_lst


        # 遍历每一个stock
        count = 0
        for stock_code in stock_code_lst:
            count += 1
            Zqdm = stock_code.split(".")[1]
            # 调用外部接口, 得到该stock的'今日'所有分时数据
            df = self.req_trend_data(stock_code=stock_code, period=period, pt=False) # period=0代表所有区间


            # 添加两类stock名称
            df["Zqdm"] = Zqdm
            df["stock_code"] = stock_code
            # 处理日期字段
            df = df.reset_index()
            df["market_date_time"] = df["market_date_time"].dt.strftime("%Y-%m-%d %X")

            # 遍历该stock的所有历史数据, 一条条存入mongo
            docs = df_to_docs(df)
            for doc in docs:
                market_date_time = doc.get("market_date_time")
                self.db["trend_zxstock"].update_one(
                    {"Zqdm":Zqdm, "market_date_time":market_date_time},
                    {"$set":doc},
                    upsert=True,
                )
            random_num = get_random_num()
            print(f"{count}: 已成功存入'{Zqdm}'的 trend_data....   {get_this_time()}....   休眠{round(random_num,2)}...")
            time.sleep(random_num)




    def store_newest_allstock(self):
        """
            function: 把4000+沪深的A股最新数据, 存储到mongo中 (存储更新频次: 每周更新一次即可!)

            tips:
                1. 该 newest_allstock 表其实可以当做 固定的"全量持有表". (所有代码的计算逻辑都来源于'它')
                    (类似于 zr_chiyou 或 danke_stock表的作用)

            # TODO:   把ETF也视为"A股", 添加到 newest_allstock mongo表中, 即可!

        """
        # 将参数转成str格式
        fields_lst = [
            'f12', 'f13', 'f19', 'f14', 'f139', 'f148', 'f2', 'f4', 'f1', 'f125', 'f18', 'f3', 'f152',
            'f5', 'f30', 'f31', 'f32', 'f6', 'f8', 'f7', 'f10', 'f22', 'f9', 'f112', 'f100', 'f103',
            'f102', 'f15', 'f16', 'f38', 'f39', 'f113', 'f40', 'f41', 'f42', 'f44', 'f45', 'f46',
            'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f49', 'f26'
        ]
        fields_str = ",".join(fields_lst)


        url_A = (
            "http://64.push2.eastmoney.com/api/qt/clist/get?"
            "cb=jQuery112404638463031674278_1595959308897&pn=1&pz=9999&po=1&np=1&"
            "ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&"
            f"fields={fields_str}"
        )
        url_ETF = (
            "http://64.push2.eastmoney.com/api/qt/clist/get?"
            "cb=jQuery112404638463031674278_1595959308897&pn=1&pz=9999&po=1&np=1&"
            "ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:MK0021,b:MK0022,b:MK0023,b:MK0024&"
            f"fields={fields_str}"
        ) # ETF共有322只

        # req请求:
            # A
        txt_A = req(url_A)
        txt_A = txt_A.replace('"-"', 'NaN')
        d_A = json.loads(re.findall(r'"diff":([\s\S]+)}}', txt_A)[0])
        df_A = pd.DataFrame(d_A)
            # ETF
        txt_ETF = req(url_ETF)
        txt_ETF = txt_ETF.replace('"-"', 'NaN')
        d_ETF = json.loads(re.findall(r'"diff":([\s\S]+)}}', txt_ETF)[0])
        df_ETF = pd.DataFrame(d_ETF)
            # 上下合并
        before_rename_df = pd.concat([df_A, df_ETF], axis=0, ignore_index=True) # 改名前的df

        # 修改列名
        _l = list(ulist_change_name_dict.values())
        renamed_df_A = df_A.rename(columns=ulist_change_name_dict)[_l] # ulist_change_name_dict是一个const常量
        renamed_df_ETF = df_ETF.rename(columns=ulist_change_name_dict)[_l] # ulist_change_name_dict是一个const常量
        after_rename_df = pd.concat([renamed_df_A, renamed_df_ETF], axis=0, ignore_index=True) # 改名后的df


        # 左右纵向合并
            # 相当于一个doc中, 既有"f1/f2"这样模糊的字段名, 也有改成中文名后的字段 (防止后续DC把字段顺序更改)
        final_df = pd.concat([before_rename_df, after_rename_df], axis=1)

        # 加工处理'列'
        final_df["stock_code"] = final_df["f13"].astype(str) + "." + final_df["f12"]
        final_df["NewestPrice"] = final_df["f2"] / 100 #f2
        final_df["JRZF"] = final_df["f3"] / 10000 #f3
        final_df["JRZE"] = final_df["f4"] / 100 #f4
        final_df["PE"] = final_df["f9"] / 100 #f9
        final_df["HighestPrice"] = final_df["f15"] / 100 #f15
        final_df["LowestPrice"] = final_df["f16"] / 100 #f16
        final_df["LastPrice"] = final_df["f18"] / 100 #f18
        # 存入mongo


        docs = df_to_docs(final_df)
        print("正在遍历doc存储中...")
        for doc in docs:
            Zqdm = doc.get("Zqdm")
            # 一条条更新
            self.db["newest_allstock"].update_one(
                {"Zqdm":Zqdm},
                {"$set":doc},
                upsert=True,
            )
        print("所有stock的最新数据, 已经成功存入mongo\n")


    def get_ALL_df(self):
        "获取所有A股的最新相关数据"
        df = read_mongo(self.db["newest_allstock"])
        return df

    def get_A_df(self):
        "获取所有A股的最新相关数据"
        df = read_mongo(self.db["newest_allstock"], {"f1":3})
        return df


    def get_ETF_df(self):
        "获取所有ETF的最新相关数据"
        df = read_mongo(self.db["newest_allstock"], {"f1":3})
        return df


    def merge_Zqmc(self, df):
        """
            function: 把原有'隐晦'的Zqdm, 直接匹配上'显式'的Zqmc
                        (1. 不管是Zqdm, 还是stock_code)
                        (2. 不管是columns, 还是index)
        """
        all_df = read_mongo(self.db["newest_allstock"], {}, {"Zqdm":1, "stock_code":1, "Zqmc":1})
        if "Zqdm" in df.columns:
            merged_df = pd.merge(df, all_df, how="left", on="Zqdm")
        elif "stock_code" in df.columns:
            merged_df = pd.merge(df, all_df, how="left", on="stock_code")
        elif "Zqdm" == df.index.name:
            all_df = all_df.set_index("Zqdm")
            merged_df = pd.concat([df, all_df], axis=1, join="inner")
        elif "stock_code" == df.index.name:
            all_df = all_df.set_index("stock_code")
            merged_df = pd.concat([df, all_df], axis=1, join="inner")
        else:
            raise Exception("该df中没有 'Zqdm'或'stock_code'\n\n")

        merged_df.pop("stock_code")

        return merged_df





    def overview_asset(self, user_name="LZC", need_to_convert_date=True):
        """
            function:
                从mongo中取出历史asset数据, 透视得到 '日期维度的净值曲线'!
            note:
                1. asset_sp表中的字段说明:
                    历史数据中的'Zxsz'实际表示的是: 当日持仓股票总市值
                    Dryk: 当日持仓股票的盈亏
                    Drykbl: 当日持仓股票的盈亏比例
                2. 需要核心关注的指标:
                    1. Dryk/CcsLjyk
                    2. TotalEarnings/ROA
                    3. CcsLjykbl/Drykbl (持仓股累计盈亏比例/当日盈亏比例) (bl不准确: 通过"每个个股的盈亏均值"计算, 不严谨, 误差大...)

            [注意]: 该报表中的'Dryk'不包含 "证券卖出所需的交易成本"和"理财收入", 所以与TotalEarnings的增长有些出入
                    (一般这天中没有执行多次卖出交易就不会产生太大的误差)


        """

        # 1. 获取mongo中的asset数据, 并透视
        df = read_mongo(self.db["asset_sp"], need_to_convert_date=need_to_convert_date)
        df = df.query(f"user_name == '{user_name}'")
        pivot_df = df.pivot_table(
            index="date",
            aggfunc={
                "total_capital_value":"mean", "total_market_value":"mean", "cash_balance":"mean",
                "CcsLjyk":"sum", "Dryk":"sum", "Drykbl":"mean", "init_capital_value":"mean",
            }
        )

        # 2. 计算透视后的汇总数据: 每日的实际"earnings"/ROA等
        pivot_df["market_value_percentage"] = pivot_df["total_market_value"] / pivot_df["total_capital_value"]
        pivot_df["TotalEarnings"] = pivot_df["total_capital_value"] - pivot_df["init_capital_value"]
        pivot_df["ROA"] = pivot_df["TotalEarnings"] / pivot_df["init_capital_value"]
            # 这里的'总市值'其实就是Ccs的总市值 (所以减掉Ccs的累计盈亏, 就是Ccs的成本市值)
        pivot_df["cost_market_value"] = pivot_df["total_market_value"] - pivot_df["CcsLjyk"]
            # Ccs的累计盈亏比例无法通过mongo数据的透视直接得出, 而是需要先透视, 再汇总进行列计算才行
        pivot_df["CcsLjykbl"] = pivot_df["total_market_value"] / pivot_df["cost_market_value"] - 1

        # 3. 排序, 打印输出
        need_to_show_list = [
            "total_capital_value", "total_market_value", "market_value_percentage", "cash_balance",
            "CcsLjyk", "CcsLjykbl", "Dryk", "Drykbl", "TotalEarnings", "ROA",
        ]
        pivot_df = sort_df(pivot_df, need_to_show_list)
        # 格式化输出df (其实就是为了把'Drykbl'用'百分号形式'呈现输出)
        show_formatted_df(pivot_df) # 自带打印功能

        return pivot_df







    def overview_deal(self, user_name="LZC", Zqmc=False):
        """
            function: 观测历史deal数据

            note:
                1. 与overview_asset的差异:
                        req_asset: 侧重于观测 '今日持仓盈亏'  [今日明细]
                        overview_asset: 侧重于观测 '持仓盈亏'的每日走势  [透视:日期维度]
                        overview_deal: 侧重于观测 '历史成交'数据   [透视:个股维度]
        """

        # 1. 获取mongo中的asset数据, 并透视
        df = read_mongo(self.db["deal_sp"])
        df = df.query(f"user_name == '{user_name}'")
        pivot_df = df[["Zqdm", "cash_flow", "deal_count_flag"]].pivot_table(
            index="Zqdm",
            aggfunc={
                "cash_flow":"sum", "deal_count_flag":"sum",
            },
        )
            # 把'买'和'卖'分成两个df (备用)
        b_df = df.query("Mmlb=='B'")
        s_df = df.query("Mmlb=='S'")
            # 统计每个股票 "买交易" 的次数
        _df1 = b_df.pivot_table(index="Zqdm", aggfunc={"user_name":"count"}).rename(columns={"user_name":"buy_times"})
            # 统计每个股票 "卖交易" 的次数
        _df2 = s_df.pivot_table(index="Zqdm", aggfunc={"user_name":"count"}).rename(columns={"user_name":"sell_times"})
        pivot_df = pd.concat([pivot_df, _df1, _df2], axis=1)

        # 2. 获取'未平仓持股'中的'成本市值'  (自己写的接口) (逻辑有点复杂和混乱, 备注都不知道咋写, 过倆月再来看肯定就看不懂了...)
        # 未平仓股dict  (eg: {"002142":-500.0, "600016":-100.0})
        opened_position_stock_dic = dict(pivot_df.query("deal_count_flag<0")["deal_count_flag"])
        lst = [] # 用于后面构造 df
            # opened_position_stock_count: 表示'未持仓股的数量' (必定是<0的, 所以: 先转成正数)
        for sim_stock_code, opened_position_stock_count in opened_position_stock_dic.items():
            opened_position_stock_count = abs(opened_position_stock_count)
            # 得到这个stock的所有 "买记录" 的docs
            this_stock_b_docs = df_to_docs(b_df[-1::-1].query(f"Zqdm=='{sim_stock_code}'"))
            # 遍历这个docs
            _accu_Zqsl = 0 # 待累加的'证券数量'  (一旦累加的"和", 大于"未平仓股数", 则停止循环, 并在此环节计算"未平仓股票的成本市值")
            _accu_cash_flow = 0
            for doc in this_stock_b_docs:
                cash_flow = abs(doc.get("cash_flow"))
                Zqsl = abs(doc.get("deal_count_flag")) # 该"买记录"中的 '证券数量'
                if _accu_Zqsl + Zqsl < opened_position_stock_count:
                    _accu_Zqsl += Zqsl # 累加'证券数量'
                    _accu_cash_flow += cash_flow # 累加'未平仓的股票成本市值'
                elif _accu_Zqsl + Zqsl >= opened_position_stock_count:
                    _delta_count = opened_position_stock_count - _accu_Zqsl #  1100-900=200
                    _accu_Zqsl += _delta_count
                    _accu_cash_flow += _delta_count/Zqsl * cash_flow # eg: 200/500股 * 10000元 (即:这200股的成本市值)
                    lst.append({"Zqdm":sim_stock_code, "Zqsl":_accu_Zqsl, "cost_market_value":_accu_cash_flow})
                    break
        cost_market_value_df = pd.DataFrame(lst).set_index("Zqdm")


        # 3. 从asset数据接口中, 获取到"股票的最新市值"
        # asset_df = A.req_asset(need_to_concat=False, return_raw_df=False, pt=False)
        # asset_df["newest_market_value"] = asset_df["Zxjg"] * asset_df["Zqsl"]
        # asset_df = asset_df[["Zqdm","newest_market_value"]]
        # asset_df = asset_df.set_index("Zqdm")

        _df = pivot_df.query("deal_count_flag<0")
        _df["Zqsl"] = _df["deal_count_flag"] * (-1)
        Zqdm_lst = list(_df.index)
            # 把 002505 转成 0.002505 的形式
                # TODO: 这里获取不到ETF的 stock_code, 所以有点问题... 试着把所有的ETF也放入到 hist_allstock中? (或者新建 hist_allETF ?)
        stock_code_lst = self._Zqdm_to_StockCode(Zqdm_lst=Zqdm_lst)
        newest_df = self.req_newest_data(secids_lst=stock_code_lst) # 这里获取'最新价格'需要依赖: newest_allstock中是否记录该Zqdm对应的 stock_code
        newest_df = newest_df.set_index("Zqdm")[["NewestPrice"]]
        newest_df = pd.concat([newest_df, _df], axis=1)
        newest_df["newest_market_value"] = newest_df["NewestPrice"] * newest_df["Zqsl"]
        newest_df = newest_df[["newest_market_value"]]


        # 4. 计算当前'未平仓持股'中的'成本市值'和'最新市值'
        final_df = pd.concat([pivot_df, cost_market_value_df, newest_df], axis=1).fillna(0.0)
        final_df["closed_position_earnings"] = final_df["cash_flow"] + final_df["cost_market_value"]
        final_df["total_earnings"] = final_df["cash_flow"] + final_df["newest_market_value"]
        final_df = final_df.sort_values("total_earnings")
        final_df.rename_axis("Zqdm", inplace=True)
        if Zqmc == True:
            final_df = self.merge_Zqmc(final_df)

        # 5. 添加一行'汇总值'
        ss = final_df.sum()
        ss.name = "汇总"
        if "Zqmc" in ss.index:
            ss.pop("Zqmc")
        if "stock_code" in ss.index:
            ss.pop("stock_code")
        final_df = final_df.append(ss)
            # 本final_df中'汇总'的 total_earnings: 是真实的"股票收益"
            # overview_asset中 '每日'的 TotalEarnings: 是总资产的收益(包括'股票收益'/'天天宝-理财收益')
        print("以下final_df: 是通过完整的历史现金流量表生成, 数据绝对真实可靠!! total_earnings就是真实的股票收益(不包括理财收益)")



        return final_df




    # 0.002505:大康; 0.002168:惠城;  1.600757:长江; 0.159995:芯; 1.600977:中电; 1.600855:长峰; 1.603042:华脉; 1.601398:工; 0.002230:讯;
    # 1.600016:民生
    # 上:1开头; 深:0开头
    # [待买]   万科:0.000002;
    # [等待低位捕捉]   海康:0.002415; 春秋:1.601021; 海直:0.000099; 桂林:0.000978;
    #                中船:1.600685; 顺丰:0.002352; 格力:0.000651; 比亚迪:0.002594; :002142;
    # [k好,价高]   葫芦娃:1.605199; 东财:0.300059; 海天:1.603288; 中公:0.002607; 美的:0.000333; 小熊:0.002959;
    # [apple]   东山精密:0.002384; 立讯精密:0.002475; 蓝思:0.300433;


    # # 弃用...(使用req_my_stock取代它)
    # def get_my_stock(self, stock_code_lst=[], pt=True):
    #     if len(stock_code_lst) == 0:
    #         stock_code_lst = [
    #             "1.000001", "0.002505", "0.002168", "1.600757", "0.159995",
    #             "1.600977",
    #             "1.600855", "1.603042",
    #             "1.601398", "0.002230", "1.600016",
    #             "0.002415",
    #             # "1.600685", "0.002352", "0.000651", "0.002594",
    #             "0.002959",
    #             "1.600685", "0.002594",
    #
    #         ]
    #
    #     to_concat_lst = []
    #     for stock_code in stock_code_lst:
    #         last_trend_data_df = self.req_trend_data(stock_code, period=1, pt=False) # 最新一行的'分时数据' (df类型)
    #         to_concat_lst.append(last_trend_data_df)
    #
    #     # 合并多个stock的'最新'数据
    #     df = pd.concat(to_concat_lst, axis=0) # 行方向:上下扩展行
    #     df = df.sort_values("JRZF")
    #     if pt == True:
    #         show_formatted_df(df)
    #     return df









Q = ReqStockData(host="local") # 使用Q作为实例名 (历史原因导致)
remote_Q = ReqStockData(host="remote") # 使用Q作为实例名 (历史原因导致)
overview_asset = remote_Q.overview_asset





class QuantUser():

    def __init__(self):
        pass








class FirmOfferAccount(QuantUser):
    # "继承了一个普通用户类 (拥有普通用户的所有方法, 又可以有实盘账户的相关方法)" # 实现起来好像比较麻烦, 暂时先不使用
    """
        function: sp账户(实盘账户); 模拟实盘的各种真实操作. 实现了东财账户的模拟登录/交易信息和资产信息的存储;

        类组件函数:
            1. 私有函数:
                - 模拟登录所需的flow步骤函数
            2. req: (请求数据)
                - req_deal_data   (本sp账户的'历史&今日成交数据')
                - req_asset       (本sp账户的'个人资产数据')
                - req_my_stock    (本sp账户的'zx股的最新价格')
            3. store: (存储数据)
                - store_deal_sp
                - store_asset_sp
            4. operate: (交易操作)
                - buying
                - selling

    """

    def __init__(
        self, user_name="LZC",
        cookies_dict=None, userId="32040006118200",
        original_password="0061883000", OriginalTotalCapitalValue=100000,
        host="local"
    ):
        """
            params:
                userId: zjzh
                original_password: 原始密码
                user_name: 用户真实名称首字母缩写  (LZC表示是我本人的实盘账户) (可用于后期存储到mongo的)
        """
        if host == "local":
            self.db = db_for_quant
        elif host == "remote":
            self.db = remote_db_for_quant

        # 1. 初始化必要的登录信息
        self.user_name = user_name
        if user_name == "LZC":
            self.userId = "320400061182"
            self.original_password = "618830"
            self.OriginalTotalCapitalValue = 250000 # 最开始的总资产 (用于后期计算总资产增幅比例的[净值曲线])
        elif user_name == "LSH":
            self.userId = "420500001519"
            self.original_password = "353622"
            self.OriginalTotalCapitalValue = 300000
        else:
            self.userId = userId
            self.original_password = original_password
            self.OriginalTotalCapitalValue = OriginalTotalCapitalValue
        # 模拟构造'随机参数': randNumber
            # (必须要有才能获取到, 可以用简单固定的1. 但如果每次都一样, 担心被反爬.)
        self.random_randNum_str = str(np.random.rand())

        # 2. 当没有传入cookies_dict时, 重新模拟登录, 重新获取cookies_dict
        if cookies_dict == None:
            self._login()
            self._check_login()
        else:
            self.cookies_dict = cookies_dict

        # 3. 获取zz信息 (每次买卖执行前, 或者其他重要操作前, 都需要执行一遍该函数: 用于更新账户资金数据)
        asset_df = self.req_asset(need_to_concat=True, return_raw_df=False)


        # 4. 赋予一个超强的爬虫类 (专门获取'东财'数据的接口)
        self.Q = ReqStockData(host=host)


    def _login(self):
        "模拟登录的'集成接口'(实际由3个函数实现)"
        # 1. 获取&识别验证码
        self._req_captcha_img()

        # 2. 获取cookie (模拟登录)
        self._simulate_login()

        # 3. 获取validatekey_value (买卖中必要的参数验证)
        time.sleep(1)
        self._req_validatekey_value()


    def _check_login(self):
        "当第一次模拟登录失败后, 可以启动循环模拟(3次循环避免网络偶然性出错), 若循环3次后还是失败, 则不再尝试...."
        for i in range(3):
            # 1. 模拟登录成功
            if self.validatekey:
                print("\n模拟登录成功!!!\n\n\n")
                break
            # 2. 模拟登录失败
            else:
                print("\n模拟登录失败!!!  等待20秒后重新模拟....\n\n\n")
                time.sleep(20)
                self._login()




    def _req_captcha_img(self):
        # 1. 获取&识别: 验证码图片
        get_captcha_url = f"https://jy.xzsec.com/Login/YZM?randNum={self.random_randNum_str}" # 请求得到验证码图片
        res_obj = req(get_captcha_url, is_obj=True)
        captcha_img_bytes = res_obj.content
        with open("captcha.jpg", "wb") as f:
            f.write(captcha_img_bytes)
        captcha_result_dict = ocr_captcha(captcha_img_bytes)
        if captcha_result_dict.get("err_str", "fail") == "OK":
            print("超级鹰验证码识别成功!!\n")
            self.captcha_result_str = captcha_result_dict.get("pic_str", "99999999999") # 一般不会存在9999的情况
        else:
            # 当超级鹰识别错误:
            print("超级鹰验证码识别失败!!\n")
            self.captcha_result_str = "8888888888888"


    def _simulate_login(self):
        # 2. post模拟登录
        url = "https://jy.xzsec.com/Login/Authentication"
        other_headers = {
            "Host" : "jy.xzsec.com",
        }
        req_method = "post"

        # js逆向: 模拟登录破解!!
        js_full_path = f"{FILE_PATH_FOR_KW618}/k_requests/js/encryption_4_dongcai_login.js"
        encrypted_password = exec_js_function(js_full_path, "EMTradeEncrypt.encrypt", self.original_password) # 获得js加密后的密码
        data = {
            "userId" : self.userId,
            # 每次模拟登录会生成不同的password, 但是每个生成的password都是可以用的(不知道差异在哪).
            "password" : encrypted_password,
            "randNumber" : self.random_randNum_str,
            "identifyCode" : self.captcha_result_str,
            "duration" : "1800",
            "authCode" : "",
            "type" : "Z",
        }
        res_obj = req(url=url, other_headers=other_headers, req_method=req_method, data=data, is_obj=True)

        # 3. 获取模拟登录后返回的cookie (uuid: 是账户信息的唯一标识!!)
        self.cookies_dict = requests.utils.dict_from_cookiejar(res_obj.cookies)
        print(self.cookies_dict)
        self.Uuid = self.cookies_dict.get("Uuid")
        self.cookie = f"Uuid={self.Uuid}" # 这一串cookie就可以唯一指定一个账户! (所有数据的获取,只需要它即可!)


    def _req_validatekey_value(self):
        # 获取今天最新的validatekey (在html中得到)
        url = "https://jy.xzsec.com/Trade/Buy"
        other_headers = {
            "Host" : "jy.xzsec.com",
            # "Cookie" : "Uuid=dc047541643247d198b792a6735ba07f",
            "Referer" : "https://jy.xzsec.com/Login?el=1&clear=&returl=/Trade/Buy",
            "Connection" : "keep-alive",
        }
        res_selector = req(url=url, other_headers=other_headers, selector=True, cookies=self.cookies_dict)
        self.validatekey = res_selector.xpath('//*[@id="em_validatekey"]/@value').extract_first()
        sprint(validatekey=self.validatekey)





    def _req_hist_deal_data(self, start_date="2020-06-01", end_date="2020-10-01", limit_items=100):
        # 1. req访问
        url = "https://jy.xzsec.com/Search/GetHisDealData"
        other_headers = {
            "Host" : "jy.xzsec.com",
            "Conten-Length" : "13",
            # "Cookie" : self.cookie,
        }
        req_method = "post"
        data = {
            "st" : start_date, # start_time
            "et" : end_date, # end_time
            "qqhs" : limit_items, # 单次限制返回多少条数据
        }
        txt = req(url=url, other_headers=other_headers, req_method=req_method, data=data, cookies=self.cookies_dict)
        d = json.loads(txt)

        # 2. 处理返回值
            # Zxsz:最新市值; Zxjg:最新价格; Zqmc:证券名称; Zqsl:证券数量; Zqdm:证券代码;
            # Zjzh:资金账号; Ljyk:浮动盈亏; Ykbl;盈亏比例; Cbjg:成本价格; Ckcb:总成本;
            # Market:市场(HA:上市;SA:深市)
            # Mmss:买卖说明
        hist_deal_data_lst = d.get("Data", [{}])
        df = pd.DataFrame(hist_deal_data_lst)
        df = df.rename(columns={
            "Cjrq":"deal_date", "Cjsj":"deal_time",
        })
        if len(df):
            df["deal_date_time"] = df["deal_date"] + df["deal_time"]
            df["deal_date"] = pd.to_datetime(df["deal_date_time"]).dt.strftime("%Y-%m-%d")
            df["deal_date_time"] = pd.to_datetime(df["deal_date_time"]).dt.strftime("%Y-%m-%d %X")
            df.pop("deal_time")
            # df["deal_date_time"] = pd.to_datetime(df["deal_date_time"])
            # df["deal_date"] = pd.to_datetime(df["deal_date"])
            # df = df.set_index("deal_date_time")
            df = df.sort_values("deal_date_time") # 按日期升序排序
            df[["Zqdm", "Cjjg", "Cjsl", "Cjje", "deal_date"]]

        return df


    def _req_today_deal_data(self, start_date="2020-06-01", end_date="2020-10-01", limit_items=100):
        # 1. req访问
        url = "https://jy.xzsec.com/Search/GetDealData"
        other_headers = {
            "Host" : "jy.xzsec.com",
            "Conten-Length" : "13",
            # "Cookie" : self.cookie,
        }
        req_method = "post"
        data = {
            "qqhs" : limit_items, # 单次限制返回多少条数据
        }
        txt = req(url=url, other_headers=other_headers, req_method=req_method, data=data, cookies=self.cookies_dict)
        d = json.loads(txt)

        # 2. 处理返回值
        hist_deal_data_lst = d.get("Data", [{}])
        df = pd.DataFrame(hist_deal_data_lst)
        df = df.rename(columns={
            "Cjrq":"deal_date", "Cjsj":"deal_time",
        })
        if len(df):
            df["deal_date_time"] = df["deal_date"] + df["deal_time"]
            df["deal_date"] = pd.to_datetime(df["deal_date_time"]).dt.strftime("%Y-%m-%d")
            df["deal_date_time"] = pd.to_datetime(df["deal_date_time"]).dt.strftime("%Y-%m-%d %X")
            df.pop("deal_time")
            # df["deal_date_time"] = pd.to_datetime(df["deal_date_time"])
            # df["deal_date"] = pd.to_datetime(df["deal_date"])
            # df = df.set_index("deal_date_time")
            df = df.sort_values("deal_date_time") # 按日期升序排序
            df[["Zqdm", "Cjjg", "Cjsl", "Cjje", "deal_date"]]

        return df


    def req_deal_data(self, start_date="2020-06-01", end_date="2020-10-01", limit_items=100):
        """
            function: 获取所有历史成交 (这秒之前的所有)
        """

        hist_deal_data_df = self._req_hist_deal_data(start_date=start_date, end_date=end_date, limit_items=limit_items)
        time.sleep(1.5) # 防止反爬
        today_deal_data_df = self._req_today_deal_data(start_date=start_date, end_date=end_date, limit_items=limit_items)
        df = pd.concat([hist_deal_data_df, today_deal_data_df], axis=0, ignore_index=True)
        # df.pop("Zqmc")
        # df.pop("Mmsm")
        df = df.fillna(0.0) # 把NAN变成0.0, 方便后续的 加减乘除计算
        return df


    def req_asset(self, need_to_concat=True, return_raw_df=False, pt=True):
        """
            function: 获取整体的资产信息
        """
        # 1. req访问
        url = "https://jy.xzsec.com/Com/queryAssetAndPositionV1"
        other_headers = {
            "Host" : "jy.xzsec.com",
            "Conten-Length" : "13",
            # "Cookie" : self.cookie,
        }
        req_method = "post"
        txt = req(url=url, other_headers=other_headers, req_method=req_method, cookies=self.cookies_dict)
        d = json.loads(txt)

        # 2. 处理返回值
            # 1. 汇总数据 (df_1) (只有一行的df)
        total_asset_dict = d.get("Data", [{}])[0]
        stock_positions_lst = total_asset_dict.pop("positions")
        df_1 = pd.DataFrame([total_asset_dict])
        df_1["Zqdm"] = "汇总"

            # 2. 细分持仓数据 (df_2)
        df_2 = pd.DataFrame(stock_positions_lst)
        df_2["Ljyk"] = pd.to_numeric(df_2["Ljyk"])
        df_2 = df_2.sort_values("Ljyk")
        df_2["date"] = get_today_date()
        df_2["datetime"] = get_this_date_time()
        df_2["Cbjg"] = df_2["Cbjg"].astype("float")
        df_2["Zxsz"] = df_2["Zxsz"].astype("float")
        df_2["Zqsl"] = df_2["Zqsl"].astype("float")
        df_2["Zxjg"] = df_2["Zxsz"] / df_2["Zqsl"] # 手动计算 "最新的股票单价"

        # 3. 更新当前账户的最新资金数据
            # i.现金余额:
        self.cash_balance = float(df_1.get("Kyzj", 0))
            # ii.持仓股票数量:
        self.chicang_stock_count_dict = dict(df_2.set_index("Zqdm")["Kysl"].astype("int"))
            # 格式如下: (key是'sim_stock_code'格式, value:是int类型)
            # chicang_stock_count_dict = {
            #     "600757":2500, "002142":500,
            # }
            # iii.账户RMB总资产
        self.total_capital_value = float(df_1.get("RMBZzc", 0))
            # iv.持仓股票总市值
        self.total_market_value = round(self.total_capital_value - self.cash_balance, 2)

        # 4. 拼接 '汇总'+'细分'
        if need_to_concat == True:
            asset_df = pd.concat([df_1, df_2], axis=0, ignore_index=True)
        else:
            asset_df = df_2

        # 5. df格式化 & 打印呈现
        asset_df = asset_df.fillna(0.0) # 用0.0来填充空置(便于后期计算)
        asset_df = asset_df.drop("Zqmc", axis=1) # 1.把名称去掉 (避嫌) (以后可删掉这行)
        raw_df = deepcopy(asset_df)
        asset_df = asset_df[["Zqdm", "Cbjg", "Ckcb", "Zxjg", "Zxsz", "Ljyk", "Ykbl", "Dryk", "Drykbl", "Zqsl", "Kysl", "date", "datetime"]]
            # 防止当日晚上东财对'当日数据'清零后, 后面报错...
        if asset_df["Dryk"].iloc[0] == '':
            asset_df["Dryk"] = 0.0
            asset_df["Drykbl"] = 0.0
        if pt == True:
            show_formatted_df(asset_df)

        # 6. 返回不同类型的df
        if return_raw_df == True: # 返回原始的所有字段
            return raw_df
        elif return_raw_df == False: # 仅返回需要的必要字段 [常用]
            return asset_df





    def req_my_stock(self, stock_code_lst=[]):
        """
            note: 感觉和 req_asset 有点重复啊...
        """
        # "get_my_chicang_stock_market_data: 获取持仓股的行情数据"
        def joint(row):
            "用于把sim_stock_code拼接成 stock_code"
            Zqdm = row.get("Zqdm")
            Market = row.get("Market")
            if Market == "SA":
                stock_code = "0." + str(Zqdm)
            elif Market == "HA":
                stock_code = "1." + str(Zqdm)
            row["stock_code"] = stock_code
            return row

        asset_df = self.req_asset(need_to_concat=False, return_raw_df=True)
        chicang_stock_df = asset_df.apply(joint, axis=1)
        stock_code_lst = list(chicang_stock_df["stock_code"])
        chicang_stock_df = self.Q.req_my_stock(stock_code_lst=stock_code_lst)
        return chicang_stock_df






    def store_deal_sp(self):
        """
            function: 把历史所有交易数据(包括今日), 都存入mongo
                      (用循环update_one的方式更新, 防止今日爬取错误破坏了历史数据)

            note:
                cash_flow: 是已经扣除了所有的费用 (最真实的每一次交易的现金流向)
        """
        all_hist_deal_df = self.req_deal_data()
        all_hist_deal_df["user_name"] = self.user_name
        # 将df变成docs的格式
        docs = df_to_docs(all_hist_deal_df)
        for doc in docs:
            # 1. 取变量值 (需要把str类型的数字, 转成float类型)
            Zqdm = doc.get("Zqdm")
            deal_date_time = doc.get("deal_date_time")
            Cjjg = float(doc.get("Cjjg"))
            Cjsl = float(doc.get("Cjsl"))
            Cjje = float(doc.get("Cjje"))
            Sxf = float(doc.get("Sxf"))
            Yhs = float(doc.get("Yhs"))
            Ghf = float(doc.get("Ghf"))
            Cjbh = float(doc.get("Cjbh"))
            total_fee = round(Sxf + Yhs + Ghf, 2)
                # 统计买卖金额(包含所有费用)
            Mmlb = doc.get("Mmlb") # mm类别
            if Mmlb == "B": # 现金流为'负'
                cash_flow = round(-1 * Cjje - total_fee, 2)
                deal_count_flag = -1 * Cjsl # deal_count_flag 用于最后透视汇总时候, 看该股是否已经平仓 (未平仓的cash_flow必定是'负的',需要排除)
            elif Mmlb == "S": # 现金流为'正'
                cash_flow = round(1 * Cjje - total_fee, 2)
                deal_count_flag = 1 * Cjsl # (成交数量的标志)

            doc.update({
                "Cjjg":Cjjg, "Cjsl":Cjsl, "Cjje":Cjje,
                "Sxf":Sxf, "Yhs":Yhs, "Ghf":Ghf,
                "total_fee":total_fee, "cash_flow":cash_flow, "deal_count_flag":deal_count_flag,
            })
            print(f"{Zqdm}, {deal_date_time},   cash_flow: {cash_flow}\n\n")

            # 2. 将 '所有历史成交数据' 一条条的插入
            self.db["deal_sp"].update_one(
                {"user_name":self.user_name, "Zqdm":Zqdm, "deal_date_time":deal_date_time},
                {"$set":doc},
                upsert=True,
            )
        # 打印提示
        print(f"[用户'{self.user_name}']: 成功插入'所有历史成交'数据")








    def store_asset_sp(self, forced_update=False):
        """
            function: 将每日真实数据存入mongo中 (基本上只要下午3点之后执行一遍即可)

            params:
                forced_update: 是否强制插入 (若是: 则即使当日盈亏数据清零, 也要对mongo进行更新)

            notice:
                1. self.db["asset_sp"]:
                    1. 每一天的真实asset情况的快照
                        (券商没有提供的数据, 我自己记录)
                    2. 该集合表的唯一主键: "user_name"/"Zqdm"/"date" 的三复合键
                    3. 所有本应为数值型的字段, 最好都以数值型存储在mongo中(不要用str存)---> 这样方便后期调用时候处理数据
                2. 如果有一天忘记了存储, 或者存储失败:
                    直接添加 "Zqdm"为"999"的一条数据 (直接把今日的汇总数据插入算了...)

        """

        # 获取最新的asset数据
        asset_df = self.req_asset(need_to_concat=False, return_raw_df=False)
        if (asset_df["Dryk"].sum() == 0.0) and (forced_update == False):
            print(f"[用户'{self.user_name}']: 插入今日的asset数据失败 (Dryk为0, 不覆盖mongo中数据)")
            return "update failed"
        # 数据库存储中, 必须要有'user_name'来做用户区分  (便于后期汇总个人数据)
        asset_df["user_name"] = self.user_name
        asset_df["total_capital_value"] = round(self.total_capital_value, 2) # 在每日asset记录中, 添加汇总后的'zzc'数据
        asset_df["total_market_value"] = round(self.total_market_value, 2)
        asset_df["cash_balance"] = round(self.cash_balance, 2)
        asset_df["init_capital_value"] = round(self.OriginalTotalCapitalValue, 2)


        # 将df变成docs的格式
        docs = df_to_docs(asset_df)
        for doc in docs:
            # 1. 取变量值 (需要把str类型的数字, 转成float类型)
            Zqdm = doc.get("Zqdm")
            date = doc.get("date")
            datetime = doc.get("datetime")
            Cbjg = float(doc.get("Cbjg"))
            Ckcb = float(doc.get("Ckcb"))
            Zxsz = float(doc.get("Zxsz"))
            # CcsLjyk仅代表未售出gu的累计yk. (不太重要的指标, 但从未来复盘角度: 可以理解为我对chicang_stock的持有态度[啥时候割?一涨就割?一跌就割?])
            CcsLjyk = float(doc.get("Ljyk")) # 这里的yk不是真实的所有累计yk (只针对当前chicang_stock部分) [遂: 将其更名为"CcsLjyk"]
            Ykbl = float(doc.get("Ykbl"))
            Dryk = float(doc.get("Dryk"))
            Drykbl = float(doc.get("Drykbl"))
            Zqsl = float(doc.get("Zqsl"))
            Kysl = float(doc.get("Kysl"))
            doc.update({"Cbjg":Cbjg, "Ckcb":Ckcb, "Zxsz":Zxsz, "CcsLjyk":CcsLjyk, "Ykbl":Ykbl, "Dryk":Dryk, "Drykbl":Drykbl, "Zqsl":Zqsl, "Kysl":Kysl})

            # 2. 将今日的 '该股票的asset数据' 存入mongo  (一日中如果执行多次, 后者可以覆盖前者)
            self.db["asset_sp"].update_one(
                {"user_name":self.user_name, "Zqdm":Zqdm, "date":date},
                {"$set":doc},
                upsert=True,
            )
        # 打印提示
        print(f"[用户'{self.user_name}']: 成功插入今日'{date}'的asset数据")







    def buying(self, sim_stock_code="002230", buying_price=6.18, buying_count=100):
        # 买入stock
        """
            params:
                sim_stock_code = "600757" # stock_code是指: 前面加'0'或'1'的那种.
        """

        # 更新账户资产数据
        self.req_asset()
        # 获取现金余额
        cash_balance = self.cash_balance # float类型
        _buying_price = round(float(buying_price), 2)
        _buying_count = int(buying_count)
        _total_buying_price = _buying_price * _buying_count

        # 当'买入所需现金' <= 剩余现金余额时, 执行buying操作
        if _total_buying_price <= cash_balance:
            buying_url = f"https://jy.xzsec.com/Trade/SubmitTrade?validatekey={self.validatekey}"
            other_headers = {
                "Host" : "jy.xzsec.com",
                "Conten-Length" : "92",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Origin" : "https://jy.xzsec.com",
                "Referer" : "https://jy.xzsec.com/Trade/Buy",
                "Connection" : "keep-alive",
                # "Cookie" : f"Uuid={self.Uuid}",
            }
            req_method = "post"
                # 设置委托买入的参数
            trade_type = "B" # B是买入, S是卖出  (该参数必须要有的!!)
            data = {
                "stockCode" : sim_stock_code,
                "price" : str(float(buying_price)),
                "amount" : str(buying_count),
                "tradeType" : trade_type,
                # "zqmc" : "宁波银行",
            }
            txt = req(url=buying_url, other_headers=other_headers, req_method=req_method, data=data, cookies=self.cookies_dict)
            d = json.loads(txt)
            if d.get("Status") == 0: # 当status为0时, 表示'交易提交成功'!!
                wtbh = d.get("Data", [{}])[0].get("Wtbh") # 委托编号
                if wtbh:
                    k_msg = (
                        f"交易提交成功!!(委托编号:{wtbh})"
                        f"【Buying-{sim_stock_code}】 {_buying_price}RMB,  {_buying_count}Gu,  Total: {_total_buying_price}RMB;\n\n"
                    )
                    print(k_msg)
            elif d.get("Status") == -2 : # 当status为-2时, 表示'会话过期'!!
                k_msg = "会话过期, 需要重新登录!!\n"
                sprint(k_msg=k_msg)
            else:
                k_msg = "发生未知错误: 交易提交失败!!\n"
                k_msg += d.get("Message", "")
                print(k_msg)
                raise Exception(k_msg)
        # 当'买入所需现金' > 剩余现金余额时, 中止buying操作
        else:
            k_msg = "现金余额不足!!\n"
            print(k_msg)




    def selling(self, sim_stock_code="002230", selling_price=618, selling_count=100):
        # 卖出stock
        """
            params:
                sim_stock_code = "600757" # stock_code是指: 前面加'0'或'1'的那种.
        """

        # 更新账户资产数据
        self.req_asset()
        # 获取股票持仓数量
        chicang_stock_count = self.chicang_stock_count_dict.get(sim_stock_code)
        _selling_price = round(float(selling_price), 2)
        _selling_count = int(selling_count)
        _total_selling_price = _selling_price * _selling_count

        # 当'待卖出股数' <= 持仓股数时, 执行selling操作
        if _selling_count <= chicang_stock_count:
            selling_url = f"https://jy.xzsec.com/Trade/SubmitTrade?validatekey={self.validatekey}"
            other_headers = {
                "Host" : "jy.xzsec.com",
                "Conten-Length" : "110",
                "Content-Type" : "application/x-www-form-urlencoded",
                "Origin" : "https://jy.xzsec.com",
                "Referer" : "https://jy.xzsec.com/Trade/Sale",
                "Connection" : "keep-alive",
                # "Cookie" : f"Uuid={self.Uuid}",
            }
            req_method = "post"
                # 设置委托买入的参数
            trade_type = "S" # B是买入, S是卖出  (该参数必须要有的!!)
            data = {
                "stockCode" : sim_stock_code,
                "price" : str(float(selling_price)),
                "amount" : str(selling_count),
                "tradeType" : trade_type,
                # "zqmc" : "宁波银行",
            }
            txt = req(url=selling_url, other_headers=other_headers, req_method=req_method, data=data, cookies=self.cookies_dict)
            d = json.loads(txt)
            if d.get("Status") == 0: # 当status为0时, 表示'交易提交成功'!!
                wtbh = d.get("Data", [{}])[0].get("Wtbh") # 委托编号
                if wtbh:
                    k_msg = (
                        f"交易提交成功!!(委托编号:{wtbh})"
                        f"【Selling-{sim_stock_code}】 {_selling_price}RMB,  {_selling_count}Gu,  Total: {_total_selling_price}RMB;\n\n"
                    )
                    print(k_msg)
            elif d.get("Status") == -2 : # 当status为-2时, 表示'会话过期'!!
                k_msg = "会话过期, 需要重新登录!!\n"
                sprint(k_msg=k_msg)
            elif d.get("Status") == -1 : # 当status为-1时, 表示'可用股份数量不足'!!
                k_msg = "可用股份数量不足!!\n"
                sprint(k_msg=k_msg)
            else:
                k_msg = "发生未知错误: 交易提交失败!!\n"
                k_msg += d.get("Message", "")
                print(k_msg)
                raise Exception(k_msg)
        # 当'待卖出股数' > 持仓股数时, 中止selling操作
        else:
            k_msg = "可用股份数量不足!!\n"
            print(k_msg)















def main():
    pass

    # Q.req_hist_allstock()

    # get_live_data()
    A = FirmOfferAccount("LZC", host="local") # 生成FOA对象可以大致能使用一天, 后续只要调用具体方法即可!!
    # df = A.req_deal_data()
    # print(df)
    # A.store_all_dealdata_in_mongo()


if __name__ == '__main__':
    print("Start test!\n\n")
    main()
    print("\n\n\nIt's over!")
