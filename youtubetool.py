import nettool
import json
import re
import toyen

class Chat:
    def __init__(self):
        self.channelid = ""
        self.author = ""
        self.paid = ""
        self.yen = ""

    def __repr__(self):
        return repr((self.author, self.yen, self.paid))


class Youtubedata:
    def __init__(self):
        self.videoid = ""
        self.nexturl = ""
        self.uploadtime = ""
        self.chatlist = []
        self.author = ""
        self.channelid = ""
        self.twitterid = ""
        self.totalpaid = 0

    def firstjson(self):
        url = "https://www.youtube.com/watch?v={}".format(self.videoid)
        content = nettool.htmlget(url)
        
        # アップロード日 取得
        datestart = content.find('datePublished')+24
        datetxt = content[datestart : datestart+10]
        datetxt = datetxt.replace("-","")
        self.uploadtime = datetxt

        # TwitterID取得 (Test)
        subtext = content.find('<body dir="ltr')
        datestart = content.find('twitter.com/', subtext)+12
        dateend = content.find("\\n", datestart)
        if (dateend - datestart < 20):
            self.twitterid = content[datestart:dateend]

        # 配信者取得
        datestart = content.find('channelId":"', subtext)+12
        dateend = content.find('"', datestart)
        self.channelid = content[datestart:dateend]

        datestart = content.find('author":"', subtext)+9
        dateend = content.find('"', datestart)
        self.author = content[datestart:dateend]

        # 配信者画像リンク取得
        datestart = content.find('https://yt3.ggpht.com/ytc/', subtext)
        dateend = content.find('=', subtext)
        # あとで

        # チャットURL 取得
        jsonstart = content.find('一部の')+76
        jsontxt = content[jsonstart:].find('{"continuation') + 17 + jsonstart
        self.nexturl = content[jsontxt :jsontxt+136]
        return

    def htmlParseJson(self):
        url = "https://www.youtube.com/live_chat_replay?continuation={}".format(self.nexturl)
        html = nettool.htmlget(url)

        # HTMLからJSON抽出
        jsonstart = html.find('window["ytInitialData"]')+26
        jsonend = html[jsonstart:].find('</script>') + jsonstart - 1
        jsontxt = html[jsonstart : jsonend]
        if (jsontxt != ""):
            jsondata = json.loads(jsontxt)["continuationContents"]["liveChatContinuation"]

        return jsondata

    def chatLoop(self):
        # DEBUG Count
        count = 0
        jsonval = ["liveChatTextMessageRenderer", "liveChatPaidMessageRenderer"]
        while(self.nexturl):
            jsondata = self.htmlParseJson()
            if ("liveChatReplayContinuationData" in jsondata["continuations"][0]) :
                self.nexturl = jsondata["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
                self.jsontoPay(jsondata)
            else:
                self.nexturl = False
            count +=1
            if count % 100 == 0:
                print(count)

    def jsontoPay(self, jsondata):
        for count in range(1, len(jsondata["actions"])-1) :
            if( "addChatItemAction"  in jsondata["actions"][count]["replayChatItemAction"]["actions"][0]): 
                json_actions = jsondata["actions"][count]["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]
            else:
                continue

            # スパチャ/ステッカースパチャ/それ以外
            if ( "liveChatPaidMessageRenderer" in json_actions):
                Chatval = "liveChatPaidMessageRenderer"
            elif ("liveChatPaidStickerRenderer" in json_actions):
                Chatval = "liveChatPaidStickerRenderer"
            else:
                continue

            # 各パラメータ取得
            channelid = json_actions[Chatval]["authorExternalChannelId"]
            found=next( (chat for chat in self.chatlist if chat.channelid==channelid) ,None)
            paid = json_actions[Chatval]["purchaseAmountText"]["simpleText"].replace(',','')
            
            if(not found):
                found = Chat()
                found.paid = paid
                found.channelid = json_actions[Chatval]["authorExternalChannelId"]
                found.author = json_actions[Chatval]["authorName"]["simpleText"]
                self.chatlist.append(found)
            else:
                found = self.plusmoney(found, paid)

            # 合計金額加算
            self.totalpaid += toyen.toyen(paid)
            # print("{}+{}={}".format(self.totalpaid - toyen.toyen(paid), toyen.toyen(paid), self.totalpaid))


    def plusmoney(self, chat, paid):
        # print(chat.paid + "|" + paid)
        one_int = toyen.toPaidGroup(chat.paid)
        two_int = toyen.toPaidGroup(paid)

        # 同じ人で通貨が同じ場合のみ加算。
        try:
            if one_int.group(1) == two_int.group(1):
                # ドルなどの小数点はFloat変換して加算
                period = two_int.group(2).split(".")
                if (len(two_int.group(2).split(".")) == 1):
                    result = int(one_int.group(2)) + int(two_int.group(2))
                    chat.paid = one_int.group(1) + str(result)
                else:
                    result = int(float(one_int.group(2))) + int(float(two_int.group(2)))
                    chat.paid = one_int.group(1) + str(result) + "." + period[1]
        except:
            print("★ERROR!★ {}, {}".format(chat.paid, paid))

        # print(chat.paid)
        return 

    def ratecalc(self):
        for chat in self.chatlist:
            chat.yen = toyen.toyen(chat.paid)
        
    def sortchatlist(self):
        st = sorted(self.chatlist, key=lambda u: u.yen, reverse=True)
        return st


    def getspchat(self, videoid):
        self.videoid = videoid
        self.firstjson()
        print("{} ({}) (@{})\nhttps://youtu.be/{}\n配信日: {}\n - - - - - - ".format(self.author, self.channelid, self.twitterid, self.videoid, self.uploadtime))
        self.chatLoop()
        self.ratecalc()

        return self

    def rankchat(self):
        st = self.sortchatlist()
        
        outputsize = 3
        if len(self.chatlist) < outputsize:
            outputsize = len(self.chatlist)

        for count in range(outputsize):
            account = st[count]
            emoji = ["🥇", "🥈", "🥉"]
            if (toyen.toPaidGroup(account.paid).group(1) == "￥"): 
                print("{}{} ￥{}".format(emoji[count], account.author, account.yen))
            else:
                print("{}{} ￥{} ({})".format(emoji[count], account.author, account.paid, account.yen))
        print("他{}人".format(len(self.chatlist)))
        print("合計￥{}".format(self.totalpaid))
        

if __name__ == '__main__':
    yd = Youtubedata()
    sp = yd.getspchat("_AkweolyFYE")
    sp.rankchat()
    

    # ひろゆき
    # yd.main("_AkweolyFYE")