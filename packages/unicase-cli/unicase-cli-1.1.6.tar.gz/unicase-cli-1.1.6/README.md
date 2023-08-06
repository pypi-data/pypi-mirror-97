![](https://shields.mitmproxy.org/pypi/v/unicase-cli.svg) ![](https://shields.mitmproxy.org/pypi/pyversions/unicase-cli.svg)
# unicase（用例管理命令行工具）

`pip install -U unicase-cli`

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

## 配置
由于创建和上传用例都需要创建人信息，在使用前必须配置测试人员英文名
```
>unicase config --help 
         
Usage: unicase config [OPTIONS]

  配置测试人员、API Base Url

Options:
  --tester TEXT    当前测试人员英文名(上传用例时需要用到)
  --base-url TEXT  当前 API Base Url
  --help           Show this message and exit.
```


## 创建 Excel 用例模板文件
写用例前可以先生成一个属于当前迭代的用例模板，模块中会根据所选迭代生成对应的 `需求`、`开发人员`下拉选择  
同时也会保存对应的迭代信息到 A1 单元格（请勿修改 A1）  

创建的用例模板名默认为：`{迭代名称}(创建人).xlsm`，如果想使用其他名称可以使用 --name 参数指定 
```
>unicase create --help  

Usage: unicase create [OPTIONS]

  创建 Excel 用例模板文件

Options:
  --name TEXT  指定生成的文件路径，默认生成到当前文件夹且以迭代名称命名
  --help       Show this message and exit.
```
![](https://img.mocobk.cn/20210223102451898487.png)

## 上传用例
上传用例包括 2 种类型的上传：  
`--type bvt`: 只上传冒烟测试用例，以 task 类型创建到 TAPD 对应迭代中，默认不加 `--type` 也是上传冒烟测试用例  
`--type all`: 上传所有测试用例，以 case 类型创建到 TAPD 测试用例模块中，并与相应的测试计划关联  

**\*用例必填项**  
冒烟用例：`一级模块`	`用例名称`	`用例等级（必须是 高）`	`开发人员`	`需求`  
功能用例：`一级模块`	`用例名称`	`需求`  

**注意:**  
* 用例上传后会把上传后的 `task_id`、`case_id` 重新写入你的用例文件，方便用例有修改重新上传、更新，请勿随意删除 `task_id` 和 `case_id`  
* 用例上传前都会校验用例的合法性，所以不用担心用例格式有问题导致上传错乱
* 上传用例时最好不要在 Excel 中打开该文件，避免工具写入时没有写的权限（实际这里也做了异常处理，会写入新的文件名）

```
>Usage: unicase upload [OPTIONS] FILE

  上传 Excel 用例到 TAPD

Options:
  --type [bvt|all]  用例上传类型：bvt 冒烟用例，all 全部用例
  --help            Show this message and exit.
```
冒烟用例示例

![](https://img.mocobk.cn/20210303142531279308.png!/fh/500)

## 建议操作流程
迭代开始——需求评审——`创建测试计划`——`创建迭代用例`——`上传冒烟用例`——`上传所有用例`——`执行用例`——发版——`用例若有更新重新上传`——`关闭测试计划`——`用例文件归档`

