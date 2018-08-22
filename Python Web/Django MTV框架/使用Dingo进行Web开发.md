# 使用Dingo进行Web开发

## 一、理解Djingo的MTV模式

客户端向服务器发出**Request**请求，请求服务器提供数据；服务器回应**Response**，也许是页面、图片、动态的数据。在这中间发生了什么呢？

Request访问的url，指向Views。

Views的作用：

- 调配加载网页的数据

- 把加载的对应网站找出来


Views会向Models查找我们需要的数据。Models，托管数据的层级。相当于是用Python语言进行数据库中的增删改查存等操作。

Views向Models层找到需要的数据，把数据装载到Templates层。Templates层即模板层，为我们看到的网页的具体样貌。

Models、Templates、Views即Django的MTV模型。



光说不练假把式。来实际编一把。

**1、首先请安装Django框架**

**2、创建django project**

在工程目录下，使用命令行，创建第一个站点。

```shell
>django-admin startproject firstsite
```

在我们的文件目录中就创建了一个firstsite，里面包含一个firstsite文件夹和一个manage.py。

![](E:\Python\Python Web\Django MTV框架\pictures\1.png)

创建第一个App，也是命令行中创建。

```shell
>python manage.py startapp firstapp
```

创建成功后，文件目录会出现一个firstpp。

![](E:\Python\Python Web\Django MTV框架\pictures\2.png)

可以看一下整个工程的结构：

![](E:\Python\Python Web\Django MTV框架\pictures\3.png)

看一看urls.py。这个文件存放着我们网站的所有url。每个url对应一个View。通过这个方式我们来找到我们想要的网页。

![](E:\Python\Python Web\Django MTV框架\pictures\4.png)

**3、在settings.py中添加上我们创建的App。这一次是在Python编辑器中进行编辑。**

![](E:\Python\Python Web\Django MTV框架\pictures\5.png)

**4、创建数据库。**

每个网站都有数据库，要创建数据库，这样网站才可以运行。在命令行中执行migrate命令。

```shell
>python manage.py migrate
```

**5、将站点运行起来。**

看一下运行结果：

```shell
>python manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
August 22, 2018 - 23:25:58
Django version 2.1, using settings 'firstsite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

在浏览器中打开127.0.0.1:8000， 这是Django一个自带的页面，表示网站创建成功。

![](E:\Python\Python Web\Django MTV框架\pictures\6.png)

**6、在Model中创建数据表**

打开firstapp/models.py，我们刚刚创建了数据库，但是还得创建表格来进行读写。在model中定义我们的表。

首先定义一个类，定义我们自己的表格People，里面有两个字段name和job，定义字段的满足条件。

![](E:\Python\Python Web\Django MTV框架\pictures\7.png)

**执行makemigrations命令**

执行完makemigrations命令，创造出这个表。

```shell
> python manage.py makemigrations
Migrations for 'firstapp':
  firstapp\migrations\0001_initial.py
    - Create model People
```

在firstapp/migrations/0001_initial.py中，可以看见表已经自动创建：

![](E:\Python\Python Web\Django MTV框架\pictures\8.png)

**将表合并到数据库中**。则我们的表真正加到了数据库中。

```shell
> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, firstapp, sessions
Running migrations:
  Applying firstapp.0001_initial... OK
```

**7、在View中获取Model中的数据**

在views.py中需要从model中获取我们刚才的数据，才能把它呈现出来。

创建视图函数first_try()，接收用户的request消息作为参数，返回对应的网页。

**8、在View中引入Template模板对数据进行渲染**

在视图函数中，把html和css样式放入到Template中，并把需要的上下文数据渲染到模板中。

{{}}在模板中为变量的标志。

```python
# views.py中的内容
from django.shortcuts import render, HttpResponse
from models import People
from django.template import Context, Template  #引入Template模板对数据渲染

# Create your views here.
def first_try(request):
    person = People(name="Spock",job="officer")

    #把Html和CSS放进Template
    html_string = '''
        <html>
          <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.4/semantic.css">
          </head>
          <body>
            <h1 class="ui center aligned icon header">
              <i class="hand spock icon"></i>
              Hello, {{ person.name }}  
            </h1>
          </body>
        </html>
    '''
    # {{}}指模板变量
    t=Template(html_string)  #将数据定义为模板
    c=Context({'person':person})  #Context是把数据库中数据装进模板，做出一个上下文，接收一个字典参数，名称和对应的变量是什么。
    web_page = t.render(c)  #render方法把上下文，即从数据库取得的信息，渲染到模板里，并存储到web_page里
    
    return HttpResponse(web_page)    #把网页变成一个http的对象
    #所有的视图函数都是接收一个Request对象，返回一个Response对象
```

**9、在URL中分配网址。**

之前说过，在urls.py中每个url对应着一个View。在urls.py中添加新的url:view对应关系。

![](E:\Python\Python Web\Django MTV框架\pictures\9.png)

**10、python manage.py runserver后，打开浏览器，输入http://127.0.0.1:8000/first_try/**

![](E:\Python\Python Web\Django MTV框架\pictures\10.png)



