# coding:utf-8

from setuptools import setup
# or
# from distutils.core import setup  
foruser = '''# Author:KuoYuan Li
[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)
本程式提供功能如下
1.輕量手寫數字資料庫(訓練資料640張圖，測試資料50張圖)
2.建立手寫圖片的windows小程式(paint.exe) 使用 dowloadPaintToolKit() 下載
 '''
setup(
        name='Data_HandWrite',   
        version='1.0.9',  
        description='Hand write toolkit and data for windows',
        long_description=foruser,
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/Data_HandWrite',      
        packages=['Data_HandWrite'],   
        include_package_data=True,
        keywords = ['machine learning','HandWrite','data'],   # Keywords that define your package best
          install_requires=[ 
          'numpy',
          'matplotlib'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
      ],
)
