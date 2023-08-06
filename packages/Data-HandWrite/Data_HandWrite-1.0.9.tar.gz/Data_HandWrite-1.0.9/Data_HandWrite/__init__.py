import os
from PIL import Image
import numpy as np
import bz2#bz2file pypi
import zipfile
import requests
#data
#https://drive.google.com/file/d/1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs/view?usp=sharing

#paint.exr
#https://drive.google.com/file/d/1EPrPilZ4XK80Cq4n9-ynO0yxZfxYTIhP/view?usp=sharing

def _save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
def _download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = _get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    _save_response_content(response, destination)

def dowloadPaintToolKit():
    '''
    download "paint.exe" , paint and save img with label immediately
    '''
    _download_file_from_google_drive('1EPrPilZ4XK80Cq4n9-ynO0yxZfxYTIhP','paint.exe')
def dowloadPaintToolKitAndExecute():
    '''
    dowloadPaintToolKit() + autoexecute "paint.exe"
    '''
    dowloadPaintToolKit()
    os.system('paint.exe')
def downloadData(folder='',isPrint=False):
    '''
    download train set and test set to 'folder'
    filename format:
    a_b_c.jpg
        a:Label name (must be integer)
        b:Creator serial
        c:Serial
    source==>
    https://drive.google.com/file/d/1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs/view?usp=sharing
    '''
    #vedio==> https://drive.google.com/file/d/1076Ftdz8hxZkly-7QxYUR6kRJHSft-7s/view?usp=sharing
    #images==> https://drive.google.com/file/d/1zmpZY5D5vNwcxhNmTgBprisevixexA4I/view
    file_id = '1ZzSeuq-9ICZuFpPKM4H_gU8OGwpqKBAs'
    destination = '1.zip'
    _download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination, mode='r') as myzip:
        for file in myzip.namelist():
            if isPrint:print("extract "+file)
            myzip.extract(file,folder)
    print('\nfile already downloaded to the folders:')
    print(os.getcwd()+'\\train\\')
    print(os.getcwd()+'\\test\\')
    os.remove(destination)
    
def LoadImgFromFile(filename):
    '''
    return flatten image data whitch can predict directly
    '''
    x = np.asarray(Image.open(filename))
    x = x.flatten()/255
    return np.array([x])
    
def LoadDataFromWeb():
    '''
    combine downloadData() and LoadData()
    make data loading more easier
    '''
    downloadData()
    X_train,Y_train = LoadData('train')
    X_test,Y_test = LoadData('test')
    return X_train,Y_train,X_test,Y_test


def LoadData(sourceFolder):
    '''
    Load data from source Folder
    return X,Y
    X:image row data of each files Loaded from  sourceFolder
      (auto divide by 255)
    Y:Labels from filename to integer
      filename format can be found in downloadData(...)
    '''
    X = []
    Y = []
    for f in os.listdir(sourceFolder):
        try:
            y=f.split('_')[0]
            Y.append(int(y))
            x = np.asarray(Image.open(sourceFolder+'/'+f))
            X.append(x.flatten()/255) #將圖像陣列展開成 1 維
        except:pass
    X = np.array(X)
    Y = np.array(Y)
    return X,Y
                
def pickSample(X,Y,maxSize):
    '''
    pick maxSize of feature vectors for each classes
    X:image row data of each files
    (auto divide by 255)
    Y:Labels of each sample
    '''
    dic={}
    newX = []
    newY = []
    for i in range(len(Y)):
        if  Y[i] in dic:
            if dic[Y[i]]<maxSize:
                dic[Y[i]]+=1
                newX.append(X[i])
                newY.append(Y[i])
        else:dic[Y[i]] = 0    
    return np.array(newX),np.array(newY)

def printSampleCode():
    print('''import Data_HandWrite
import numpy as np
import matplotlib.pyplot as plt
#下載 1-5 數字圖片並載入至陣列變數
Data_HandWrite.downloadData()
X_train,Y_train = Data_HandWrite.LoadData('train')
X_test,Y_test = Data_HandWrite.LoadData('test')
#=====模型訓練=====
from sklearn.svm import SVC
model = SVC(decision_function_shape='ovo',gamma=0.004,probability=True)
model.fit(X_train,Y_train)
#test資料夾整體測試
result = model.predict(X_test)
print('accuracy=',model.score(X_test,Y_test)*100)
for i in range(len(result)):
    print(Y_test[i],'==>',result[i])
#=====單一檔案測試=====
ans = '3'
testFile = 'test/'+ans+'_100_0000.jpg'
x = Data_HandWrite.LoadImgFromFile(testFile)
#秀出每個類別的對數機率
log_probs = model.predict_log_proba(x)
resultLabel = str(model.predict(x)[0])
#秀出該圖形
plt.xlabel('log probility of each class:\n'+str(log_probs))
plt.title('testing result:'+resultLabel)
plt.imshow(np.reshape(x,(28,28,3)))
plt.show()
#下載手繪工具程式並執行
Data_HandWrite.dowloadPaintToolKitAndExecute()''')



