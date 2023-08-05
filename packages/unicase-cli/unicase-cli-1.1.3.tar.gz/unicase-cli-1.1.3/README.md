# unicase

`pip install unicase-cli`

```
>unicase --help

Usage: unicase [OPTIONS] COMMAND [ARGS]...

  UNI 测试用例管理工具

Options:
  --help  Show this message and exit.

Commands:
  config  配置测试人员、API Base Url
  create  创建 Excel 用例模板文件
  upload  上传 Excel 用例到 TAPD
```

## 创建 Excel 用例模板文件
写用例前可以先生成一个属于当前迭代的用例模板
```
>unicase create --help  

Usage: unicase create [OPTIONS]

  创建 Excel 用例模板文件

Options:
  --name TEXT  指定生成的文件路径，默认生成到当前文件夹且以迭代名称命名
  --help       Show this message and exit.
```
![](https://img.mocobk.cn/20210223102451898487.png)

## 配置
```
>unicase config --help 
         
Usage: unicase config [OPTIONS]

  配置测试人员、API Base Url

Options:
  --tester TEXT    当前测试人员英文名(上传用例时需要用到)
  --base-url TEXT  当前 API Base Url
  --help           Show this message and exit.
```
## 上传用例（开发中 50%）
```
>Usage: unicase upload [OPTIONS] FILE

  上传 Excel 用例到 TAPD

Options:
  --type [bvt|all]  用例上传类型：bvt 冒烟用例，all 全部用例
  --help            Show this message and exit.
```