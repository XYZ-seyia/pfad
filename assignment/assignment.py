import requests
import bs4 as bs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
url = "https://www.mtr.com.hk/ch/corporate/investor/patronage.php"
response = requests.get(url)
content = response.text
soup = bs.BeautifulSoup(content, "html.parser")
data=[]
Data = []
Datas=[]
#获取所有带有td字符的数据
datas= soup.findAll("td")
#将可迭代对象转换为列表
for i in datas:
    data0=i.string
    if data0!=None:
        data.append(data0)
#去掉多余的元素
index=data.index( '二零二四年七月')
Data=data[index:]
#去除文本类型和数字中的“,”
for i in Data:
    j=i.replace(",","")
    if j.isdigit():
        j=float(j)
        Datas.append(j)
    else:
        p=i.replace(".","")
        if p.isdigit():
            i=float(i)
            Datas.append(i)
# 将数据转换为10列7行的DataFrame
new_column_names = ['Domestic Service Monthly Total', 'Domestic Service Average Weekday', 'Airport Express Monthly Total', \
                    'Airport ExpressAverage Daily', 'Cross-boundary Monthly Total', 'Cross-boundary Average Daily', 'Intercity Monthly Total', \
                    'Intercity Daily', 'HSR Monthly Total', 'HSR Average Daily']
df = pd.DataFrame(np.array(Datas).reshape(7, 10), columns=new_column_names)
# 分离相差过大的数据
df_odd = df.iloc[:, [0, 2, 4, 6, 8]]  # 第1,3,5,7,9列
df_even = df.iloc[:, [1, 3, 5, 7, 9]]  # 第2,4,6,8,10列
#折线图
plt.figure(figsize=(10, 6))
for i in range(df_odd.shape[1]):
    plt.plot(df_odd.index+1, df_odd.iloc[:, i], label=df_odd.columns[i])
plt.xlabel('month')
plt.ylabel('Number of People')
plt.title('Total Monthly MTR Population in Hong Kong from January to July 2024')
plt.legend(title='TYPE')
plt.show()

#雷达图
labels_even = df_even.columns
num_vars_even = len(labels_even)
angles_even = np.linspace(0, 2 * np.pi, num_vars_even, endpoint=False).tolist()
angles_even += angles_even[:1]
df_radar_even = df_even.mean().tolist()
df_radar_even += df_radar_even[:1]
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles_even, df_radar_even, color='green', alpha=0.25)
ax.plot(angles_even, df_radar_even, color='green', linewidth=2)
ax.set_yticklabels([])
ax.set_xticks(angles_even[:-1])
ax.set_xticklabels(labels_even)
plt.title('Average Daily MTR Population in Hong Kong from January to July 2024')
plt.show()
