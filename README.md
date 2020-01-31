# Collect-Info-Research

- 目录结构

```
├── generat_plugin.py
├── info_collect.py
└── plugins
    ├── ...
```

将文章分为web、re、pwn、generic、coding、news这几类，方便推送给用户时，用户可根据自身需求快速查看对应文章，如需增加类别，需要修改以下代码：

在model_types中添加你要新增的类别名称即可。

![6f54ba3920f5143224656da86ea78075](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo477qtj30zq042mxu.jpg)

RSS源：[zer0yu/CyberSecurityRSS: RSS: 优秀的网络安全知识来源](https://github.com/zer0yu/CyberSecurityRSS)

存入mongodb的数据字段：

![24d5ae03167d39eca38c034024bbffbc](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo4mwjxj327y0d6453.jpg)

使用插件式开发，可以满足自定义插件以及自定义类别的需求，只需要按照格式写好对应的插件即可。

## 插件开发

插件格式：```{}_{}_plugin.format(name,type,)```

generat_plugin.py是用来以模板形式生成插件的,usage如下：

```
usage: generat_plugin.py [-h] -u URL -pn PLUGIN_NAME --type TYPE --rsstype
                         RSSTYPE

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Rss Url.
  -pn PLUGIN_NAME, --plugin_name PLUGIN_NAME
                        Plugin name.
  --type TYPE           Plugin type.
```

这几个参数都是必须要传入的，url是rss的url，pn是插件的名称，type是插件的type，即web、re、pwn这些，使用这款插件生成工具，可以解决百分之90的rss源解析。

使用方式：

![994502b98087e84ab63b548129b1bd6d](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo5bfroj31ya02wq46.jpg)

按照格式传入信息后，会在当前目录下生成插件：

![e78b712bde489809ed60d5e69d5615f4](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo5o708j31iy02sdh9.jpg)

如果输出如上，即打印出了rss内的文章信息，并且两个时间格式都是相同的，就可以直接用了，不过在用之前要删去这两行：

![c96b2616f1c61c31bc897b5de3ec2178](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo6lzfaj31d60323zt.jpg)

PS：我在模板中设置了rss的解析时间为10s，如果超出这个解析时间，默认定为解析失败，有需要的可以自行修改。

⚠️：插件生成工具不是万能的，有的插件并不支持我自定义好了的模板，比如某one插件。

他的rss是这样的：

![56d81b7d62daa2f8e4ab99e6f337f0d0](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo7mn3hj31a40u0aly.jpg)

里边没有我在模板中写好的updated参数，所以插件直接生成的脚本用不了，稍微改改才能用，最终运行效果如下。

![56ea64e8ccc4243b1eef1a8bfefa8bc4](https://tva1.sinaimg.cn/large/006tNbRwgy1gbfqo8ha3yj327y0smh3z.jpg)

另外，写插件也并不一定非要是解析RSS的插件，其他插件都是可以的，只要最终往mongodb中插入指定结构的数据即可。