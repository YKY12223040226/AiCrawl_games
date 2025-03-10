# AiCrawl_games
一个基于最新开源crawl4ai和deepseekAPI的爬取某网站游戏排行榜，在使用机器学习模型分析数据的项目

TapTap游戏数据分析系统
基于异步爬虫与机器学习的游戏市场潜力评估工具

🌟 项目亮点
​智能爬虫引擎：基于crawl4ai的异步爬虫系统，实现每秒3-5次的安全请求频率只能快捷爬取所需数据，利用deepseekAPI实现同步对爬取的每一个数据简单评价分析。
​多维度分析：集成聚类分析(KMeans)、降维可视化(PCA)、类型潜力矩阵等6大分析模块
​预测模型：随机森林回归模型实现游戏类型组合评分预测（MAE=0.23）

爬虫引擎：AsyncWebCrawler + asyncio
数据处理：Pandas + NumPy
机器学习：scikit-learn (KMeans/PCA/RandomForest)
可视化：Matplotlib + Seaborn
辅助工具：python-dotenv + logging
