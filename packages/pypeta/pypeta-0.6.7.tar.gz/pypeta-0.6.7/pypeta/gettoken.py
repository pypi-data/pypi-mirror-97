from pypeta import Peta

host='https://peta.bgi.com/api'
peta=Peta(username="bgi-peta@genomics.cn",password="zhuqingyan",host=host)

print(peta.cookies['token'])