# -*- coding: cp1252 -*-
import requests
import re
import ast
import threading
ego_list=[];orgasm=[]

email='' #put your email login 
password='' #the pssword
url='https://www.hentaiheroes.com/ajax.php'
cookies_login=requests.post('https://www.hentaiheroes.com/phoenix-ajax.php',data={'login':email,'password':password,'stay_online':'1','module':'Member','action':'form_log_in','call':'Member'})

cookies= cookies_login.cookies
def nextmission():
    
    print '\n',("*"*15),'nextmission',('*'*15)
    homeurl='https://www.hentaiheroes.com/home.html'
    r=requests.post(homeurl, cookies=cookies)
    #ez=re.findall('/battle.html(.*)^(?!disabled).*$',r.content)
    rt=('{}').format((''.join((re.findall('quest/(.*)(\d){1}',r.content)[0]))))

    data={'class':'Quest','action':'next','id_quest':rt}
    nextmission=requests.post(url, cookies=cookies,data=data)
    result=nextmission.content
    print result[-36:-1]
    return result

def startmission():
        
    while True:
        nextm=nextmission()
        if 'false' in nextm:
            break

def activities():
        
    r=requests.post('https://www.hentaiheroes.com/activities.html?tab=missions', cookies=cookies)
    s=re.findall('<button rel="finish" class="orange_text_button".* >',r.content)
    if len(s) == 1:
        print len(s),' activities est en cours d\'execution'
    elif len(s) == 0 and len(re.findall('mission_object',r.content)) != 0:
        
        idmission_re=re.findall('mission_object sub_block.*"id_mission":(.*),"d',r.content)
        id_member_mission_re=re.findall('mission_object sub_block.*"id_member_mission":(.*),"i',r.content)
        
        idmission=int(idmission_re[0].replace('"',""))
        id_member_mission=int(id_member_mission_re[0].replace('"',""))

        print idmission,id_member_mission
        data={'class':'Missions','action':'start_mission','id_mission':idmission,'id_member_mission':id_member_mission}
        do_mission=requests.post('https://www.hentaiheroes.com/ajax.php',data=data, cookies=cookies)
        recupure_mission=requests.post('https://www.hentaiheroes.com/ajax.php',data={'class':'Missions',
                                                                                     'action':'claim_reward','id_mission':idmission,
                                                                                     'id_member_mission':id_member_mission}, cookies=cookies)
        print recupure_mission.content
        if 'true' in recupure_mission.content:
            activities()
        print (do_mission.content[-15:-1]).decode(encoding='UTF-8')
        
    else:
        datagift={'class':'Missions','action':'give_gift'}
        givegift=requests.post('https://www.hentaiheroes.com/ajax.php',data=datagift, cookies=cookies)
 
        print givegift,' error'

def catchmoney():
    
    r=(requests.post('https://www.hentaiheroes.com/harem.html', cookies=cookies)).content
    grl=re.findall('{"id_girl":"(\d*)","level',r)
    print '\n',("*"*15),'catchmoney',('*'*15)
    for i in grl:
        data={'class':'Girl','who':i,'action':'get_salary'}
        r=requests.post(url, cookies=cookies,data=data)
        print i,' :',r.content[-15:-1]


def startfight():
    typeid='id_troll';typek='fight mission'
    home_url=(requests.get('https://www.hentaiheroes.com/home.html',cookies=cookies)).text
    quest_text=re.findall('href="/(.+?)\".*Quête en cours',home_url);quest_text="https://www.hentaiheroes.com/{0}".format(quest_text[0])
    energy_fight=int((re.findall('<span energy>(.*?)</span>',home_url))[1])


    world_url=requests.get(quest_text,cookies=cookies)
    world_text=re.findall('Aventure<span.*class="mapArrowBack_flat_icn"></span></a><span>&gt;</span><a class="back" href="(.*?)"\>',world_url.text);world_text="https://www.hentaiheroes.com/{0}".format(world_text[0])

    battle_id=re.findall('<a href="(.*?)" class="troll_world">Affronter',(requests.get(world_text,cookies=cookies)).text)
    battle_id="https://www.hentaiheroes.com/{0}".format(battle_id[0])
    for i in range(energy_fight):
        
        arene(battle_id,i,typek,typeid)




def arene(homeurl,i,typek,typeid):
    
    print '\n',('*'*15),typek,('*'*15),'\n'
    dic_who_type='who[{0}]'.format(typeid)
    arene_req=requests.post(homeurl, cookies=cookies)
    if typeid=='id_arena':
        arene_dict=re.findall('{"id_member":.*}',arene_req.content)
        if arene_dict :
            
            my_arene_dict=(ast.literal_eval((arene_dict)[0]))['ego'];arene_dict=(arene_dict)[1]
            arene_dict=ast.literal_eval(arene_dict)

    if typeid=='id_troll':
        arene_dict=(re.findall('{"id_troll":.*}',arene_req.content))[0]
        arene_dict=ast.literal_eval(arene_dict)
        my_arene_dict=arene_dict['ego']
    if arene_dict:
            
        arene_dict={'who['+k+']': v for k, v in arene_dict.items()};arene_dict.update({'class':'Battle','action':'fight','autoFight':'0'})
        ego_adv=arene_dict['who[ego]'];print ' [*] player : ',i,'\n [*] ego :',ego_adv,'\n'
        print "ego adversaire",ego_adv
        print "your ego ",my_arene_dict
            
        if  ego_adv <= my_arene_dict:
            
            are_combat=requests.post('https://www.hentaiheroes.com/ajax.php', cookies=cookies,data=arene_dict)
            
        elif ego_adv > my_arene_dict:
            print "this player strong than you"
    print '*'*20,'end of fighting ','*'*20

def startarene():
    typeid='id_arena';typek='arene'
    for i in range(0,3):
        homeurl='https://www.hentaiheroes.com/battle.html?id_arena={}'.format(i)
        arene(homeurl,i,typek,typeid)
    
activities()
thcatchmoney=threading.Thread(target=catchmoney()).start()
thstartmission=threading.Thread(target=startmission()).start()
thstartfight=threading.Thread(target=startfight()).start()
tharene=threading.Thread(target=startarene()).start()





