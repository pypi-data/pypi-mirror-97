import webbrowser as wb

def baidu(Internet):
    wb.open("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=80035161_1_dg&wd="+Internet+"&fenlei=256&rsv_pq=c5e0583100006dfc&rsv_t=fe35F9WrYITKX92LiivZTaUrdK2N5zmrXEmbkCUiBBQzkiV6rRq7z5qVtkOS09WNI84Qbg&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=5&rsv_sug1=4&rsv_sug7=101&rsv_sug2=0&rsv_btype=i&inputT=5104&rsv_sug4=14786")
def sougo(Internet):
    wb.open("https://www.sogou.com/web?query="+Internet+"&_asf=www.sogou.com&_ast=&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index&sut=4434&sst0=1592999401577&lkt=0%2C0%2C0&sugsuv=1592999391075621&sugtime=1592999401577")
def go360(Internet):
    wb.open("https://www.so.com/s?ie=utf-8&fr=none&src=360sou_newhome&q="+Internet)

def visit():
    wb.open("my_com.html")

if __name__ == "__main__":
    from time import *
    print(
        """
        Warnning:
        作者：郭燕铭
        版本：0.0.1
        邮箱：gyms1111@163.com
        """
    )
    sleep(3)
    visit()