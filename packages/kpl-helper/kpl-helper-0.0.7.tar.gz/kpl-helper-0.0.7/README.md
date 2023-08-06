# KPL Helper包

使用KPL Helper实现与KPL平台交互的功能。

在使用`helper`包之前，必须先调用`ready()`函数，在所有程序结束后调用`done()`函数。

## helper.get_parameter 函数
算法中需要暴露出来的超参数全部放入代码根目录的`parameter.yml`文件中。可以使用该函数来获取算法的超参数

## helper.io 模块
算法要得知从哪个目录下读取模型或数据，向哪个目录输出文件才能持久化文件，需要使用io模块。
`io.get_input_path`, `io.get_output_path`

## helper.metric 模块
算法如果希望绘制 Loss 等曲线，且在前端页面中实时显示。那么可以通过实例化`MetricFigure`对象来发送 metric 数据到服务端。

## helper.progress 模块
为了让算法使用者在KPL平台上知晓算法运行的进度，提供剩余时间参考。可以通过发送进度的函数，将进度信息发送给服务端。

## helper.saver 模块
可以使用命令行或函数保存算法、数据集、模型。

在容器中提供了保存所需的一些环境变量如下。如果在容器外使用需要手动指定。

- `KPL_BACKEND_HOST`是后台服务的地址。在容器中将访问内部地址。
- `KPL_TOKEN_LOCATE`jwt文件的位置。
- `KPL_TOKEN`指定了当前的jwt。可以和`KPL_TOKEN_LOCATE`二选一。

使用CLI：
```bash
$ khelper save dataset --name "dataset_name" --desc "description" --path /path/to/dataset
$ khelper save model --name "model_name" --desc "description" --dir /path/to/model
```

使用代码：
```python

```

显示上传进度条。

### 保存数据集


### 保存模型
路径根目录不能包含中文等特殊字符。可以上传文件夹模型或者单个文件。

### 保存算法
- 算法根目录下需要有`environment.yml`文件。
- 目前，算法文件夹的最大大小为50MB。
- 会将整个文件夹中的全部文件打包上传。默认忽略`__pycache__`文件夹的内容。



## helper.container 模块
可以使用命令行或函数调用。

```bash
$ khelper stop container
```

使用代码
```python
import kpl_helper as helper
helper.container.stop()
```

