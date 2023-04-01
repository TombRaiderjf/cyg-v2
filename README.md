# 环境配置

1. **电脑必须是NVIDIA显卡**
2. 安装谷歌浏览器
3. 安装Python3+CUDA+torch+CudNN+TensorRT，请注意版本匹配问题renshi
4. pip install 脚本.py文件所需的模块

我的环境是win10, python 3.7.2, CUDA 11.3, torch 1.12.1+cu113, cudnn 8.6.0.163_cuda11, TensorRT 8.5.1.7

# 文件功能

1. get_cookies.py 获取谷歌浏览器cookie
2. login.py 入口脚本
3. img.png 预热图像
4. 1130rt_model.pth 训练好的图像识别模型

# 使用方法

1. 先配置好环境，确保import都能找到
2. 修改get_cookies 55行谷歌浏览器cookie路径
3. 打开谷歌浏览器，**登录自己的格子账号**
4. 复制想要抢的号的商品id，在公示结束1分钟前左右运行脚本：
   python3 login.py [id] [use_neice] 0 
   如果配置了代理池，运行脚本
   python3 login.py [id] [use_neice] [use_proxy] [num_proxy] [proxy]

脚本运行后显示以下输出说明成功启动：

`预热结束--------------`

`剩余时间： xx`

只需等待倒计时结束，开始抢号

（如果读取cookie出错，请删除本地路径的Cookies.db重新尝试；如果抢号成功会显示success，只需要刷新一下网页就能看到已下单）

# 声明

本程序仅供学习交流使用，开源为了方便大家了解torch和tensorRT加速，并非商业目的

# 联系十五

如果遇到技术问题或者想交流代码相关，请关注公众号天龙情报站，后台私信我（注明找十五），我会尽量帮助解答哦~

下方左侧就是公众号二维码，右侧是小程序二维码，最末尾是我一个美女朋友的抖音，助力千粉梦想让十五看看咱家的号召力！

![图片](gongzhong.jpg) ![图片](tools.jpg)

![图片](douyin.jpg)

