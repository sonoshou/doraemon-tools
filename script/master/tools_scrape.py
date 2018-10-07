from bs4 import BeautifulSoup
import urllib.request as req
import os

tool_list = ['tool_a', 'tool_ka', 'tool_sa', 'tool_ta', 'tool_na', 
            'tool_ha', 'tool_ma', 'tool_ya', 'tool_ra', 'tool_wa']

# 区切りの文字を指定
sep_str = '\t'

# ひみつ道具の一覧を取得
write_str = ""
for tool in tool_list:
    url = 'https://www.tv-asahi.co.jp/apps/page/back_number.php?P_ID=1575&C_DIR=' + \
          tool + '&TYPE=pc&CNT=400&ITEM=ttl'

    res = req.urlopen(url)
    html = res.read().decode('shift-jis')

    # 取得元のhtmlの構造にエラーあり。
    html = html.replace('</font>', '')

    soup = BeautifulSoup(html, 'html.parser')

    item_list = soup.select('dl > li > dt')
    rubi_list = soup.select('dl > li > dt > span')
    desc_list = soup.select('dl > li > dd')

    for i in range(len(item_list)):
        write_str += item_list[i].text.split('\n')[1].strip() + sep_str + \
        rubi_list[i].text + sep_str + desc_list[i].text + "\n"

    res.close()

# ファイル書き込み
path_w = os.getcwd() + "/data/item_list.tsv"

with open(path_w, mode='w') as f:
    f.write(write_str)