import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用SimHei字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
#加载数据
data = pd.read_excel("complete_games.xlsx")
print("数据预览：")
print(data.head())
print(data.info())

#计算潜力评分
# 此处直接将 'rating' 作为主要潜力评分
data['潜力评分'] = data['rating']

#补充特征：计算每个游戏评价的文本长度，作为描述维度的一个量化指标
data['desc_len'] = data['descripration'].apply(lambda x: len(x) if isinstance(x, str) else 0)

#利用机器学习进行项目聚类
# 选择聚类特征：此处选取 'rating' 和 'desc_len'
features = ['rating', 'desc_len']
X = data[features].dropna()

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用 KMeans 进行聚类，此处设置聚类数为3（可根据实际情况调整）
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# 将聚类结果加入原始数据中（注意只对无缺失值的数据进行赋值）
data.loc[X.index, 'cluster'] = clusters

# 利用 PCA 将高维数据降到二维，便于可视化聚类效果
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')
plt.title("项目聚类分布图")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.legend(*scatter.legend_elements(), title="聚类类别")
plt.show()

#构建类型潜力矩阵
# 按照游戏类型与聚类类别统计各组的平均潜力评分

matrix = data.groupby(['type', 'cluster'])['潜力评分'].mean().unstack()
print("类型潜力矩阵：")
print(matrix)

#筛选重点项目
# 以潜力评分处于前25%的游戏作为重点项目
threshold = data['潜力评分'].quantile(0.75)
key_projects = data[data['潜力评分'] >= threshold]
print("筛选出的重点项目：")
print(key_projects[['name', 'type', '潜力评分']])
