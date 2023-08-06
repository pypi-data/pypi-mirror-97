# Insnail Ai Tools

蜗牛ai团队 python的一些小工具，自用

## Install

```shell script
pip install --upgrade insnail-ai-tools
```

如果使用了豆瓣、阿里等非官方源，可能出现未同步，使用以下方式安装最新版本:
```shell script
pip install -i https://pypi.org/simple --upgrade insnail-ai-tools
```

### requires-extra

本模块依赖的包相对较多，所以对需要安装额外依赖包的模块做了若干拆分。
比如如果只需要oss上传的功能，只需要类似如下的安装：
```shell
pip install --upgrade "insnail_ai_tools[oss]"
```

如果只需要fastapi相关的模块：

```shell
pip install --upgrade "insnail_ai_tools[fastapi]"
```

如果同时需要fastapi和sso相关的模块：
```shell
pip install --upgrade "insnail_ai_tools[fastapi,sso]"
```

目前有的模块为:

- oss: 使用阿里云上传功能
- sso: 登录验证模块
- fastapi: fastapi相关模块
- django: django相关模块
- flask: flask 相关模块
- wechat: 跟微信调用相关的模块

## development

```shell
# 拉取代码
git clone https://git.woniubaoxian.com/ai/insnail_ai_tools.git
# 安装flit
pip install flit==3.0.0
# 安装开发环境
flit install --deps=develop
```
