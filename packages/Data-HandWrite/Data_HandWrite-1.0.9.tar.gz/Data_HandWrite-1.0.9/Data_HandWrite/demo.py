import Data_HandWrite
import numpy as np
import matplotlib.pyplot as plt
#下載 1-5 數字圖片並載入至陣列變數
Data_HandWrite.downloadData()
X_train,Y_train = Data_HandWrite.LoadData('train')
X_test,Y_test = Data_HandWrite.LoadData('test')
#模型訓練
from sklearn.svm import SVC
model = SVC(decision_function_shape='ovo',gamma=0.004,probability=True)
model.fit(X_train,Y_train)
#test資料夾整體測試
result = model.predict(X_test)
print('accuracy=',model.score(X_test,Y_test)*100)
for i in range(len(result)):
    print(Y_test[i],'==>',result[i])
#單一檔案測試
x = Data_HandWrite.LoadImgFromFile('test/5_100_0000.jpg')
plt.imshow(np.reshape(x,(28,28,3)))
plt.show()
result = model.predict_log_proba(x)
print('log probility of each class:\n',result)
#下載手繪工具程式並執行
Data_HandWrite.dowloadPaintToolKitAndExecute()