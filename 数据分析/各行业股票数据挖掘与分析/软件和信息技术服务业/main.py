# 基本设置
import requests
import re
import pymysql
import time
import tushare as ts
from sk import keywords, stock_codes
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
keyword = keywords()
stock_code = stock_codes()
# stock_code = stock_code[96:]
chanYe = '软件和信息技术服务业'

# 获取每个公司的舆情数据的函数
def getScore(company, keyword):
    # 1.获取网页源代码（参考2.3、3.1、3.4节）
    url = 'http://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company  # 其中设置rtt=4则为按时间排序，如果rtt=1则为按焦点排序
    res = requests.get(url, headers=headers, timeout=10).text

    # 2.编写正则提炼内容（参考3.1节）
    p_href = '<h3 class="news-title_1YtI1 "><a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="news-title_1YtI1 ">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)
    p_date = '<span class="c-color-gray2 c-font-normal c-gap-right-xsmall" .*?>(.*?)</span>'
    date = re.findall(p_date, res)
    p_source = '<span class="c-color-gray" .*?>(.*?)</span>'
    source = re.findall(p_source, res)

    # 3.数据清洗（参考3.1节）
    length_href = len(href)
    length_title = len(title)
    length_date = len(date)
    length_source = len(source)
    m = min(length_href, length_title, length_date, length_source)
    
    for i in range(m):
        title[i] = title[i].strip()  # strip()函数用来取消字符串两端的换行或者空格，不过目前（2020-10）并没有换行或空格，所以其实不写这一行也没事
        title[i] = re.sub('<.*?>', '', title[i])  # 核心，用re.sub()函数来替换不重要的内容
        # 统一日期格式（参考5.1节）
        date[i] = date[i].split(' ')[0]
        date[i] = re.sub('年', '-', date[i])
        date[i] = re.sub('月', '-', date[i])
        date[i] = re.sub('日', '', date[i])
        if ('小时' in date[i]) or ('分钟' in date[i]):
            date[i] = time.strftime("%Y-%m-%d")
        else:
            date[i] = date[i]

    # 4.舆情评分版本4及数据深度清洗（参考5.1和5.2和5.3节）
    score = []
    for i in range(m):
        num = 0
        try:
            article = requests.get(href[i], headers=headers, timeout=10).text
        except:
            article = '爬取失败'

        try:
            article = article.encode('ISO-8859-1').decode('utf-8')
        except:
            try:
                article = article.encode('ISO-8859-1').decode('gbk')
            except:
                article = article
        p_article = '<p>(.*?)</p>'
        article_main = re.findall(p_article, article)  # 获取<p>标签里的正文信息
        article = ''.join(article_main)  # 将列表转换成为字符串  
        for k in keyword:
            if (k in article) or (k in title[i]):
                num -= 5
        score.append(num)
        # 数据深度清洗（参考5.1节）
        company_re = company[0] + '.{0,5}' + company[-1]
        if len(re.findall(company_re, article)) < 1:
            title[i] = ''
            source[i] = ''
            href[i] = ''
            date[i] = ''
            score[i] = ''
    while '' in title:
        title.remove('')
    while '' in href:
        href.remove('')
    while '' in date:
        date.remove('')
    while '' in source:
        source.remove('')
    while '' in score:
        score.remove('')

    # 5.打印清洗后的数据（参考3.1节）
    length_href = len(href)
    length_title = len(title)
    length_date = len(date)
    length_source = len(source)
    n = min(length_href, length_title, length_date, length_source)
    total = 0
    for i in range(n):
        total += score[i]
    return total

# 获取每个公司的当天收盘价的函数
def getClose(code, d='2023-06-29'):
    frame = ts.get_k_data(code, start=d, end=d)
    close = frame['close'].tolist()
    if close:
        return close[0]
    else:
        return 0

