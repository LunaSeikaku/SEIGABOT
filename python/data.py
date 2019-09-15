# By LunaSeikaku (Robbie Munro) 15/09/19
import csv # for saving and loading data at start and end of running
import random as rng # for decisions
import copy as cop # for object instances ie. in battle to avoid changing the underlying touhou values
from PIL import Image # for horizontal !war team image creation
import numpy as np # see above
import matplotlib.pyplot as plt #for balance graphing
class Player: # Info on a discord user
    def __init__(self,i,nm,se="Empty",fr=["Empty","Empty","Empty"],br=["Empty","Empty","Empty"],bp=["Empty"],po=0):
        self.id = i
        self.name = nm
        self.secretary = se
        self.team = [br,fr]
        self.backpack = bp
        self.points = po
    def gainPoints(self,p):
        self.points+=p
        self.save()
        return self.name+" gained "+str(p)+" points!|They now have "+str(self.points)+" points!|***"
    def losePoints(self,p):
        self.points-=p
        self.save()
        return self.name+" used "+str(p)+" points!|They now have "+str(self.points)+" points!|***"
    def getName(self):return self.name
    def setSecretary(self,newsec):
        sm = ""
        for i in self.backpack: # if sorted by rarity, first item in list with be highest rated version of that 2hu
            if i.name==newsec:
                if self.secretary!="Empty":sm="Your previous Secretary, "+self.secretary.name+", has been shuffled into your Backpack."
                self.secretary = i#.name#cop.copy(i)
                self.save()
                return "Your Secretary has been set to "+i.name+"|"+sm+"|***>"+i.name+">Smug***"
        return "INPUT ERROR:|'"+newsec+"' is not a valid Touhou name from your Backpack!|"
    def getSecretary(self):return self.secretary
    def getTeam(self):return self.team
    def clearTeam(self): # empty entries from Team into Backpack
        for i in self.team[0]:
            if i!="Empty":self.appendBackpack(i)
        for i in self.team[1]:
            if i!="Empty":self.appendBackpack(i)   
        self.team = [["Empty","Empty","Empty"],["Empty","Empty","Empty"]]
        self.save()
    def setTeam(self,fr,br):
        # check Team is all in Backpack:
        indices = []
        for i in range(len(fr)):
            for j in range(len(self.backpack)): # check for rarity too! (if sorted by rarity, don't need to)
                if fr[i].name==self.backpack[j].name:
                    fr[i].rarity=self.backpack[j].rarity
                    indices.append(j)
                    break
        for i in range(len(br)):
            for j in range(len(self.backpack)):
                if br[i].name==self.backpack[j].name:
                    br[i].rarity=self.backpack[j].rarity
                    indices.append(j)
                    break
        if len(indices)<6: return "INPUT ERROR:|Choose 6 from your Backpack!|"
        
        # if here then all 6 Touhou are present in Backpack so remove from Backpack:
        indices = sorted(indices,reverse=True) # highest to lowest to avoid index removal clashing
        for i in indices:
            del self.backpack[i]
        # now add Touhou removed from Backpack to Team and display them:
        for i in self.team[0]:
            if i!="Empty":self.backpack.append(i)
        for i in self.team[1]:
            if i!="Empty":self.backpack.append(i)
        self.sortBackpack()
        self.team = [fr,br]
        #
        #self.sortTeam()
        self.save()
        return None
    def sortTeam(self): # needed? #debug?
        self.team[0].sort(key=lambda x:x.name)
        self.team[1].sort(key=lambda x:x.name)
        #self.team = [sorted(self.team[0]),sorted(self.team[1])] # sort by names
    def appendFrontline(self,t):
        if self.team[1][0]=="Empty":self.backpack=[t] # if empty list, remake list with new entry
        else:self.team[1].append(t)
        if len(self.team[1])>3: # if longer than 3, move first item in backline to backpack
            t = self.team[1].pop(0)
            self.appendBackpack(t)
        self.sortTeam()
        self.save()
    def removeFrontline(self,i):
        self.team[1].remove(i)
        if len(self.team[1])<1:self.team[1].append("Empty")
        self.sortTeam()
        self.save()
    def appendBackline(self,t):
        if self.team[0][0]=="Empty":self.backpack=[t] # if empty list, remake list with new entry
        else:self.team[0].append(t)
        if len(self.team[0])>3: # if longer than 3, move first item in frontline to backpack
            t = self.team[0].pop(0)
            self.appendBackpack(t)
        self.sortTeam()
        self.save()
    def removeBackline(self,i):
        self.team[0].remove(i)
        if len(self.team[0])<1:self.team[0].append("Empty")
        self.sortTeam()
        self.save()
    def getBackpack(self):return self.backpack
    def appendBackpack(self,t):
        s = ""
        rs = ["N","SR","SSR","USSR"]
        if self.backpack[0]=="Empty":self.backpack=[t]
        else:
            for i in self.backpack:
                if i.name==t.name: # it's a Duplicate:
                    for j in range(len(rs)): # convert rarities to ints:
                        if rs[j]==i.rarity:
                            a = j
                        if rs[j]==t.rarity:
                            b = j
                    try:
                        i.rarity=rs[a+b+1] # try move to next higher tier
                        s = "Duplicate!|Your "+t.rarity+" "+t.name+" is now a "+i.rarity+" "+t.name+"!|***"
                    except:
                        i.rarity="USSR"
                        if i.rarity==t.rarity:s = "Duplicate!|Your "+t.rarity+" "+t.name+" is now a "+i.rarity+" "+t.name+"!|***"
                        else:s = "Duplicate!|Your "+i.rarity+" "+t.name+" is already max rarity!|***" # gain credits?
                    break
            if s=="":self.backpack.append(t) # if s=="" after Backpack searched, then duplicate not found, so add as is
        self.sortBackpack()
        self.save()
        return s
    def removeBackpack(self,i):
        self.backpack.remove(i) # use inheritance for removal
        self.sortBackpack()
        self.save()
    def sortBackpack(self):#self.backpack.sort(key=lambda x:(len(x.rarity), x.name)) # sort by names
        self.backpack.sort(key=lambda x:x.name)
        self.backpack.sort(key=lambda x:len(x.rarity),reverse=True)
    def unparsedBackpack(self):
        bp = []
        if self.backpack[0]=="Empty":return "Empty"
        for i in self.backpack:
            bp.append(i.name+"|"+i.rarity)
        return "***".join(bp)
    #def getFrontrow(self):return self.frontrow
    #def getBackrow(self):return self.backrow
    #def toString(self):return("----------\nName: "+self.name+"\nSecretary: "+self.secretary+"\nFront Row: "+self.frontrow[0]+", "+self.frontrow[1]+", "+self.frontrow[2]+"\nBack Row: "+self.backrow[0]+", "+self.backrow[1]+", "+self.backrow[2]+"\n----------")
    def getStringTouhou(self,save):
        try:
            sec = self.secretary.name # for visual output purposes only
            if save:sec+="|"+self.secretary.rarity # for save purposes only
        except:
            sec = self.secretary # if "Empty"
        l = []
        for i in self.team[1]:
            try:
                j = i.name
                if save:j+="|"+i.rarity
                l.append(j)
            except:
                l.append(i)
        for i in self.team[0]:
            try:
                j = i.name
                if save:j+="|"+i.rarity
                l.append(j)
            except:
                l.append(i)
        return sec,l
    def save(self):
        # find entry in plrs.csv, make copy of it and replace Player, then overwrite entire csv
        l = []
        # Read all data from the csv file.
        with open('./csv/plrs.csv', 'r') as b:
            bs = csv.reader(b)
            l.extend(bs)

        # Find line to replace
        index = 0
        for i in range(1,len(l)):
            if int(l[i][0])==self.id:index=i 

        # data to override in the format {line_num_to_override:data_to_write}.
        sec,m = self.getStringTouhou(True)
        s = self.unparsedBackpack()
        replace = {index:[self.id,self.name,sec,m[0],m[1],m[2],m[3],m[4],m[5],s,self.points]}
        #replace = {index:[self.id,self.name,self.secretary,self.team[1][0],self.team[1][1],self.team[1][2],self.team[0][0],self.team[0][1],self.team[0][2],s]}
        
        # Write data to the csv file and replace the line in the replace dict.
        with open('./csv/plrs.csv', 'w', newline='') as b:
            w = csv.writer(b)
            for line, row in enumerate(l):
                 data = replace.get(line, row)
                 w.writerow(data)
    def toString(self):
        sec,l = self.getStringTouhou(False)
        return("----------\nName: "+self.name+"\nSecretary: "+sec+"\nFront Row: "+l[0]+", "+l[1]+", "+l[2]+"\nBack Row: "+l[3]+", "+l[4]+", "+l[5]+"\n----------")
