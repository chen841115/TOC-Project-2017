from transitions.extensions import GraphMachine

import telegram
import re
import urllib.request; #用來建立請求
import urllib.parse;

API_TOKEN = '389383697:AAEsHgE3Y-L9RxGFtUv4mPTufiGlsJFjP9k'
bot = telegram.Bot(token=API_TOKEN)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == '股價'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == '股票建議'

    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == '大盤'

    def is_going_to_state4(self, update):
        text = update.message.text
        return text.lower() != 'help' and text.lower() != 'back'

    def is_going_to_state5(self, update):
        text = update.message.text
        return text.lower() == '爆量長紅'

    def is_going_to_state6(self, update):
        text = update.message.text
        return text.lower() == '瞬間暴漲'

    def is_going_to_state7(self, update):
        text = update.message.text
        return text.lower() == '爆量長黑'

    def is_going_to_state8(self, update):
        text = update.message.text
        return text.lower() == '瞬間暴跌'
        
    def is_going_to_state9(self, update):
        text = update.message.text
        return text.lower() == '國際股市'
        
    def is_going_to_state10(self, update):
        text = update.message.text
        return text.lower() != 'help' and text.lower() != 'back'
        
    def is_going_to_state11(self, update):
        text = update.message.text
        return text.lower() == '休市日期'
        
    def is_going_to_state12(self, update):
        text = update.message.text
        return text.lower() != 'help' and text.lower() != 'back'

    def is_going_to_user(self, update):
        text = update.message.text
        return text.lower() == 'help' or text.lower() == 'back'

    def on_enter_user(self, update):
        #chat_id = bot.get_updates().message.chat_id
        #bot.send_message( chat_id ,  "I'm sorry Dave I'm afraid I can't do that.")
        update.message.reply_text("輸入： 大盤/股價/股票建議/國際股市/休市日期")

    def on_enter_state1(self, update):
        update.message.reply_text("請輸入股票代碼")
        #update.message.reply_text(update.message.text)
        #self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("輸入： 爆量長紅/瞬間暴漲/爆量長黑/瞬間暴跌")
        #self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        url = 'http://www.wantgoo.com/stock/0000';
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=0
        while i<len(respData):
            match = re.search(r'([0-9]+\.[0-9]+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            #update.message.reply_text("大盤指數 : ")
            update.message.reply_text("大盤指數 : "+match.group())

        i=0
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            update.message.reply_text("漲跌 : "+match.group())
        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            update.message.reply_text("漲跌% : "+match.group())

        self.go_back(update)

    def on_exit_state3(self, update):
        print('Leaving state3')

    def on_enter_state4(self, update):
        #update.message.reply_text("您輸入的股票代碼是 : ")
        update.message.reply_text("您輸入的股票代碼是 : "+update.message.text)

        url = 'http://www.wantgoo.com/stock/'+update.message.text;
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=0
        while i<len(respData):
            match = re.search(r'(?<=<h3 class="idx-name">)(.+)(?=<span class="i idx-code">)',respData[i])
            if match: break
            i+=1    
        if match:
            #update.message.reply_text("公司 : ")
            update.message.reply_text("公司 : "+match.group())
        
        i=0
        while i<len(respData):
            match = re.search(r'(?<=name="Deal">)([0-9]+\.[0-9]+)',respData[i])
            if match: break
            i+=1 

        if match:
            #update.message.reply_text("目前股價 : ")
            update.message.reply_text("目前股價 : "+match.group())    

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg" name="Change">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1 

        if match:
            update.message.reply_text("漲跌 : "+match.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg" name="ChangeRate">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1 

        if match:
            update.message.reply_text("漲跌% : "+match.group())    

        self.go_back2(update)

    def on_exit_state4(self, update):
        print('Leaving state4')
        
    def on_enter_state5(self, update):
        update.message.reply_text("最近交易日 爆量長紅 前五名 : ")

        url = 'http://www.wantgoo.com/';
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=1135
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('1 : '+match.group()+' '+match1.group())        

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('2 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('3 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('4 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('5 : '+match.group()+' '+match1.group())

        self.go_back3(update)

    def on_exit_state5(self, update):
        print('Leaving state5')

    def on_enter_state6(self, update):
        update.message.reply_text("最近瞬間暴漲 前五名 : ")

        url = 'http://www.wantgoo.com/';
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=0
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('1 : '+match.group()+' '+match1.group())        

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('2 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('3 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('4 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('5 : '+match.group()+' '+match1.group())

        self.go_back3(update)

    def on_exit_state6(self, update):
        print('Leaving state6')

    def on_enter_state7(self, update):
        update.message.reply_text("最近爆量長黑 前五名 : ")

        url = 'http://www.wantgoo.com/';
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=1450
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('1 : '+match.group()+' '+match1.group())        

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('2 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('3 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('4 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('5 : '+match.group()+' '+match1.group())

        self.go_back3(update)

    def on_exit_state7(self, update):
        print('Leaving state7')

    def on_enter_state8(self, update):
        update.message.reply_text("最近爆量長黑 前五名 : ")

        url = 'http://www.wantgoo.com/';
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=774
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('1 : '+match.group()+' '+match1.group())        

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('2 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('3 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('4 : '+match.group()+' '+match1.group())

        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<td class="lt"><a href="/stock/)(.+)(?=" target="_blank">)',respData[i])
            if match: break
            i+=1
        i+=1
        while i<len(respData):
            match1 = re.search(r'(?<=target="_blank">)(.+)(?=</a></td>)',respData[i])
            if match1: break
            i+=1 
        if match1:
            update.message.reply_text('5 : '+match.group()+' '+match1.group())

        self.go_back3(update)

    def on_exit_state8(self, update):
        print('Leaving state7')
        
    def on_enter_state9(self, update):
        update.message.reply_text("請輸入國際股市代碼")
        #update.message.reply_text(update.message.text)
        #self.go_back(update)

    def on_exit_state9(self, update):
        print('Leaving state9')
        
    def on_enter_state10(self, update):
        update.message.reply_text("您輸入的國際股市代碼是 : "+update.message.text)

        url = 'http://www.wantgoo.com/global/stockindex?StockNo='+update.message.text;
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=0
        while i<len(respData):
            match = re.search(r'(?<=<h3 class="idx-name">)(.+)(?=<span class="i idx-code">)',respData[i])
            if match: break
            i+=1    
        if match:
            #update.message.reply_text("公司 : ")
            update.message.reply_text("國際股市名稱 : "+match.group())
        
        i=0
        while i<len(respData):
            match = re.search(r'([0-9]+\.[0-9]+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            #update.message.reply_text("大盤指數 : ")
            update.message.reply_text("指數 : "+match.group())

        i=0
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            update.message.reply_text("漲跌 : "+match.group())
        i+=1
        while i<len(respData):
            match = re.search(r'(?<=<span class="chg">)(.+)(?=</span>)',respData[i])
            if match: break
            i+=1

        if match:
            update.message.reply_text("漲跌% : "+match.group())   

        self.go_back4(update)

    def on_exit_state10(self, update):
        print('Leaving state10')
        
    def on_enter_state11(self, update):
        update.message.reply_text("請輸入股市地區代碼")
        update.message.reply_text("台灣：TWSE/上海：SHA/深圳：SZA/香港：HSI/日本：NKY/南韓：KOSPI/新加坡：STI")
        update.message.reply_text("美國：USEQ/加拿大：TSE300/墨西哥：EXBOL/英國：UKX/德國：DAX/法國：CAC/瑞士：SMI")
        #update.message.reply_text(update.message.text)
        #self.go_back(update)

    def on_exit_state11(self, update):
        print('Leaving state11')
        
    def on_enter_state12(self, update):
        #update.message.reply_text("您輸入的國際股市代碼是 : "+update.message.text)

        url = 'http://www.wantgoo.com/global/rest?no='+update.message.text;
        respData = urllib.request.urlopen(url).read()
        respData =respData.decode('UTF-8')
        respData = re.split(r'[\n\r\f]+', respData)
        i=0
        match=1;
        while match:
            while i<len(respData):
                match = re.search(r'(?<=<td>)(.+)(?=</td>)',respData[i])
                if match: break
                i+=1    
            if match:
                update.message.reply_text("日期 : "+match.group())
            i+=1
            while i<len(respData):
                match = re.search(r'(?<=<td>)(.+)(?=</td>)',respData[i])
                if match: break
                i+=1    
            if match:
                update.message.reply_text("原因 : "+match.group())
            i+=1

        self.go_back5(update)

    def on_exit_state12(self, update):
        print('Leaving state11')
