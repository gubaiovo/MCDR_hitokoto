# Hitokoto
调用[Hitokoto](https://hitokoto.cn/)接口，并自动输出到服务器

### 配置文件

```json
{
    "interval": "10s",
    "parameters": {},
    "base_url": "https://v1.hitokoto.cn/",
    "from_where": true
}
```

- `interval` : 获取间隔，支持单位：s、m、h。最少10s
- `base_url` : api地址
- `parameters` : 调用参数，参考 [#接口说明](https://developer.hitokoto.cn/sentence/#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)
- `from_where` : 是否显示来源

示例配置文件

```json
{
    "interval": "1m",
    "parameters": {
        "c": ["a", "c"],
        "max_length": 10
    },
    "base_url": "https://v1.hitokoto.cn/",
    "from_where": true
}
```



### API 调用

插件提供 `get_hitokoto()` 函数调用api

使用示例

```python
import hitokoto

message = hitokoto.get_hitokoto()
print(message)
```