class Spellcard: # Info on an attack a Touhou uses in Battle
    def __init__(self,i,nm,mg,el,sd,md,ld,ac,di,mo):
        self.id = i
        self.name = nm
        self.difficulty = "NORMAL" # Easy/Normal/Hard/Lunatic, set after creation of card
        self.magic = mg # bool: true if magic attack, false if physical attack
        self.elements = el
        self.DMG = [sd,md,ld]
        #self.SDMG = sd # short range (icicle fall = 0)
        #self.MDMG = md # medium range
        #self.LDMG = ld # long range
        self.accuracy = ac
        self.difficulties = di
        self.effects = mo # list of status effect objects
        self.grades = [] # simply for show
        self.addGrade(sd,50,40,30,20)
        self.addGrade(md,50,40,30,20)
        self.addGrade(ld,50,40,30,20)
        self.addGrade(ac,90,80,70,60)
        # extras here
    def getID(self):return self.id
    def getName(self):return self.name
    def getDifficulty(self):return self.difficulty
    def setDifficulty(self):
        r = rng.randrange(0,101)
        if (r > 99):
            self.difficulty = "LUNATIC"
        elif (r > 90):
            self.difficulty = "HARD"
        elif (r > 65):
            self.difficulty = "NORMAL"
        else:
            self.difficulty = "EASY"
    def getMagic(self):return self.magic
    def getMajor(self):return self.major
    def getMinor(self):return self.minor
    def getDMG(self):return self.DMG
    #def getSDMG(self):return self.SDMG
    #def getMDMG(self):return self.MDMG
    #def getLDMG(self):return self.LDMG
    def getAccuracy(self):return self.accuracy
    def getGrades(self):return self.grades
    def addGrade(self,x,s,a,b,c):
        if x>=s:self.grades.append("S")
        elif x>=a:self.grades.append("A")
        elif x>=b:self.grades.append("B")
        elif x>=c:self.grades.append("C")
        else:self.grades.append("D")
    def toGrade(self):return("----------\nShort Damage: "+self.grades[0]+"\nMedium Damage: "+self.grades[1]+"\nLong Damage: "+self.grades[2]+"\nAccuracy: "+self.grades[3])
    def toString(self):return("----------\nName: "+self.name+"\nDifficulty: "+self.difficulty+"\nMagic: "+str(self.magic)+"\nMajor Element: "+self.major+"\nMinor Element: "+self.minor+"\nShort Range Damage: "+str(self.DMG[0])+"\nMedium Range Damage: "+str(self.DMG[1])+"\nLong Range Damage: "+str(self.DMG[2])+"\nAccuracy: "+str(self.accuracy)+"\n----------")
class Touhou: # Information on the characters controlled by the Player that fight each other in Battle
    def __init__(self,i,nm,gm,st,ds,mj,mi,hp,ph,mp,do,im,sp): # remember to update def __copy__ and Data when you update this!
        # Info
        self.id = i
        self.name = nm
        self.game = gm
        self.stage = st
        self.description = ds
        self.major = mj
        self.minor = mi
        self.rarity = "N"
        # Stats
        self.HP = hp # health they start a Battle with
        self.PHATK = ph # base damage modifer for physical Spellcards
        self.MPATK = mp # base damage modifer for magical Spellcards
        self.accuracy = 10
        self.dodge = do # percentage chance out of 100 to evade damage, +10 grazes
        self.grades = [] # simply for show
        self.addGrade(hp,1250,1000,750,500)
        self.addGrade(ph,50,40,30,20)
        self.addGrade(mp,50,40,30,20)
        self.addGrade(do,40,30,20,10)
        # Spellcards
        self.spellcards = sp #[[Easy],[Normal],[Hard],[Lunatic]]
        # Status Effects
        self.effects = []
        self.immunities = im # ints representing self.status methods for lingering effects from damage
        self.turns = 1 # how many attacks they deal (could add startturns if adding multiattack touhous)
    def __copy__(self): # to ensure original values are kept intact and not passed between fights
        return type(self)(self.id,self.name,self.game,self.stage,self.description,self.major,self.minor,self.HP,self.PHATK,self.MPATK,self.dodge,self.immunities,self.spellcards)
    def getID(self):return self.id
    def getName(self):return self.name
    def getGame(self):return self.game
    def getStage(self):return self.stage
    def getDescription(self):return self.description
    def getMajor(self):return self.major
    def getMinor(self):return self.minor
    def getRarity(self):return self.rarity
    def setRarity(self,x):self.rarity = x#self.difficulty = x WTF
    def getHP(self):return self.HP
    def getPHATK(self):return self.PHATK
    def getMPATK(self):return self.MPATK
    def getDodge(self):return self.dodge
    def getGrades(self):return self.grades
    def addGrade(self,x,s,a,b,c):
        if x>=s:self.grades.append("S")
        elif x>=a:self.grades.append("A")
        elif x>=b:self.grades.append("B")
        elif x>=c:self.grades.append("C")
        else:self.grades.append("D")
    def toGrade(self):return("----------\nHealth: "+self.grades[0]+"\nPhysical Attack: "+self.grades[1]+"\nMagical Attack: "+self.grades[2]+"\nDodge: "+self.grades[3]+"\n----------")
    def getSpellcardsbydifficulty(self,i):return self.spellcards[i]
    def getSpellcard(self,i,j):return self.spellcards[i][j]#
    def getAnyAttack(self):return rng.choice(rng.choice(self.spellcards))
    def getAttack(self,i):return rng.choice(self.spellcards[i])
    def setDifficulties(self):
        for i in range(len(self.spellcards)):
            for j in self.spellcards[i]:
                j.setDifficulty()
    def getElementConversion(self,e): #e = self.major OR self.minor
        c = {0:"Void",1:"Life",2:"Death",3:"Light",4:"Dark",5:"Ichor",6:"Fire",7:"Water",8:"Wind",9:"Earth",
            10:"Synthetic",11:"Spirit",12:"Joy",13:"Fortitude",14:"Fear",15:"Despair",16:"Almighty",17:"Holy",18:"Corruption",19:"Unholy"}
        return c[e]
    def toString(self,emotion="Default"):
        sp = "Easy:\n" # cancer
        for i in self.getSpellcardsbydifficulty(0):
            sp+=i.name+"\n"
        sp += "\nMedium:\n"
        for i in self.getSpellcardsbydifficulty(1):
            sp+=i.name+"\n"
        sp += "\nHard:\n"
        for i in self.getSpellcardsbydifficulty(2):
            sp+=i.name+"\n"
        sp += "\nLunatic:\n"
        for i in self.getSpellcardsbydifficulty(3):
            sp+=i.name+"\n"
        sp = "Spellcards:|"+sp+"|"
        return("Name: "+self.name+"\nGame: "+str(self.game)+"\nStage: "+str(self.stage)+"\nRarity: "+self.rarity+
               "|Description: "+self.description+"|***>"+self.name+">"+emotion+"***"+
               "\nMajor Element: "+self.getElementConversion(self.major)+"\nMinor Element: "+self.getElementConversion(self.minor)+"|Health: "+str(self.HP)+"\nPhysical Attack: "+str(self.PHATK)+"\nMagical Attack: "+str(self.MPATK)+"\nDodge: "+str(self.dodge)+"|"+
               sp)
