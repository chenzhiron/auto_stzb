## auto_stzb
* 地图土地识别 × (目前依赖于标记)

## 启动项目文件说明
    命令行启动
        打开 main.py 注释掉 8.9.10 行
        进入 toolkit 目录
        运行 python ../main.py
    编辑器启动
        打开 main.py 注释掉 6.7 行
        取消注释  8,9,10 行
## electron
    取消main.py注释 31-34行
---
    使用说明
    进入 /web/electron_web/ 目录
    运行 
        yarn install 这一个可能卡住无法下载，如果无法下载就放弃，顺利的话往下走
        yarn make 这一步报错需要自行百度解决

        打包后的文件在 ./out/ 下
        自行修改 gui.py 其中的 第5行拼接路径
        回到上面 启动项目文件说明
目前基于electron 启动后无法解决内存泄露，需要自行到任务管理器，关闭 名字为 adb.exe 程序，应该是 ~~~4个~~~

## 模拟器要求
* 分辨率 1280* 720
* 模拟器版本 安卓10以下 
* 后续补充........


## 安装依赖包出现
    import paddle
    ModuleNotFoundError: No module named 'paddle'

#### 执行
    python -m pip install paddlepaddle==2.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple

## minitouch模拟器点击方案（步骤一）
    版本适应：安卓10以下
    执行命令：
        查询电脑架构：adb.exe shell getprop ro.product.cpu.abi
    添加 minitouch：
        执行命令 adb.exe push ./libs/x86/minitouch /data/local/tmp
        根据架构，替换路径 x86 为对应的架构名字，如果没有对应架构，则需要自动生成，存放libs路径自行切换
    minitouch文件权限更改：
        执行命令 adb shell
                cd /data/local/tmp
                chmod 777 minitouch
## pyminitouch 使用问题
1. 端口占用： 修改 config/const.py 配置文件中的 operate_change_port 
2. 后续补充.....