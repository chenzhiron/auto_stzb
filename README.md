## auto_stzb
* 地图土地识别 × (目前依赖于标记)

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