class Effect:
    def __init__(self,i,ta,h,l,tu,c,te):
        self.id = i # for calling procs most likely
        self.target = ta # true if given to defender, otherwise given to self aka attacker
        self.hit = h # is displayed eg 'Blinded!'
        self.lingerhit = l # is displayed eg 'continued to be Blinded!'
        self.turns = tu # turns the effect lasts for (reset if effected again)
        self.constant = c # affect occurs everytime they attack eg poison # 1 to 0 if no, otherwise 2
        self.team = te
        # elemental text list? eg 'X was blinded by the Light'
    def __copy__(self):
        return type(self)(self.id,self.target,self.hit,self.lingerhit,self.turns,self.constant,self.team)
class Element:
    def __init__(self,nm,i,li):
        self.name = nm
        self.index = i # used to find position in other elements' lists
        self.list = li # list of modifiers to damage output ala water against fire = 2 aka 2x
class Stat: #holds a single statistic for one player's forces
    def __init__(self,v,t,n):
        self.value = v
        self.title = t
        self.name = n
class Data:
    def __init__(self):
        self.players = [] # discord shit, remember to export data when possible to import on reboot
        self.spellcards = []
        self.touhous = []
        self.touhousbystage = [[],[],[],[],[],[],[]]
        self.statuses = []
        self.elements = []
        try:
            with open('./csv/fecs.csv', 'r') as fi:
                next(fi)
                f = fi.readlines()
                r = csv.reader(f)
                for i in r:
                    self.statuses.append(Effect(int(i[0]),int(i[1]),i[2],i[3],int(i[4]),int(i[5]),int(i[6])))
        except Exception as e:
            print(e)
           #print ("Error! Is fecs.csv in the csv folder?")
        try:
            with open('./csv/eles.csv', 'r') as fi:
                next(fi)
                f = fi.readlines()
                r = csv.reader(f)
                c = 0
                for i in r:
                    self.elements.append(Element(i[0],c,[int(i[1]),int(i[2]),int(i[3]),int(i[4]),int(i[5]),int(i[6]),int(i[7]),int(i[8]),int(i[9]),int(i[10]),int(i[11]),int(i[12]),int(i[13]),int(i[14]),int(i[15]),int(i[16]),int(i[17]),int(i[18]),int(i[19]),int(i[20])]))
                    c+=1
        except:
           print ("Error! Is eles.csv in the csv folder?")
        try:
            with open('./csv/spls.csv', 'r') as fi:
                next(fi)
                f = fi.readlines()
                r = csv.reader(f)
                for i in r:
                    effects = []
                    elementIDs = i[3].split("_") # Create list of element IDs owned by this touhou
                    effectIDs = i[9].split("_") # Create list of spellcard IDs owned by this touhou
                    for j in effectIDs:
                        if j!='0':
                            e = self.getEffectByID(int(j))
                            effects.append(e)
                    self.spellcards.append(Spellcard(int(i[0]),i[1],int(i[2]),elementIDs,int(i[4]),int(i[5]),int(i[6]),int(i[7]),i[8],effects))
        except:
           print ("Error! Is spls.csv in the csv folder?")
        try:
            with open('./csv/2hus.csv', 'r') as fi:
                next(fi)
                f = fi.readlines()
                r = csv.reader(f)
                for i in r:
                    immunities = i[11].split("_")
                    for j in range(len(immunities)):immunities[j] = int(immunities[j])
                    cards = [[],[],[],[]]
                    cardIDs = i[12].split("_") # Create list of spellcard IDs owned by this touhou
                    for j in cardIDs:
                        c = self.getSpellcardByID(int(j))
                        diffIDs = c.difficulties.split("_") # Create list of difficulties owned by this spellcard
                        for k in range(len(diffIDs)):
                            cards[int(diffIDs[k])].append(c)
                    t = Touhou(int(i[0]),i[1],int(i[2]),int(i[3]),i[4],int(i[5]),int(i[6]),int(i[7]),int(i[8]),int(i[9]),int(i[10]),immunities,cards)
                    self.touhous.append(t)
                    self.touhousbystage[int(i[3])-1].append(t)
        except:
            print ("Error! Is 2hus.csv in the csv folder?")
        try:
            with open('./csv/plrs.csv', 'r') as fi:
                next(fi)
                f = fi.readlines()
                r = csv.reader(f)
                for i in r:
                    # Alice|N -> [N Alice 2hu object]:
                    # Secretary
                    if i[2]=="Empty":sec=i[2]
                    else: # grab 2hu
                        s = i[2].split("|")
                        sec = cop.copy(self.getTouhouByName(s[0]))
                        sec.rarity = s[1]
                    # Team
                    tea = []
                    for j in range(3,9):
                        if i[j]=="Empty":tea.append("Empty") # debug?
                        else:
                            s = i[j].split("|")
                            t = cop.copy(self.getTouhouByName(s[0]))
                            t.rarity = s[1]
                            tea.append(t)
                    fr = [tea[0],tea[1],tea[2]]
                    br = [tea[3],tea[4],tea[5]]
                    # Backpack
                    if i[9][:5]=="Empty":bp=[i[9]]
                    else:
                        bp = []
                        ts = i[9].split("***")
                        for j in ts:
                            s = j.split("|")
                            t = cop.copy(self.getTouhouByName(s[0]))
                            t.rarity = s[1]
                            bp.append(t)
                    self.players.append(Player(int(i[0]),i[1],sec,fr,br,bp,int(i[10]))) #int(i[0])???
        except:
           print ("Error! Is plrs.csv in the csv folder?")
    def getPlayers(self):return self.players
    def parseUsername(self,u,getname=0): # getname 0 when id output is required, otherwise 1 (it's a handy index as well as a bool)
        # input Discord mention, get either their username or id:
        if u[:1]=='@':u=u[1:] # remove @ symbol when mentioning other Discord users
        u = u.split('#') # separate mention into username and id
        if len(u)==1:u[0] = int(u[0][-7:-1]) # for bots that end in >
        else:u[0] = int(u[0][-6:]) # str XXXXXXXXXXXXXYYYYYY => int YYYYYY
        return u[getname] # outputs either username or id depending on whether getname is 0 or 1
    def getPlayerByID(self,i):
        for j in self.players:
            if (j.id == i):
                return j # ends here if found so as to not write to file unnecessarily
        return None # see below:
    def getPlayerByUsername(self,u):
        # write new player to plrs.csv, then grab this entry
        i = self.parseUsername(u) # get index
        p = self.getPlayerByID(i) # get player if their index is already on file
        if p!=None:return p # return player if found, otherwise continue method
        try:
            # write new entry to file with new discord user's id and username
            p = [i,self.parseUsername(u,1),"Empty","Empty","Empty","Empty","Empty","Empty","Empty","Empty",100]
            with open('./csv/plrs.csv', 'a', newline='') as fi:
                w = csv.writer(fi)
                w.writerow(p)
            fr = [p[3],p[4],p[5]]
            br = [p[6],p[7],p[8]]
            if p[9][:5]=="Empty":bp=[p[9]]
            else: # grab 2hu
                bp = []
                ts = p[9].split("***")
                for j in ts:
                    s = j.split("|")
                    t = self.getTouhouByName(s[0])
                    t.rarity = s[1]
                    bp.append(t)
            self.players.append(Player(int(p[0]),p[1],p[2],fr,br,bp,int(p[10]))) #int(i[0])???
            return self.players[len(self.players)-1]
        except:
            print ("Error! Is plrs.csv in the csv folder?")
    def getEffectByID(self,i):
        for j in self.statuses:
            if (j.id == i):
                return j
    def getSpellcards(self):return self.spellcards
    def getSpellcardByID(self,i):
        for j in self.spellcards:
            if (j.id == i):
                return j
    def getTouhous(self):return self.touhous
    def getTouhouByID(self,i):
        for j in self.touhous:
            if (j.id == i):
                return j
    def getTouhouByName(self,i):
        for j in self.touhous:
            if (j.name == i):
                return j
    def newhu(self,mini=0,maxi=101):
        # Get a character and it's rarity. Set maxi to the stage minimum level values to cap the possible stage of Touhou
        r = rng.randrange(0,101)
        if (r > 99):
            rarity = "USSR"
        elif (r > 90):
            rarity = "SSR"
        elif (r > 65):
            rarity = "SR"
        else:
            rarity = "N"
        r = rng.randrange(mini,maxi)
        if (r > 99):
            l = self.touhousbystage[6]
        elif (r > 95):
            l = self.touhousbystage[5]
        elif (r > 90):
            l = self.touhousbystage[4]
        elif (r > 75):
            l = self.touhousbystage[3]
        elif (r > 55):
            l = self.touhousbystage[2]
        elif (r > 30):
            l = self.touhousbystage[1]
        else:
            l = self.touhousbystage[0]
        t = cop.copy(rng.choice(l)) # t = touhou object (cop.copy to ensure original values of touhu remain unchanged)
        t.setRarity(rarity) # set new Touhou's rarity
        t.setDifficulties() # set powerlevels of each of this Touhou's spellcards
        return t
    def catchTouhou(self,p):
        t = newhu() # set maxi by player level later

