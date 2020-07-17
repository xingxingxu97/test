import pandas as pd
data_train=pd.read_csv('C:/Users/28640/Desktop/sensor_train.csv')
data_test=pd.read_csv('C:/Users/28640/Desktop/sensor_test.csv')
data_test['fragment_id']=data_test['fragment_id']+7292
#合并训练集与测试集
data=pd.concat([data_train,data_test],keys=['train','test'])
#构建新的指标
data['acc']=(data['acc_x']**2+data['acc_y']**2+data['acc_z']**2)**0.5
data['acc_g']=(data['acc_xg']**2+data['acc_yg']**2+data['acc_zg']**2)**0.5
#构建新的数据集，根据fragment_id对数据进行聚合
data_new=data[['fragment_id','behavior_id']].drop_duplicates()
#构建各加速度指标在5s的时间序列上的特征
for i in [indicator for indicator in data.columns if 'acc' in indicator]:
    for j in ['max','min','mean','median','std','skew']:
        data_new[i+'_'+j]=data[i].groupby(data['fragment_id']).agg(j).values
    data_new[i+'_kurt']=data[i].groupby(data['fragment_id']).apply(lambda x:pd.Series(x).kurt()).values
#保存新数据在本地上
data_new.to_csv('D:/data_temp.csv')

data_new=pd.read_csv('D:/data_temp.csv')