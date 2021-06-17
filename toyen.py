import re
import nettool
import sys

Rate = {
    "¥": 1,
    "￥": 1, 
    "\\": 1, 
    "₩": 0.1, # ウォン
    "£": 154, # ポンド
    "$": 108.97, # USD
    "A$": 108.97, # USD 
    "R$": 21.6, # レアル (ブラジル)
    "€": 132, # ユーロ 
    "₹": 1.49, # ルピー (インド)
    "₱": 2.28, # ペソ(フィリピン) (PHP)
    "NT$": 3.89, # ニュー台湾ドル
    "NZ$": 78.0, # ニュー台湾ドル
    "HK$": 14.03, #香港ドル
    "CA$": 90, # カナダドル
    "MX$": 5.47, # ペソ （メキシコ)
    "CHF ": 120.88, # フラン (スイス)
    "HUF ": 0.38, # フォリント（ハンガリー)
    "ARS ": 1.154, # ペソ (アルゼンチン)
    "PHP ": 2.28, # ペソ (フィリピン)
    "COP ": 0.03, # ペソ (コロンビア)
    "CLP ": 0.15, # ペソ (チリ)
    "RUB ": 1.48, # ルーブル (ロシア)
    "PLN ": 29.43, # ズローティー (ポーランド)
    "CZK ": 5.21, # コルナ（チェコ)
    "CRC ": 0.18, # コロン (コスタリカ) 
    "DKK ": 17.86, # クローネ (デンマーク)
    "NOK ": 13.10, # クローネ (ノルウェー)
    "PYG ": 0.016, # グアラニー (パラグアイ)
    "SEK ": 13.05, # クローナ （スウェーデン)
    "SGD ": 81.69, # シンガポールドル
    "MYR ": 26.56, # リンギット (マレーシア)
    "ZAR ": 8.04, # ランド (南アフリカ)
    "PEN ": 28.44, # ペルーソル
    "ISK ": 0.91, # アイスランド
    "AED ": 29.78, # ディルハム(アラブ)
    "JOD ": 154.30, # ヨルdan
    "SAR ": 29.16, # riyaru saujiarabia
    "GTQ ": 14.17, # クツアル(guatemara)
    "RON ": 27.08, # レウ(ルーマニア)
    "BYN ": 43.90, # beraru-si(ru-buru)
    "TRY ": 12.98, # トルコリラ
    "BOB ": 15.89, # boribia-no
    "HRK ": 17.79, # クーナ クロアチア
    "DOP ": 1.92, # peso dominika
    "UYU ": 2.51, # peso uruguai
    "HNL ": 4.56, # renpira honjurasu
    "NIO ": 3.10, # nikaragua korudoba
    "₪": 33.72,
    "RSD ": 1.13, #ディナール (セルビア)
    "BGN ": 67.95, # レフ(ブルガリア)
    "EGP ": 7.01, # ポンド(エジプト)
    "QAR ": 30.41, # リヤル(カタール)
    "NGN ": 0.27, # ナイラ(ナイジェリア)
    "BAM ": 67.81, # マルク(ボスニア)
}

def toyen(paid):
    yeng = toPaidGroup(paid)
    try:
        return int(float(yeng.group(2)) * Rate[yeng.group(1)])
    except:
        import traceback
        print("★ERROR!★")
        nettool.sendline("ERROR: {}".format(paid))
        nettool.sendline(traceback.print_exc())
        print("")
        return 0

def toPaidGroup(paid):
    paid = paid.replace(",", "")
    regit = re.compile("(.*\s|\$|.*\$|¥|￥|₩|£|€|₹|₪|₱)(.*)")
    one_int = regit.match(paid)
    return one_int

if __name__ == '__main__':
    print(toyen("¥100"))
