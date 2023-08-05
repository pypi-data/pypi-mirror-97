from pypeta import Peta
import sys

host = 'https://peta.bgi.com/api'
peta = Peta(username="bgi-peta@genomics.cn", password="zhuqingyan", host=host)

studys = peta.list_visible_studys()
target_name = sys.argv[1]

print(list(studys[studys.name.str.contains(target_name)].studyIdentifier))
