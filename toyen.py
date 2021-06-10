import re

Rate = {
    "￥": 1, 
    "₩": 0.1, # ウォン
    "£": 154, # ポンド
    "$": 108.97, # USD
    "A$": 108.97, # USD 
    "R$": 7.73, # レアル (ブラジル)
    "€": 132, # ユーロ
    "₹": 1.49, # ルピー (インド)
    "NT$": 3.89, # ニュー台湾ドル
    "HK$": 14.03, #香港ドル
    "CA$": 90, # カナダドル
    "MX$": 5.47, # ペソ （メキシコ)
    "CHF ": 120.88, # フラン (スイス)
    "HUF ": 0.38, # フォリント（ハンガリー)
    "ARS ": 1.16, # ペソ (アルゼンチン)
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
    "NZ ": 78.0, 
}

def toyen(paid):
    yeng = toPaidGroup(paid)
    try:
        return int(float(yeng.group(2)) * Rate[yeng.group(1)])
    except:
        print("★ERROR!★")
        return 0

def toPaidGroup(paid):
    paid = paid.replace(",", "")
    regit = re.compile("(.*\s|\$|.*\$|￥|₩|£|€|₹)(.*)")
    one_int = regit.match(paid)
    return one_int

if __name__ == '__main__':
    print(toyen("$100.00"))
