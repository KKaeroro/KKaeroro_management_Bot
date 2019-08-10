import discord
import os
import asyncio
import re
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime

countG = 0
players = {}
queues= {}
musiclist=[]
mCount=1
searchYoutube={}
searchYoutubeHref={}
client = discord.Client()

def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()

@client.event
async def on_ready():
    print(f'Logged in as: {client.user.name}')
    print(f'With ID: {client.user.id}')
    print(f'Ready')
    await client.change_presence(game=discord.Game(name="(!디코페북 도움말) PLZ", type=1))

@client.event
async def on_member_join(member):
    fmt = '{1.name} 에 오신 걸 환영합니다! 모두 환영을 해주세요!, {0.mention} 님 규칙, 공지사항을 잘 보시고 이용해주셨으면 좋겠습니다!'
    channel = member.server.get_channel("609077700040196135")
    await client.send_message(channel, fmt.format(member, member.server))
    await client.send_message(member, "안녕하세요! Discord FaceBook 서버 BOT 입니다! \n서버에 오신 걸 진심으로 환영합니다! \n\n```\n자기소개 방에 알맞게 자기소개 해주시고 규칙 확인 후 이모지 클릭 바랍니다! 준비가 완료 되었으면 \n!회원가입 을 통해 관리자를 호출 하십시오! \n시간이 소요 될 수 있습니다!\n```\n회원가입 신청 채널에서 !회원가입 명령어를 쓰시길 바랍니다.")

@client.event
async def on_member_remove(member):
    channel = member.server.get_channel("609077700040196135")
    fmt = '{0.mention} 님이 서버에서 나가셨습니다.'
    await client.send_message(channel, fmt.format(member, member.server))
    

