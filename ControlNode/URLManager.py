#-*-coding:utf-8-*-



"""
url管理器是管理所有的url的，但是拉钩网的数据是通过API接口来获取的
所以对于url构造来说，并没有多少意义，API接口通过post方式传递参数来
获取数据，所以url管理器在此项目中没有多大意义，url无需通过构造，而是需要
在获取数据的时候传递参数，这部分放在下载器中
"""

class URLManager(object):
    def __init__(self):
        super(self).__init__
