import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. 读取数据
data = pd.read_excel("complete_games.xlsx")
# 统计所有游戏类型
data['type'] = data['type'].astype(str)  # 确保类型字段是字符串
data['type_list'] = data['type'].apply(lambda x: x.split('/') if isinstance(x, str) else [])

# 对类型进行 One-Hot 编码
mlb = MultiLabelBinarizer()
type_encoded = pd.DataFrame(mlb.fit_transform(data['type_list']), columns=mlb.classes_)

# 合并编码后的数据
data = pd.concat([data, type_encoded], axis=1)

#选择特征和目标值
X = type_encoded  # 类型编码作为输入
y_rating = data['rating']  # 目标：评分

# 拆分数据集（测试机占20%）
X_train, X_test, y_train_rating, y_test_rating = train_test_split(X, y_rating, test_size=0.2, random_state=42)

#采用随机森林训练模型
model_rating = RandomForestRegressor(n_estimators=100, random_state=42)
model_rating.fit(X_train, y_train_rating)

#预测
y_pred_rating = model_rating.predict(X_test)

#计算误差
mae_rating = mean_absolute_error(y_test_rating, y_pred_rating)

print(f"评分预测误差 (MAE): {mae_rating}")


# 预测新游戏类型评分
def predict_new_game(types):
    input_data = pd.DataFrame(0, index=[0], columns=mlb.classes_)
    for t in types:
        if t in input_data.columns:
            input_data[t] = 1
    pred_rating = model_rating.predict(input_data)[0]
    return  pred_rating

# 进行评分预测
new_types = ['买断制', 'Steam移植','修仙' ]
pred_rating = predict_new_game(new_types)
print(f"新游戏类型 {new_types} 预测的评分: {pred_rating:.2f}")