@client.event
async def on_message(message):
    if message.content.startswith("!안녕"):
        await client.send_message(message.channel, "안녕하세요! Discord Facebook 관리 봇인 캐로로 관리봇이라고 합니다!")

    if message.content.startswith('!경고부여'): # '!경고부여' 으로 시작하는 명령어를 감지한다면,
        if message.content[6:].startswith('<@'): # in 구문을 써도 되지만, 우린 아직 안배웠습니다. 여하튼 디스코드의 언급은 "<@(유저 ID)>"의 형태라서 "<@"으로 시작하면 유저를 언급했다고 봐도 됩니다.
            mention_id = re.findall(r'\d+', message.content) # 아래와 같은 절차를 거쳐 경고를 부여할 유저의 ID를 추출합시다.(사실상 message.content라는 변수에서 숫자만 뽑아내는겁니다.) re라는 모듈에 대한 강좌는 추후 진행하겠습니다.
            mention_id = mention_id[0]
            mention_id = str(mention_id)
            # 파일명은 코드 짜는 사람 마음이지만, 우리는 "(서버 ID)_(유저 ID).txt" 로 짓겠습니다.
            if os.path.isfile(message.server.id + " _ " + mention_id + ".txt"): # 해당 유저의 경고파일이 없으면 만들어야 하기에, 경고 파일이 있는지 확인합시다.
                f = open(message.server.id + " _ " + mention_id + ".txt", 'r') # 대상 유저의 경고수를 먼저 받아옵시다.
                past_warn = f.read() # past_warn이라는 변수에 예전 경고를 집어넣습니다.
                f.close() # 파일을 닫아줍시다. 원래는 안써도 무방하지만, 닫는것이 낫습니다. 그 이유는 좀있다 설명하도록 합죠.
                now_warn = int(past_warn) + 1 # 그리고 1을 경고에 추가로 넣어줍시다.
                now_warn = str(now_warn) # 문자열 형태로 바꿔줍니다. 그 이유는 나중에 설명하겠습니다.
                f = open(message.server.id + " _ " + mention_id + ".txt", 'w') # 파일을 쓰기 권한으로 열어줍니다. (여담이지만, 쓰기 권한으로 열면 파일을 알아서 만듭니다. 그대신, 기존에 파일이 있으면 지우고 만들어버리니 주의합시다.)
                f.write(now_warn) # 현재 경고를 넣어줍니다.
                f.close() 
                await client.send_message(message.channel, "<@" + message.author.id + "> 님이 <@" + mention_id + "> 님께 경고 1회를 부여했습니다!\n<@" + mention_id + "> 님의 경고는 `" + now_warn + "회` 입니다!") # 알림을 보냅시다. `<<이것은 마크다운이라고 하는 문법의 일종입니다. 이것을 채팅 칠 때 좌|우에 기입하면 박스가 생깁니다.
            else:
                f = open(message.server.id + " _ " + mention_id + ".txt", 'w') # 우선 만들고 시작해야죠. 쓰기 권한으로 열어봅시다. 
                f.write("1") # 경고 1회를 추가합시다.
                f.close() 
                await client.send_message(message.channel, "<@" + message.author.id + "> 님이 <@" + mention_id + "> 님께 경고 1회를 부여했습니다!\n<@" + mention_id + "> 님의 경고는 `1회` 입니다!") # 알림을 보냅니다.
        else: # 언급이 안되었다면,
            await client.send_message(message.channel, "유저를 언급하여 주세요!") # 유저를 언급해달라는 메시지를 보냅니다.
    
    if message.content.startswith('!말하기'):
        await client.send_message(message.channel, '메세지 내용을 15초내로 입력해주세요!')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)
         
        if msg is None:
            await client.send_message(message.channel, '15초내로 입력해주세요. 다시시도: !말하기')
            return
        else:
            await client.send_message(message.channel, msg.content)

    if message.content.startswith("!회원가입"):
        channel = message.server.get_channel("609063113970417664")
        await client.send_message(channel, "@here \n" + "<@" + message.author.id + "> 님이 회원가입을 요청하셨습니다.\n필요한 부분에 충족했는지 잘 확인 후 역할 지급 부탁드립니다.\n1. 자기소개가 잘 써져있는가?\n2. 규칙에 이모지를 클릭했는가.\n이것에 충족하면 드리세요.")
        await client.send_message(message.channel, "회원가입이 요청되었습니다. 잠시만 기다려주시면 채널이 열리게됩니다 계속 열람이 안되면 ✨안내원✨을 언급해주세요.")
    if message.content.startswith("!칭호신청"):
        channel = message.server.get_channel("609084916503805972")
        file = openpyxl.load_workbook("칭호건의.xlsx")
        sheet = file.active
        learn = message.content.split(" ")
        for i in range(1, 3000):
            if sheet["A" + str(i)].value == "-":
                sheet["A" + str(i)].value = learn[1]
                await client.send_message(message.channel, "칭호 추가 신청 목록에 등록이 되었습니다!\n서버관리자에게 호출이 되었습니다!")
                await client.send_message(channel, "<@" + message.author.id + "> 님이 칭호신청을 하였습니다.")
                break
        file.save("칭호건의.xlsx")
    if message.content.startswith("!유저정보"):
        date = datetime.datetime.utcfromtimestamp(((int(message.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0x00ff00)
        embed.add_field(name="이름", value=message.author.name, inline=True)
        embed.add_field(name="서버닉네임", value=message.author.display_name, inline=True)
        embed.add_field(name="가입일", value=str(date.year) + "년" + str(date.month) + "월" + str(date.day) + "일", inline=True)
        embed.add_field(name="아이디", value=message.author.id, inline=True)
        embed.set_thumbnail(url=message.author.avatar_url)
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith("!디코페북 도움말"):
        channel = message.channel
        embed = discord.Embed(
            title = '★Discord FaceBook 필요 서버 명령어 1/2.★',
            description = '★많은 명령어들이 소개 되어 있습니다!★ \n ======================================',
            colour = discord.Colour.blue()
        )
    
        #embed.set_footer(text = '끗')
        dtime = datetime.datetime.now()
        #print(dtime[0:4]) # 년도
        #print(dtime[5:7]) #월
        #print(dtime[8:11])#일
        #print(dtime[11:13])#시
        #print(dtime[14:16])#분
        #print(dtime[17:19])#초
        embed.set_footer(text=str(dtime.year)+"년 "+str(dtime.month)+"월 "+str(dtime.day)+"일 "+str(dtime.hour)+"시 "+str(dtime.minute)+"분 "+str(dtime.second)+"초")
        #embed.set_footer(text=dtime[0:4]+"년 "+dtime[5:7]+"월 "+dtime[8:11]+"일 "+dtime[11:13]+"시 "+dtime[14:16]+"분 "+dtime[17:19]+"초")
        embed.add_field(name = '!안녕', value = '서버 봇이 인사합니다!',inline = False)
        embed.add_field(name = '!말하기', value = '10초 동안 말할 내용을 입력하면 봇이 똑같이 따라 합니다!',inline = False)
        embed.add_field(name = '!회원가입', value = '회원가입 신청을 합니다! (하신 분들이 만약 하셨다면 경고를 드립니다.)',inline = False)
        embed.add_field(name = '!유저정보', value = '나의 유저정보를 봅니다',inline = False)
        embed.add_field(name = '!칭호신청', value = '칭호신청 방에서만 이용해주세요. 칭호 신청을 할 수 있습니다!',inline = False)
        embed.add_field(name = '!초대링크신청', value = '초대링크신청방에서만 이용해주세요. 초대링크 신청을 할 수 있습니다!',inline = False)
        embed.add_field(name = '!투표하기', value = '투표를 시작합니다! (관리자 Only) (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!배그각', value = '배그각을 알려줍니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!주사위', value = '주사위를 굴려봅니다! (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!날씨보기', value = '!날씨 원하는지역 을 입력하면 날씨를 볼 수 있습니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!언급', value = '@everyone을 사용합니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!실검 or !실시간검색어', value = '네이버 실시간 검색어를 알려드립니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!영화순위', value = '네이버 영화에서 영화순위를 알려드립니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!복권', value = '복권 숫자를 램덤으로 알려드립니다. (이벤트 개최 가능성이 있습니다!) (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!타이머', value = '!타이머 (숫자) 타이머를 시작합니다. (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!제비뽑기', value = '!제비뽑기 (숫자) 를 입력하면 제비뽑기를 실행합니다! (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!이모티콘', value = '랜덤으로 이모티콘을 보냅니다! (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!반가워', value = '기능 봇이 인사를 합니다! (디코페북 기능 BOT)',inline = False)
        embed.add_field(name = '!재생', value = '!노래 노래이름 을 입력하시면 노래를 틀어 줍니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!디코페북 도움말2', value = '다음 도움말을 보려면 이 명령어를 치세요.',inline = False)
    
        await client.send_message(channel,embed=embed)
    if message.content.startswith("!디코페북 도움말2"):
        channel = message.channel
        embed = discord.Embed(
            title = '★Discord FaceBook 필요 서버 명령어 2/2 .★',
            description = '★많은 명령어들이 소개 되어 있습니다!★ \n ======================================',
            colour = discord.Colour.blue()
        )
    
        #embed.set_footer(text = '끗')
        dtime = datetime.datetime.now()
        #print(dtime[0:4]) # 년도
        #print(dtime[5:7]) #월
        #print(dtime[8:11])#일
        #print(dtime[11:13])#시
        #print(dtime[14:16])#분
        #print(dtime[17:19])#초
        embed.set_footer(text=str(dtime.year)+"년 "+str(dtime.month)+"월 "+str(dtime.day)+"일 "+str(dtime.hour)+"시 "+str(dtime.minute)+"분 "+str(dtime.second)+"초")
        #embed.set_footer(text=dtime[0:4]+"년 "+dtime[5:7]+"월 "+dtime[8:11]+"일 "+dtime[11:13]+"시 "+dtime[14:16]+"분 "+dtime[17:19]+"초")
    
        embed.add_field(name = '!일시정지', value = '노래를 잠시 중지 시킵니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!스킵', value = '노래를 스킵 시킵니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!반복', value = '!반복 On/Off 노래 반복을 합니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!정지', value = '노래를 완전히 정지 합니다. 플레이리스트도 제거 됩니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!다시재생', value = '일시정지된 노래를 다시 플레이 합니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!일시정지', value = '노래를 잠시 중지 시킵니다. (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!queue', value = '재생목록을 확인 합니다. (한글화 안되어 있음) (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '!가사', value = '가사를 보여줍니다 (페북디코 뮤직 BOT)',inline = False)
        embed.add_field(name = '로로야', value = '로로야를 이용해서 봇이랑 이야기 해보세요. (페북디코 로로야)',inline = False)
        embed.add_field(name = '!rank', value = '자신의 레벨을 봅니다. (페북디코 미유기)',inline = False)
        embed.add_field(name = '!출첵', value = '출석체크를 합니다. (페북디코 마냥이)',inline = False)
        embed.add_field(name = '!청소', value = '!청소 (숫자) 청소를 합니다. 관리자가 없으면 자신의 메세지만 삭제 합니다. (페북디코 마냥이)',inline = False)
        embed.add_field(name = '.궁합', value = '궁합을 볼 사람을 언급을 해주세요! (디코페북 궁합 BOT)',inline = False)
        embed.add_field(name = '명령어가 많이 없는 건 기분 탓입니다.', value = '페북디코 관리 봇은 관리자를 위한 명령어 밖에 없어 실제 유저 분들이 쓸 수 있는 기능은 없습니다. 일부 봇들의 명령어도 섞여 있습니다.',inline = False)
    
        await client.send_message(channel,embed=embed)



    if message.content.startswith("!초대링크신청"):
        channel = message.server.get_channel("609085004324274186")
        await client.send_message(channel, "@here \n" + "<@" + message.author.id + "> 님이 초대링크를 요청하셨습니다.")
        await client.send_message(message.channel, "초대링크를 관리자한테 요청하였습니다. 개인디코로 알려드립니다. 초대링크는 1시간 후 자동으로 삭제가 됩니다.")


client.run('NjA2MTg3MzQ2Njg1MDY3Mjk0.XUwdCw.-xZa2P-PZS6AhSQhKyOPmWbLv8Q')
