from django.shortcuts import render, HttpResponse
from firstapp.models import People
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
    c=Context({'person':person})  #Context是把数据装进模板，做出一个上下文，接收一个字典参数，名称和对应的变量是什么。
    web_page = t.render(c)  #render方法把上下文，即从数据库取得的信息，渲染到模板里，并存储到web_page里

    return HttpResponse(web_page)    #把网页变成一个http的对象
    #所有的视图函数都是接收一个Request对象，返回一个Response对象
