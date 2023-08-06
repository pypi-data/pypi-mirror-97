# 使用说明

## Sample

### Config
继承ApolloConfig 或者YamlConfig，定义类属性即可，注意做类型标注，会从Apollo拉取对应的字段，并做parse

#### sample
定义:
```python
# config.py
import os
from insnail_ai_tools.config import ApolloConfig


class Config(ApolloConfig):
    ES_URI: list = None
    MONGO_URI: str = "mongo_uri"
    DEBUG: bool = True
    AGE: int = 10


config = Config(
    os.getenv("APOLLO_APP_ID", "insnail-qa-robot"),
    os.getenv("APOLLO_SERVER_URL", "http://10.0.0.176:8080"),
    os.getenv("APOLLO_CLUSTER", "default")
)
config.fetch()
```

使用:
```python
# use.py
from config import config
print(config.ES_URI)
```

### web app

[fastapi](https://fastapi.tiangolo.com/)

#### sample

```python
from insnail_ai_tools.web import create_fast_api_app
app = create_fast_api_app(cors=True, health_check=True, title="My App", version="0.0.1")

```