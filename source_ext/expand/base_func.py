import discord
import random

from custom_manger import command_manger
import data
from const import Strings, Docs
from db_manger import dbmanger
from web_find import SearchWord







class base_func:
    def __init__(self):
        self.color = 0x7ACDF4
        self.dbmanger = dbmanger()

    async def command_help(self,message):
        emb = discord.Embed(title='깔롤랭은 국룰입니다',description=Docs.help,colour=self.color)
        await message.channel.send(embed = emb)

    async def command_choice(self,message):
        chlist = message.content.split()
        chlist = chlist[2:]
        await message.channel.send("내가 뽑은건...!\n%s입니당!"%random.choice(chlist))

    # async def command_study(self, message):
    #     messages = message.content.split()[2]
    #     outputs = study_pathfind().find_study(messages)
    #     await message.channel.send("https://" +outputs)
    #     print(outputs)

        


    async def command_custom_send(self,message,prefixed = False):
        contents = message.content.split()
        search_msg = self.dbmanger.search_data('made_command','keycommand',contents[0])
        
        
    
    
        
    
    def command_잊어(self,message):#샤키야 key커맨드
        forget_word = message.content[6:]
        with open('snow_shaki_bot.txt','w', encoding='utf-8') as save_word:
            with open('snow_shaki_bot.txt','r', encoding='utf-8') as read_word:
                lines = read_word.readlines()
                for i in range(len(lines)):
                    if lines[i] in forget_word:
                        try:
                            lines = lines[:i] + lines[i+1:]
                        except IndexError:
                            pass
                save_word.writelines(lines)
        


        await message.channel.send("?\n형신이세요? 알려주고 잊으라하네ㅔ,,,")
        return
        
    

        

    def command_배워(self,message) :#샤키야 key커맨드 value커맨드
        word = message.content[7:].split(":")
        with open('snow_shaki_bot.txt', 'a', encoding= 'utf-8') as ff:
            ff.write('%s:;%s\n' % (word[0], word[1]))
        
        await message.channel.send("야랄 왜 나한테...")

    
    def command_사진(self,message):
        findg = message.content[9:]
        await message.channel.trigger_typing()
        image = SearchWord().get_image(findg)

        if image is None:
            await message.channel.send("이미지 불러오기를 실패했습니다")

        else:
            em = discord.Embed(title = "%s의 이미지 검색결과" %findg,colour = self.color)
            em.set_image(url = image)
        await message.channel.send(embed = em)
        
        
            
    def command_사전(self,message):
        findn = message.content[9:]
        findit = SearchWord().get_dic(findn)

        if findit is None:
            await message.channel.send("사전검색이 실패했습니다.")

        else:
            em2 = discord.Embed(title = "%s의 네이버사전검색 결과" % findn,description = "%s" %findit,colour = self.color)
            await message.channel.send(embed = em2)
    
    def command_굴러(self, message):
        await message.channel.send(random.choice(["데구르르 꽝","꽝 데구르르","데구르르 뎅강","ㄷㄱㄹㄹ ㄷㄱ","야랄,,, 너나 구르세요"]))
    
    def command_Hello(self,message):
        if message.content.split()[0] == "참수진":
            await message.channel.send("뒤져")
        else:
            pass
    
    
    # @bad_shaki
    # async def command_급식(self,message):
    #     keyword = message.content.split()[-1]
    #     today_meal = SearchWord().get_meal(keyword = "내일" if keyword == "내일" else "[오늘]" )

        
        
        
    #     morning = today_meal.index("[중식]")
    #     if "[석식]" in today_meal:
    #         afternoon = today_meal.index("[석식]")
        
    #     today_morning = '-\n'.join(today_meal[1:morning])
    #     if "[석식]" in today_meal:
    #         today_afternoon = '-\n'.join(today_meal[morning +1 :afternoon])
    #         today_dinner = '-\n'.join(today_meal[afternoon +1 :])

    #     else:
    #         today_afternoon = '-\n'.join(today_meal[morning+1:])
            
        
        
    #     emb = discord.Embed(title = "**%s의 급식 **" % ("[내일]" if keyword == "내일" else "[오늘]"), colour = self.color)
       
    #     emb.add_field(name = "[조식]", value = today_morning,inline = False)
    #     emb.add_field(name = "[중식]", value = today_afternoon, inline = False)
    #     if "[석식]" in today_meal:
    #         emb.add_field(name = "[석식]", value = today_dinner, inline = False)

    #     await message.channel.send(embed = emb)