# 获取score和closeprice
for i in range(len(stock_code)):
    total = getScore(stock_code[i][1], keyword)
    closeprice = getClose(stock_code[i][0])
    stock_code[i].append(total)
    stock_code[i].append(closeprice)
    stock_code[i].append('2023-06-29')
    print('股票代码：' + str(stock_code[i][0]) + '，公司名称：' + str(stock_code[i][1]) + '，舆情得分：' + str(stock_code[i][2]) + '，收盘价格：' + str(stock_code[i][3]) + '，日期：' + str(stock_code[i][4]))

# 生成完整的数据:industry,company,title,source,href,date,score,closeprice
data = []
for i in stock_code:
    data.append([chanYe, i[0], i[1], 'baidu.com', 'baidu.com', i[4], i[2], i[3]])
print(data[:3])

# 建立数据库连接
connection = pymysql.connect(host='localhost', port=3306, user='root', password='000000', database='c3031', charset='utf8')

# 创建游标对象
cursor = connection.cursor()

# 检查表是否存在，如果存在则删除
drop_table_query = 'DROP TABLE IF EXISTS hangye_dataminning'
cursor.execute(drop_table_query)

# 创建数据表的 SQL 语句
create_table_query = '''
CREATE TABLE IF NOT EXISTS hangye_dataminning (
    industry VARCHAR(255),
    company VARCHAR(255),
    title VARCHAR(255),
    source VARCHAR(255),
    href VARCHAR(255),
    date DATE,
    score FLOAT,
    closeprice FLOAT
)
'''

# 执行创建数据表的 SQL 语句
cursor.execute(create_table_query)

# 插入数据的 SQL 语句
insert_query = '''
INSERT INTO hangye_dataminning (industry, company, title, source, href, date, score, closeprice)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''

# 执行插入数据的 SQL 语句
cursor.executemany(insert_query, data)

# 提交事务
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()

# 将数据保存为xlsx文件
import openpyxl

# 创建一个新的 Excel 工作簿
workbook = openpyxl.Workbook()

# 获取默认的工作表
sheet = workbook.active

# 设置表头字段
fields = ['industry', 'company', 'title', 'source', 'href', 'date', 'score', 'closeprice']

# 写入表头
sheet.append(fields)

# 写入数据
for row in data:
    sheet.append(row)

# 保存工作簿到文件
workbook.save('data.xlsx')

# 保存散点图为 JPG 文件
import pandas as pd
import matplotlib.pyplot as plt

# 将数据转换为 DataFrame
df = pd.DataFrame(data, columns=['industry', 'company', 'title', 'source', 'href', 'date', 'score', 'closeprice'])

# 计算第7列（score）和第8列（closeprice）的相关系数
correlation = df['score'].corr(df['closeprice'])

# 输出相关系数
print("相关系数：", correlation)
print("""相关系数的值在 -1 到 1 之间。如果相关系数接近 -1，表示两个变量之间存在强烈的负相关关系。换句话说，当 df['score'] 的值增加时，df['closeprice'] 的值很可能会减少，并且这种关系是强烈的。
如果相关系数接近 1，表示两个变量之间存在强烈的正相关关系。这意味着当 df['score'] 的值增加时，df['closeprice'] 的值很可能会增加，并且这种关系是强烈的。
如果相关系数接近 0，表示两个变量之间没有线性关系或线性关系非常弱。换句话说，df['score'] 的值的变化不会明显影响 df['closeprice'] 的值，或者它们之间的关系是非线性的。
通过输出相关系数的值，可以判断 df['score'] 和 df['closeprice'] 两列之间的线性关系的强度和方向。如果相关系数的值接近 -1 或 1，表示两列之间的线性关系较强。如果相关系数的值接近 0，则表示两列之间的线性关系较弱或者没有线性关系。
在散点图中，x 轴表示 df['score'] 列的值，y 轴表示 df['closeprice'] 列的值。通过绘制散点图，可以直观地观察到两列数据之间的关系，以进一步了解它们的线性关系及其趋势。""")

# 绘制散点图
plt.scatter(df['score'], df['closeprice'])
plt.xlabel('Score')
plt.ylabel('Close Price')
plt.title('Correlation Analysis')

# 保存散点图为 JPG 文件
plt.savefig('scatter_plot.jpg')
plt.show()