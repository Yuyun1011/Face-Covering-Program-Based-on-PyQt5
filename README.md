# -基于PyQt的监控数据集人脸手动遮挡程序-
## 1 项目简介
对于监控视频的数据集当中，会拍摄到行人的脸部，为了保护其隐私，需要对数据集的人脸部分进行手动遮盖，并且保存这给位置呈灰色的黑底图像。本项目基于PyQt5，完成了上述基本任务。
## 2 基本功能
本项目主要功能为手动遮挡图像数据集中人脸部分。首先使用者可以加载一幅RGB图像到程序窗口，同时会生成一幅与其同宽高的全黑像素图。然后使用者可以再加载一幅IR图像（绝大多数情况下，除色域之外，其他与RGB图像完全相同）到程序窗口，并对这三幅图像同时进行操作。在RGB图像上面使用鼠标画笔对人脸部分进行遮盖的同时，笔迹会在IR图像和全黑像素图的相同位置出现。完成人脸遮盖之后，可以保存改动后的全黑像素图像。还能够实时显示当前操作的RGB图像和IR图像的绝对位置，和要保存的改动后的全黑像素图的保存路径。另外，为了对使用者友好，本程序还设置了，上一张，下一张，清空笔迹等快捷键。
![face_cover](https://user-images.githubusercontent.com/45918664/184271301-c58bd8d8-1855-49a5-ae58-8b71927b272f.png)
## 3 运行环境
本人运行本程序的计算机操作系统为Windows 11，Python解释器版本为Python 3.9， PyQt版本为5.15.4。
另外，因为种种原因，PyQt5的安装可能会出现一些问题，现将本人在安装方法总结如下：
```
pip install PyQt5
pip install PyQt5-tools
```
在安装的PyQt库中搜索如下目录
```
"...\plungins\platforms"
```
配置环境变量
```
QT_QPA_PLATFORM_PLUGIN_PATH
PATH: "...\plungins\platforms"
```
到此，PyQt5库就配置完毕。然后本人遇到了PNG图像能够正常加载，JPG图像文件却无法加载的问题。解决办法如下：
```
在安装库文件目录中找到包含qjpeg.dll文件的文件夹imageformats。
```
然后找到Python可执行文件即python.exe所在位置，比如本人位置为
```
"C:\Users\Yuyun1011\AppData\Local\Programs\Python\Python39"
```
最后将上述imageformats文件夹整个copy到python.exe文件所在目录下。
