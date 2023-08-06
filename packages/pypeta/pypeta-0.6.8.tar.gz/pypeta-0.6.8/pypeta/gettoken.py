from pypeta import Peta

host='https://peta.bgi.com/api'
peta=Peta(username="liujilong@bgi.com",password="liujilong",host=host)

print(peta.cookies['token'])