class DataHandler:
    def __init__(self):
        self.Data = Data() # To add: player shit, battle features, commands for bot
        self.status = {1:self.illuminate,2:self.blind,3:self.burn,4:self.poison,5:self.stun,6:self.concuss,7:self.bleed,8:self.heal,9:self.freeze,10:self.disease,11:self.charm,12:self.siren,100:self.extraturn}
        self.commands = {"help":self.help,"battle":self.singleplayer,"singlebattle":self.singleplayer,
                         "teambattle":self.multiplayer,"multibattle":self.multiplayer,"multiplayer":self.multiplayer,"multiteam":self.multiteam,
                         "stages":self.stages,"balance":self.balanceCheck,"":self.z,
                         "*Personal:*":self.z,"backpack":self.backpack,"viewbackpack":self.viewbackpack," ":self.z,
                         "secretary":self.secretary,"setsecretary":self.setSecretary,"  ":self.z,
                         "touhou":self.touhou,"setteam":self.setTeam,"clearteam":self.clearTeam,"   ":self.z,
                         "duel":self.duel,"teamduel":self.teamduel,"catch":self.catch,"adventure":self.adventure} # " " gaps used for more efficient displaying on Discord
    def grabName(self): # Output random touhou name to bot
        return rng.choice(self.Data.touhous).name
    def z(self):pass # for easier command listing # debug?

    # Parts of a single attack from one Touhou to another:
    def extraturn(self,s,attacker,i,remove=False): # Almighty timestop
        if remove:attacker.turns=1
        else:
            attacker.turns=2
            s+=":alarm_clock: "+attacker.name+" poses and exclaims: ***ZA WARUDO!*** :alarm_clock:||"
        return s
    def charm(self,s,attacker,i,remove=False): # Rude
        if remove:attacker.turns=1
        else:
            attacker.turns=0
            s+=":heart: "+attacker.name+" was Charmed and is too enthralled to attack! :heart:||"
        return s
    def illuminate(self,s,attacker,i,remove=False): # Light
        if remove:attacker.dodge = int(round(attacker.dodge*2))
        else:attacker.dodge = int(round(attacker.dodge/2))
        return s
    def blind(self,s,a,i,remove=False): # Dark
        if remove:a.accuracy = int(round(a.accuracy*2))
        else:a.accuracy = int(round(a.accuracy/2))
        return s
    def burn(self,s,attacker,i,remove=False): # Fire
        if not remove:
            x = rng.randrange(0,(attacker.PHATK*i.turns)) # damages increase as it proceeds
            attacker.HP = attacker.HP-x
            s+=":fire: "+attacker.name+" took "+str(x)+" damage from Burning! :fire:||"
        return s
    def poison(self,s,attacker,i,remove=False): # Water
        if not remove:
            x = rng.randrange(0,(attacker.MPATK*i.turns)) # damages increase as it proceeds
            attacker.HP = attacker.HP-x
            s+=":biohazard: "+attacker.name+" took "+str(x)+" damage from Poison! :biohazard:||"
        return s
    def stun(self,s,a,i,remove=False): # Wind
        if remove:
            a.dodge = int(round(a.dodge*2))
            a.accuracy = int(round(a.accuracy*2))
        else:
            a.dodge = int(round(a.dodge/2))
            a.accuracy = int(round(a.accuracy/2))
        return s
    def concuss(self,s,attacker,i,remove=False): # Earth
        if remove:attacker.turns=1
        else:
            s+=":warning: "+attacker.name+" cannot attack because of their concussion! :warning:||"
            attacker.turns=0
        return s
    def bleed(self,s,attacker,i,remove=False): # Synth
        if not remove:
            x = rng.randrange(0,(50*i.turns)) # damages increase as it proceeds
            attacker.HP = attacker.HP-x
            s+=":knife: "+attacker.name+" took "+str(x)+" damage from Bleeding! :knife:||"
        return s
    def heal(self,s,attacker,i,remove=False): # Almighty
        if not remove:
            x = rng.randrange(50,100)
            attacker.HP = attacker.HP+x
            s+=":hearts: "+attacker.name+" restored "+str(x)+" HP from Healing! :hearts:||"
        return s
    def freeze(self,s,attacker,i,remove=False): # Water
        if remove:attacker.turns=1
        else:
            s+=":icecream: "+attacker.name+" is Frozen solid and cannot attack! :icecream:||"
            attacker.turns=0
        return s
    def siren(self,s,attacker,i,remove=False): # Spirit (musical)
        if not remove:
            x = rng.randrange(0,(attacker.PHATK*i.turns)) # damages increase as it proceeds
            attacker.HP = attacker.HP-x
            s+=":loudspeaker: "+attacker.name+" took "+str(x)+" damage from the blaring Siren! :loudspeaker:||"
        return s
    def disease(self,s,attacker,i,remove=False): # Water
        if not remove:
            x = rng.randrange(0,(attacker.MPATK*i.turns)) # damages increase as it proceeds
            attacker.HP = attacker.HP-x
            s+=":biohazard: "+attacker.name+" took "+str(x)+" damage from the Plague! :biohazard:||"
        return s
    # To implement: radicalize system with array more status effects, range notification, edit critical hits?, elements dps buff, rarity dps buff (1.0,1.1,1.2,1.3), more end statistics and team notifications
    def turn(self,s,attacker,defender,r,a): #attacker=touhou using a spellcard against a target defender, r=range, a=attack
        dmg=0
        for g in range(attacker.turns): # usually just 1 attack, but possibly 2 or 0 for timestop or stun respectively
            # Calculation of Damage:
            if(a.magic):mod=attacker.MPATK # mod = magical/physical attack addition depending on respective nature of spellcard
            else:
                mod=attacker.PHATK
            ele = 1 # Elemental modifier
            for i in a.elements:
                ele*=(self.Data.elements[int(i)].list[defender.major])/2
                ele*=(self.Data.elements[int(i)].list[defender.minor])/4
            rmg = rng.randrange(0,10)
            dmg = int(round((a.DMG[r]+mod+rmg)*ele,0)) # (Spellcard damage + physical/magic attack value + 0-9) * elemental product
            #dmg = int(str((a.DMG[r]+mod+rmg)*ele).split(".")[0])
            # Hitting, Grazing or Missing and effect of each:
            h = rng.randrange(1,a.accuracy+attacker.accuracy) # int to avoid float failures
            if (dmg<=0):s+=defender.name+" says:\n'BAKA BAKA, BAKA BAKA, BAKA BAKA!'||" # no damage lmao
            elif (h>defender.dodge): # Hit
                if rng.randrange(0,100) > 94: # Tiny random chance of a CRITICAL HIT
                    dmg = dmg*5
                    defender.HP=defender.HP-dmg
                    s+=self.image(attacker.name,"Evil")
                    s+=":punch: **"+attacker.name+"["+str(attacker.HP)+"]** used *"+a.name+"!*\nCRITICAL HIT! :punch:|It does "+str(dmg)+" damage to "+defender.name+", reducing their health to "+str(defender.HP)+"!|"
                else:
                    defender.HP=defender.HP-dmg
                    s+="**"+attacker.name+"["+str(attacker.HP)+"]** used *"+a.name+"!*|It does "+str(dmg)+" damage to "+defender.name+", reducing their health to "+str(defender.HP)+".|"
                # Potentially Give Status Effects (only on direct hit):
                for i in a.effects: # for every possible effect it might instill on the target
                    if(rng.randrange(0,4)==0): # maybe change from 1/3 chance for each everytime later
                        for j in defender.immunities: # if status would go off, but defender is immune, notify the audience of this:
                            if i==j:s+=":stop: *"+defender.name+" was almost "+i.lingerhit+", but they are immune!* :stop:||"
                        if s[-7:]=="stop:||":pass # don't activate proc if immune (without having to declare variables and shit)
                        found = False
                        for j in defender.effects: # make sure not to stack effects
                            if j.id==i.id:found=True # could reset turn timer here
                        if found==False:
                            if i.target: # If inflicting on the defender:
                                defender.effects.append(cop.copy(i)) # N.B. need to copy it so as not to alter the actual effect
                                s+=":thumbsdown: *"+defender.name+" "+i.hit+"!* :thumbsdown:||"
                            else: # If inflicting it on themselves:
                                attacker.effects.append(cop.copy(i))
                                s+=":thumbsup: *"+attacker.name+" "+i.hit+"!* :thumbsup:||"
            elif (h>defender.dodge-10): # Graze
                dmg = int(round(dmg / 10))
                defender.HP -= dmg
                s+=":smirk: **"+attacker.name+"["+str(attacker.HP)+"]** used *"+a.name+"!*\nBut "+defender.name+" grazes it! :smirk:|It merely does "+str(dmg)+" damage to them and reduces their health to "+str(defender.HP)+".|"
            else: # Miss
                dmg = 0
                s+=":sweat: **"+attacker.name+"["+str(attacker.HP)+"]** used *"+a.name+",*\nbut it completely missed "+defender.name+"! :sweat:||"
        # rarity buff:
        rs = ["N","SR","SSR","USSR"]
        for r in enumerate(rs):
            if attacker.rarity==r[1]: dmg*= (r[0]*0.1)+1 # 1.0x to 1.3x boost
            if defender.rarity==r[1]: dmg*= 1-(r[0]*0.1) # 1.0x to 0.7x boost
        return s,dmg
    # Parts from a battle between at least 2 opposing Touhous, consisting of a series of 'turns' above:
    def rps(self,who,d): # Choose attack. d = difficulty (4 = any)
        if(d==4):return who.getAnyAttack()
        else:return who.getAttack(d)
    def frontline(self,s,attackers,defenders,row,diff,maxdmg): #misleading title, can be backline too
        maxi = 2
        for i in attackers[row]:
            if not defenders[1]:maxi=1 # limit to short/medium range if no opposing backline
            r = rng.randrange(0,maxi) # choose range
            atk = self.rps(i,diff) # choose their attack
            # Impact of Status Effects:
            x,dmg = 0,0
            for j in i.effects:
                if j.turns<1: # if this is the last turn if affects the touhou on (delete Status from Touhou and possibly revert effects):
                    if j.team:
                        for k in attackers[row]:
                            s = self.status[j.id](s,k,j,True) # remove the effect to stats if required (only works for one shots)
                    else:s = self.status[j.id](s,i,j,True) # remove the effect to stats if required (only works for one shots)
                    del i.effects[x]
                    if j.lingerhit!=" ":s+=":thumbsup: *"+i.name+" is no longer "+j.lingerhit+"!* :thumbsup:||" # move to remove
                else:
                    if j.constant>0:
                        if j.team:
                            for k in attackers[row]:
                                s = self.status[j.id](s,i,j) # run effects (see above procs)
                        else:s = self.status[j.id](s,i,j)
                        if j.constant==1:j.constant = 0 # if one-shot, prevent it from running next turn
                    j.turns-=1
                x+=1
            # Target an opposing Touhou and attack them:
            t = rng.randrange(0,len(defenders[r])) # choose target index
            tar = defenders[r][t] # get target
            s,dmg = self.turn(s,i,tar,r+row,atk) # attack them
            if(dmg>maxdmg.value):maxdmg=Stat(dmg,i.name,atk.name) # record stats if needed
            if (tar.HP < 0.1): # touhous die when they are killed (uh oh)
                s+=self.image(defenders[r][t].name,"Sad")
                s+=":skull_crossbones: "+tar.name+" fell unconscious. :skull_crossbones:||"
                del defenders[r][t]
                if not defenders[0]:
                    defenders[0]=defenders[1] # move backline into frontline if frontline are all dead
                    defenders[1]=[]
                    if not defenders[0]:
                        #s+=":The opposing team were all defeated!:\n" #blocked for now for singlebattle accomodation using this proc
                        return s,maxdmg # GG
                    s+=":arrow_forward: The opposing backline moves forward! :arrow_forward:||"
        return s,maxdmg
    def restoreimage(self,n): # removes white bg from pngs, temporary
        rgba = np.array(Image.open("chars/"+n+"/Smug.png"))
        rgba[rgba[...,-1]==0] = [0,0,0,0]
        Image.fromarray(rgba).save("chars/"+n+"/Smug.png")
    def teamimage(self,n,na,nb,nc): # create/overwrite horizontal 'team' image n with character portraits na, nb and nc
        # stolen from StackOverflow tbh
        # ongoing fix for white png background removal, remove eventually
        self.restoreimage(na)
        self.restoreimage(nb)
        self.restoreimage(nc)
        images = map(Image.open, ["chars/"+na+"/Smug.png", "chars/"+nb+"/Smug.png", "chars/"+nc+"/Smug.png"])
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)
        new_im = Image.new('RGB', (total_width, max_height))
        x_offset = 0
        images = map(Image.open, ["chars/"+na+"/Smug.png", "chars/"+nb+"/Smug.png", "chars/"+nc+"/Smug.png"])
        for im in images:
            new_im.paste(im, (x_offset,max_height-im.height))
            x_offset += im.size[0]
        new_im.save("chars/Main/"+n+".png")
    def multibattle(self,s,ateam,bteam,d=4):
        turns = 0
        amaxdmg,bmaxdmg=Stat(0,"",""),Stat(0,"","")
        s+=":arrow_double_down: "+ateam[1][0].name+" "+ateam[1][1].name+" "+ateam[1][2].name+" :arrow_double_down:||"
        self.teamimage("Team1b",ateam[1][0].name,ateam[1][1].name,ateam[1][2].name)
        s+=self.image("Main","Team1b")
        #s+=self.image(ateam[1][rng.randrange(0,3)].name,"Default")
        s+=":arrow_double_down:  "+ateam[0][0].name+" "+ateam[0][1].name+" "+ateam[0][2].name+" :arrow_double_down:||"
        self.teamimage("Team1f",ateam[0][0].name,ateam[0][1].name,ateam[0][2].name)
        s+=self.image("Main","Team1f")
        #s+=self.image(ateam[0][rng.randrange(0,3)].name,"Default")
        s+="VS||"
        self.teamimage("Team2f",bteam[0][0].name,bteam[0][1].name,bteam[0][2].name)
        s+=self.image("Main","Team2f")
        #s+=self.image(bteam[0][rng.randrange(0,3)].name,"Default")
        s+=":arrow_double_up: "+bteam[0][0].name+" "+bteam[0][1].name+" "+bteam[0][2].name+" :arrow_double_up:||"
        self.teamimage("Team2b",bteam[1][0].name,bteam[1][1].name,bteam[1][2].name)
        s+=self.image("Main","Team2b")
        #s+=self.image(bteam[1][rng.randrange(0,3)].name,"Default")
        s+=":arrow_double_up: "+bteam[1][0].name+" "+bteam[1][1].name+" "+bteam[1][2].name+" :arrow_double_up:||"
        s+=":bell: Fight! :bell:||" # touhou flavortext here!
        while (ateam and bteam):
            #s+="***" # separator line for different messages on discord
            # One turn of combat:
            turns+=1
            s+="***Team 1's frontline attacks!|------------------------------|"
            s,amaxdmg=self.frontline(s,ateam,bteam,0,d,amaxdmg) # 0 = Short to Medium range
            if not ateam[0] or not bteam[0]:break
            s+="***Team 2's frontline attacks!|------------------------------|"
            s,bmaxdmg=self.frontline(s,bteam,ateam,0,d,bmaxdmg)
            if not ateam[0] or not bteam[0]:break
            if ateam[1]: # doesn't continue if it's a touhou in a 1D list (one of the lines is RIP)
                s+="***Team 1's backline attacks!|------------------------------|"
                s,amaxdmg=self.frontline(s,ateam,bteam,1,d,amaxdmg) # 1 = Medium to Far range
                if not ateam[0] or not bteam[0]:break
            if bteam[1]:
                s+="***Team 2's backline attacks!|------------------------------|"
                s,bmaxdmg=self.frontline(s,bteam,ateam,1,d,bmaxdmg)
        return self.showStats(s,ateam,bteam,amaxdmg,bmaxdmg,turns)
    def singlebattle(self,s,ateam,bteam,d=4): #d=difficulty
        turns = 0
        amaxdmg,bmaxdmg=Stat(0,"",""),Stat(0,"","")
        s+=":arrow_double_down: "+ateam[0][0].name+" :arrow_double_down:||"
        s+=self.image(ateam[0][0].name,"Default")
        s+="VS||"
        s+=self.image(bteam[0][0].name,"Default")
        s+=":arrow_double_up: "+bteam[0][0].name+" :arrow_double_up:||"
        s+=":bell: Fight! :bell:||" # touhou flavortext here!
        while (ateam and bteam):
            # One turn of combat:
            turns+=1
            s,amaxdmg=self.frontline(s,ateam,bteam,0,d,amaxdmg) # 0 = Short to Medium range
            if not ateam[0] or not bteam[0]:break
            s,bmaxdmg=self.frontline(s,bteam,ateam,0,d,bmaxdmg)
            #if turns%5==0:s+="***" #might need to add ***s here
        return self.showStats(s,ateam,bteam,amaxdmg,bmaxdmg,turns)
    def showStats(self,s,ateam,bteam,amaxdmg,bmaxdmg,turns):
        s+="***"
        #s+="***xxxxxxxxxxxxxxxxxxxxxx\n***"
        if ateam[0]:
            s+=self.image(ateam[0][0].name,"Happy")
            s+="You won!|\n" #assign to players
        else:
            s+=self.image(bteam[0][0].name,"Happy")
            s+="You lost!|\n"
        s+="Turns taken: "+str(turns)+"|\n"
        s+="Stats for Team 1:|\n" #debug (team 1 will equal discord username
        s+="Highest Damage: "+str(amaxdmg.value)+" by **"+amaxdmg.title+"** with *"+amaxdmg.name+"*|"
        s+="Stats for Team 2:|\n" #debug
        s+="Highest Damage: "+str(bmaxdmg.value)+" by **"+bmaxdmg.title+"** with *"+bmaxdmg.name+"* |***"
        return s
    def multiteam(self,player1,player2):
        # get player details by comparing discord username here:
        p1 = self.getPlayerByUsername(player1)
        p2 = self.getPlayerByUsername(player2)
        # make a copy of their teams for this battle:
        ateam = cop.copy(p1.team)
        bteam = cop.copy(p2.team)
        """s = ""
        ateam,bteam = [[],[]],[[],[]]
        for i in range(3):
            ateam[0].append(self.dupe(xteam[0][i])) # debug only
            ateam[1].append(self.dupe(yteam[1][i])) # debug only
            bteam[0].append(self.dupe(xteam[0][i])) # debug only
            bteam[1].append(self.dupe(yteam[1][i])) # debug only"""
        return self.multibattle(s,ateam,bteam) # all diffuclties
    def multiplayer(self, a,b,c,d,e,f, u,v,w,x,y,z):
        s = ""
        # cancer:
        a,ss = self.dupe(a)
        s+=ss
        b,ss = self.dupe(b)
        s+=ss
        c,ss = self.dupe(c)
        s+=ss
        d,ss = self.dupe(d)
        s+=ss
        e,ss = self.dupe(e)
        s+=ss
        f,ss = self.dupe(f)
        s+=ss
        u,ss = self.dupe(u)
        s+=ss
        v,ss = self.dupe(v)
        s+=ss
        w,ss = self.dupe(w)
        s+=ss
        x,ss = self.dupe(x)
        s+=ss
        y,ss = self.dupe(y)
        s+=ss
        z,ss = self.dupe(z)
        s+=ss
        
        ateam,bteam = [[a,b,c],[d,e,f]],[[u,v,w],[x,y,z]]
        return self.multibattle(s,ateam,bteam) # all diffuclties
    def singleplayer(self,x,y):
        s = ""
        a,ss = self.dupe(x)
        s+=ss
        b,ss = self.dupe(y)
        s+=ss
        #a = cop.copy(self.Data.getTouhouByName(x))
        #b = cop.copy(self.Data.getTouhouByName(y))
        ateam,bteam=[[a],[]],[[b],[]]
        return self.singlebattle(s,ateam,bteam)
    # Non Standard Game Modes:
    def stages(self,x=""):
        stage = 1
        mini = {1:0,2:31,3:56,4:76,5:91,6:96,7:100,8:100} # Used for specifying touhous by stage
        maxi = {1:30,2:55,3:75,4:90,5:95,6:99,7:101,8:101} # Used for specifying touhous by stage
        emo = ["broken_heart","crescent_moon","fire","fireworks","first_place","hammer","heart","moneybag","pray","telescope","milk"]
        e = rng.choice(emo)
        adj = ["Highly Responsive to","The Story of","Phantasmagoria of","Lotus","Mystic","Embodiment of","Perfect","Immaterial and Missing","Imperishable","Shoot the","Mountain of","Scarlet Weather","Subterranean","Unidentified","Touhou","Double","Fairy","Ten","Hopeless","Double Dealing","Impossible","Urban Legend in","Legend of","Antimony of","Hidden Star in","Violet","Wily Beast and"]
        nou = ["Prayers","Eastern Wonderland","Dim.Dream","Land Story","Square","Scarlet Devil","Cherry Blossom","Power","Night","Flower View","Bullet","Faith","Rhapsody","Animism","Fantastic Object","Hisoutensoku","Spoiler","Wars","Desires","Masquerade","Character","Spell Card","Limbo","Lunatic Kingdom","Common Flowers","Four Seasons","Detector","Weakest Creature"]
        s = ":"+e+": Touhou "+str(rng.randrange(1,101))+": "+adj[rng.randrange(0,len(adj))]+" "+nou[rng.randrange(0,len(nou))]+"! :"+e+":|"
        dif = {0:"Playing on **Easy** difficulty.",1:"Playing on **Normal** difficulty.",2:"Playing on **Hard** difficulty.",3:"Playing on **Lunatic** difficulty!"} #
        d = rng.randrange(0,4) # difficulty
        s += dif[d]+"|"
        #a = cop.copy(self.Data.getTouhouByName(x))
        a,ss = self.dupe(x)
        s+=ss # reduced to one line maybe?
        s+=self.image(a.name,"Happy")
        s+="**"+a.name+"** can use the following spellcards:|" #
        for i in a.getSpellcardsbydifficulty(d): # debug only! #
            s+=i.name+"\n" #
        s+="|***" #***
        b = cop.copy(a)
        totalstages = rng.randrange(1,9)#phantasm roll
        if totalstages<8:totalstages=7 # either 7 or rarely 8 stages
        while (b.HP>0 and stage < totalstages):
            if stage<7:s+="STAGE "+str(stage)+":||" # declare whether stage or special stage
            elif stage < 8:s+="EX STAGE:||"
            else:s+="PHANTASM STAGE:||"
            """if round(stage)>stage: # if midboss, fight them first:
                s+="MIDBOSS:||"
                b = cop.copy(a)
                ateam = [[b],[]]
                bteam = [[cop.copy(self.Data.newhu(mini[stage],maxi[stage]))],[]]
                s += self.singlebattle(s,ateam,bteam,d)
            s+="BOSS:||"""
            b = cop.copy(a) # reset variables to battle starting values
            ateam = [[b],[]] #reset stats
            bteam = [[cop.copy(self.Data.newhu(mini[stage],maxi[stage]))],[]] #get random opposing touhou based on stage
            s = self.singlebattle(s,ateam,bteam,d)
            stage+=1
        if ateam[0]:
            s+=":thumbsup::thumbsup::thumbsup: Congrats, you resolved the Incident! :thumbsup::thumbsup::thumbsup:||"
        else:
            s+=":frowning: Better luck next time, kid. :frowning:||"
        return s
    def balanceCheck(self,x,y): #a and b are Touhou names
        aHPa,dHPa = [],[]
        s = ""
        attacker,ss = self.dupe(x)
        s+=ss
        defender,ss = self.dupe(y)
        s+=ss
        diffs=["Easy|","Normal|","Hard|","Lunatic|","Any|"]
        for j in range(5):
            aHPm,dHPm=0,0
            wins,losses = 0,0
            for i in range(10):
                a = cop.copy(attacker)
                d = cop.copy(defender)
                ss = self.singlebattle(s,[[a],[]],[[d],[]],j)
                aHPm+=a.HP
                dHPm+=d.HP
                if (a.HP > 0):
                    wins+=1
                else:
                    losses+=1
            if aHPm<0:aHPm=0
            if dHPm<0:dHPm=0
            aHPa.append(aHPm)
            dHPa.append(dHPm)
            s+=diffs[j]
            s+="*Victories out of 10 matches:*\n"
            s+="**"+a.name+"**: "+str(wins)+"\n"
            s+="**"+d.name+"**: "+str(losses)+"***"#\n
        plt.plot(aHPa,'-b',label=a.name)
        plt.plot(dHPa,'-r',label=d.name)
        plt.legend(loc='upper left')
        maxa = []
        maxa.append(max(aHPa))
        maxa.append(max(dHPa))
        plt.axis([0, 4, 0, max(maxa)])
        plt.xticks([0,1,2,3,4],["Easy","Normal","Hard","Lunatic","Any"])
        plt.ylabel('Mean HP (10 rounds)')
        #plt.yaxis(0, 1200)
        #plt.axis(option='tight')
        plt.savefig('chars/Main/graph.png')
        plt.close()
        s+=self.image("Main","graph")
        s+="Perfectly balanced... as all things should be(?)||"
        return s
    # Player shit:
    def pointCheck(self,p,required):
        points = p.points
        if points >= required:return p.losePoints(required),False
        else:return "Hey!|You don't have enough points to do that!\nCommand Cost: "+str(c)+"\nYou have: "+str(p.points)+"\nYou need: "+str(c-p.points)+" more!",True
    def catch(self,playerdetails): # Add level shit
        p = self.Data.getPlayerByUsername(playerdetails) # also creates new player and adds them if not found
        s,b = self.pointCheck(p,10)
        if b:return s
        # Catch a random Touhou of random rarity and add it to the post author's inventory (tl;dr gacha)
        catch = cop.copy(self.Data.newhu())
        if (catch.rarity[0]=="U"):s += "THE WHEEL OF FATE IS TURNING...|You caught an **["+catch.rarity+" "+catch.name+"]**!|"
        else:s += "THE WHEEL OF FATE IS TURNING...|You caught a **["+catch.rarity+" "+catch.name+"]**!|"
        s+=self.image(catch.name,"Happy")
        # add to player collection and post message to discord
        s+=p.appendBackpack(catch) #.name+"|"+catch.rarity
        lucky = 5
        while lucky>3: # 1 in 4 chance to gain an extra Catch, which can stack.
            lucky = rng.randrange(1,5)
            if lucky>3:
                catch = cop.copy(self.Data.newhu())
                if (catch.rarity[0]=="U"):s += "LUCKY!|You also caught an **["+catch.rarity+" "+catch.name+"]**!|"
                else:s += "LUCKY!|You also caught a **["+catch.rarity+" "+catch.name+"]**!|"
                s+=self.image(catch.name,"Happy")
                s+=p.appendBackpack(catch)
        return s
    
    def secretary(self,playerdetails): # equvilant to viewSecretary + helpSecretary
        p = self.Data.getPlayerByUsername(playerdetails)
        try:
            #s = self.Data.getTouhouByName(p.secretary).toString() # prints Secretary details and image before continuing
            s = p.secretary.toString()
        except:
            s = "You currently have no Secretary!|To set a secretary from a Touhou in your Backpack, type:\n'!war setsecretary [Touhou Name]'|"
        c = ["setSecretary"] # add commands here!
        s+="Secretary Commands:|"
        for i in c:s+=i+"\n"
        return s+"|"
    def setSecretary(self,playerdetails,newsec):
        p = self.Data.getPlayerByUsername(playerdetails)
        return p.setSecretary(newsec) # string
    
    def setTeam(self,playerdetails,a,b,c,d,e,f):
        try:
            a = self.definedDupe(a)
            b = self.definedDupe(b)
            c = self.definedDupe(c)
            d = self.definedDupe(d)
            e = self.definedDupe(e)
            f = self.definedDupe(f)
        except:
            return "INPUT ERROR:|Please enter 6 valid Touhou names!|"
        p = self.Data.getPlayerByUsername(playerdetails)
        s = p.setTeam([a,b,c],[d,e,f]) # string or None
        if s == None:
            s = "Your Backline:|"
            s+=d.name+" "+e.name+" "+f.name+"|"
            self.teamimage("Team1b",d.name,e.name,f.name)
            s+=self.image("Main","Team1b")
            s+= "Your Frontline:|"
            s+=a.name+" "+b.name+" "+c.name+"|"
            self.teamimage("Team1f",a.name,b.name,c.name)
            s+=self.image("Main","Team1f")
        return s
    def clearTeam(self,playerdetails):
        self.Data.getPlayerByUsername(playerdetails).clearTeam()
        return "Your Team has been shuffled into your Backpack.||"
    def backpack(self,playerdetails): # equvilant to viewSecretary + helpSecretary
        p = self.Data.getPlayerByUsername(playerdetails)
        s = self.viewbackpack(playerdetails) # prints Secretary details and image before continuing
        c = ["viewbackpack"] # add commands here!
        s+="Backpack Commands:|"
        for i in c:s+=i+"\n"
        return s+"|"
    def viewbackpack(self,playerdetails):
        bp = self.Data.getPlayerByUsername(playerdetails).getBackpack()
        s = "Your Backpack:|"
        for i in bp:s+=i.rarity+" "+i.name+"\n"
        return s+"|"
    def touhou(self,t):
        try:
            return self.Data.getTouhouByName(t).toString()
        except:
            return "INPUT ERROR:|'"+t+"' is not a valid Touhou name!|"
    def duel(self,authordetails,playerdetails): # message author's Secretary vs player's Secretary they call out, if possible
        a = self.Data.getPlayerByUsername(authordetails)
        p = self.Data.getPlayerByUsername(playerdetails)
        try:
            a.secretary.toString()
        except:
            return "You currently have no Secretary!|To set a secretary from a Touhou in your Backpack, type:\n'!war setsecretary [Touhou Name]'|"
        try:
            p.secretary.toString()
        except:
            return "Opponent currently has no Secretary!|To set a secretary from a Touhou in your Backpack, type:\n'!war setsecretary [Touhou Name]'|"
        return self.singleplayer(a.secretary.name,p.secretary.name) # run fight if both players have Secretaries
    def teamduel(self,authordetails,playerdetails): # message author's Secretary vs player's Secretary they call out, if possible
        a = self.Data.getPlayerByUsername(authordetails)
        p = self.Data.getPlayerByUsername(playerdetails)
        try:
            a.team[0][0].toString() # doesn't add to s so doesn't print on Discord, 
            a.team[0][1].toString() # but is used as a test to ensure it's a Touhou
            a.team[0][2].toString() # and not something dumb like a string
            a.team[1][0].toString()
            a.team[1][1].toString()
            a.team[1][2].toString()
        except:
            return "You currently don't have a full Team!|To set a secretary from a Touhou in your Backpack, type:\n'!war setsecretary [Touhou Name]'|"
        try:
            p.team[0][0].toString()
            p.team[0][1].toString()
            p.team[0][2].toString()
            p.team[1][0].toString()
            p.team[1][1].toString()
            p.team[1][2].toString()
        except:
            return "Opponent currently doesn't have a full Team!|To set a secretary from a Touhou in your Backpack, type:\n'!war setsecretary [Touhou Name]'|"
        return self.multiplayer(a.team[0][0].name,a.team[0][1].name,a.team[0][2].name,a.team[1][0].name,a.team[1][1].name,a.team[1][2].name,p.team[0][0].name,p.team[0][1].name,p.team[0][2].name,p.team[1][0].name,p.team[1][1].name,p.team[1][2].name) # run fight if both players have full Teams
    def adventure(self,authordetails,x=""): #stages
        stage = 1
        mini = {1:0,2:31,3:56,4:76,5:91,6:96,7:100,8:100} # Used for specifying touhous by stage
        maxi = {1:30,2:55,3:75,4:90,5:95,6:99,7:101,8:101} # Used for specifying touhous by stage
        emo = ["broken_heart","crescent_moon","fire","fireworks","first_place","hammer","heart","moneybag","pray","telescope","milk"]
        e = rng.choice(emo)
        adj = ["Highly Responsive to","The Story of","Phantasmagoria of","Lotus","Mystic","Embodiment of","Perfect","Immaterial and Missing","Imperishable","Shoot the","Mountain of","Scarlet Weather","Subterranean","Unidentified","Touhou","Double","Fairy","Ten","Hopeless","Double Dealing","Impossible","Urban Legend in","Legend of","Antimony of","Hidden Star in","Violet","Wily Beast and"]
        nou = ["Prayers","Eastern Wonderland","Dim.Dream","Land Story","Square","Scarlet Devil","Cherry Blossom","Power","Night","Flower View","Bullet","Faith","Rhapsody","Animism","Fantastic Object","Hisoutensoku","Spoiler","Wars","Desires","Masquerade","Character","Spell Card","Limbo","Lunatic Kingdom","Common Flowers","Four Seasons","Detector","Weakest Creature"]
        s = ":"+e+": Touhou "+str(rng.randrange(1,101))+": "+adj[rng.randrange(0,len(adj))]+" "+nou[rng.randrange(0,len(nou))]+"! :"+e+":|"
        dif = {0:"Playing on **Easy** difficulty.",1:"Playing on **Normal** difficulty.",2:"Playing on **Hard** difficulty.",3:"Playing on **Lunatic** difficulty!"} #
        d = rng.randrange(0,4) # difficulty
        s += dif[d]+"|"
        au = self.Data.getPlayerByUsername(authordetails)
        # find Touhou in player's inventory:
        #for 
        #for i in au.backpack:
        #x=
        a,ss = self.dupe(au.secretary.name) #(x)
        s+=ss # reduced to one line maybe?
        s+=self.image(a.name,"Happy")
        s+="**"+a.name+"** can use the following spellcards:|" #
        for i in a.getSpellcardsbydifficulty(d): # debug only! #
            s+=i.name+"\n" #
        s+="|***" #***
        b = cop.copy(a)
        totalstages = rng.randrange(1,9)#phantasm roll
        if totalstages<8:totalstages=7 # either 7 or rarely 8 stages
        while (b.HP>0 and stage < totalstages):
            if stage<7:s+="STAGE "+str(stage)+":||" # declare whether stage or special stage
            elif stage < 8:s+="EX STAGE:||"
            else:s+="PHANTASM STAGE:||"
            """if round(stage)>stage: # if midboss, fight them first:
                s+="MIDBOSS:||"
                b = cop.copy(a)
                ateam = [[b],[]]
                bteam = [[cop.copy(self.Data.newhu(mini[stage],maxi[stage]))],[]]
                s = self.singlebattle(s,ateam,bteam,d)
            s+="BOSS:||"""
            b = cop.copy(a) # reset variables to battle starting values
            ateam = [[b],[]] #reset stats
            bteam = [[cop.copy(self.Data.newhu(mini[stage],maxi[stage]))],[]] #get random opposing touhou based on stage
            s = self.singlebattle(s,ateam,bteam,d)
            #s+="***"
            stage+=1
            if b.HP>0:s+=au.gainPoints(10*stage) # Player gains Points every time they Win a Stage.
        if ateam[0]:
            s+=":thumbsup::thumbsup::thumbsup: Congrats, you resolved the Incident! :thumbsup::thumbsup::thumbsup:||"
        else:
            s+=":frowning: Better luck next time, kid. :frowning:||"
        return s
    # Other
    def image(self,c,e): # form a string that will make the bot post an image when it's fed into it during the output process
        return "***>"+c+">"+e+"***"
    def help(self):
        s = "List of !war commands:|"
        for i in self.commands:
            s+=i+"\n"
        return s
    def definedDupe(self,x): # throw error if incorrect 2hu
        y = cop.copy(self.Data.getTouhouByName(x))
        y.toString()
        return y
    def dupe(self,x): # attempt to grab a touhou by name. If it fails (user typo most likely) then grab a random touhou and inform the user
        s = ""
        y = cop.copy(self.Data.getTouhouByName(x)) #touhou exists
        if y is None:
            y = cop.copy(self.Data.newhu())
            s+="INPUT ERROR:|'"+x+"' is not a valid Touhou name! They have been replaced by **"+y.name+".**|"
        return y,s
    # random encounter one team of touhou
# Currently: Redoing battle system in multiplayer format only to accomodate abilities like Alice creating dolls and group-affecting status effects
# Battle Phases: Selection of Touhou -> Battle loop -> Stats
# Resistances and Immunities
# print damage calculation
# Empty 2hu
# Replace catch with better rarity unless LEGENDARY
