import os
import sys
import clr
import time
import random
import datetime
import shutil

clr.AddReference('IronPython.SQLite.dll')
clr.AddReference('IronPython.Modules.dll')

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = 'FNJ - Arena'
Website = 'https://www.StreamlabsChatbot.com'
Description = 'Friday Night Jams - Arena (!fnj & !profile)'
Creator = 'DrWhistler'
Version = '1.0.0.0'

#---------------------------------------
# Set Variables
#---------------------------------------
m_Response = 'This is a test message'
m_Command = '!fnj'
m_CooldownSeconds = 120
m_CommandPermission = 'Everyone'
m_CommandInfo = ''

userId=""

playerActiveList=[]
playerInactiveList=[]

def Init():
 global m_Response
 m_Response = '' 
 return

def Execute(data):

    global userId
    userId = data.User.lower()

    if data.IsChatMessage():

        if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
            
            userId = data.User.lower()
            
            ### join  ##################################
            if data.GetParam(1).lower() == 'enter':
                enterArena(userId,False)

            ### leave ##################################
            elif data.GetParam(1).lower() == 'exit':               
                exitArena(userId)

            ### who   ##################################
            elif data.GetParam(1).lower() == 'who':   
                who()

        if data.GetParam(0).lower() == m_Command and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,'Moderator',m_CommandInfo):
            
            ### reset  ##################################
            if data.GetParam(1).lower() == 'clear':

                ClearArena()
 
             ### add  ##################################
            if data.GetParam(1).lower() == 'add':

                if (data.GetParam(2).lower() == 'ch'):
                    challenge(data.GetParam(3).lower())
                else:
                    if (data.GetParam(2).lower()):
                        AddPlayer(data.GetParam(2).lower())
                    else:
                        Parent.SendTwitchMessage('/w drwhistler No user specifieid to be entered. Type !fnj add <player>')
 
            ### remove  ##################################
            if data.GetParam(1).lower() == 'remove':

                if (data.GetParam(2).lower()):
                    RemovePlayer(data.GetParam(2).lower())
                else:
                    Parent.SendTwitchMessage('/w drwhistler No user specifieid to be removed. Type !fnj remove <player>')

            ### Return list of active participants sorted by SR  ##################################
            if data.GetParam(1).lower() == 'list':   

                ReturnSortedParticipants()

        if data.GetParam(0).lower() == '!profile' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
                        
            if (data.GetParam(1)):

                if (data.GetParam(1).lower()=='region'):

                    if (data.GetParam(2).lower()=='e' or data.GetParam(2).lower()=='w' or data.GetParam(2).lower()=='eu' or data.GetParam(2).lower()=='s' or data.GetParam(2).lower()=='o' or data.GetParam(2).lower()=='a'):
                        setRegion(userId,data.GetParam(2).lower())
                    else:
                        Parent.SendTwitchMessage('/w ' + data.User + ' Type "!profile region <region>" to update your profile. Valid regions are: \'E\' US East , \'W\' US West , \'EU\' Europe , \'S\' South America , \'O\' Oceania , and \'A\' Southeast Asia ')

                elif (data.GetParam(1).lower()=='court'):
                
                    if (data.GetParam(2).lower()=='random' or data.GetParam(2).lower()=='stadium' or data.GetParam(2).lower()=='penthouse'):
                        setCourt(userId,data.GetParam(2).lower())
                    else:
                        Parent.SendTwitchMessage('/w ' + data.User + ' Type "!profile court <court>" to update your profile. Valid courts are: \'RANDOM\' , \'STATDIUM\' , and \'PENTHOUSE\' ')

                elif (data.GetParam(1).lower()=='main'):

                    if (data.GetParam(2).lower()=='gator' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='bluebolt' or data.GetParam(3).lower()=='bold' or data.GetParam(3).lower()=='mustard' or data.GetParam(3).lower()=='neongreeon' or data.GetParam(3).lower()=='plum' or data.GetParam(3).lower()=='purplerays' or data.GetParam(3).lower()=='salmon' or data.GetParam(3).lower()=='sweeli' or data.GetParam(3).lower()=='bone' or data.GetParam(3).lower()=='dinocamo' or data.GetParam(3).lower()=='flamingo' or data.GetParam(3).lower()=='lips' or data.GetParam(3).lower()=='rainbow' or data.GetParam(3).lower()=='galvanized' or data.GetParam(3).lower()=='junker' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'bluebolt\', \'bold\', \'mustard\', \'neongreeon\', \'plum\', \'purplerays\', \'salmon\', \'sweeli\', \'bone\', \'dinocamo\', \'flamingo\', \'lips\', \'rainbow\', \'galvanized\', and \'junker\'.')

                    elif (data.GetParam(2).lower()=='haruka' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='amethyst' or data.GetParam(3).lower()=='aquamarine' or data.GetParam(3).lower()=='ember' or data.GetParam(3).lower()=='grape' or data.GetParam(3).lower()=='grass' or data.GetParam(3).lower()=='greyhound' or data.GetParam(3).lower()=='griffin' or data.GetParam(3).lower()=='ocean' or data.GetParam(3).lower()=='slate' or data.GetParam(3).lower()=='tourmaline' or data.GetParam(3).lower()=='boombox' or data.GetParam(3).lower()=='butterflies' or data.GetParam(3).lower()=='cherryblossom' or data.GetParam(3).lower()=='skulls' or data.GetParam(3).lower()=='splatter' or data.GetParam(3).lower()=='thorns' or data.GetParam(3).lower()=='midnight' or data.GetParam(3).lower()=='ninjabot' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'amethyst\', \'aquamarine\', \'ember\', \'grape\', \'grass\', \'greyhound\', \'griffin\', \'ocean\', \'slate\', \'tourmaline\', \'boombox\', \'butterflies\', \'cherryblossom\', \'skulls\', \'splatter\', \'thorns\', \'midnight\', and \'ninjabot\'.')

                    elif (data.GetParam(2).lower()=='kahuna' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='aerobic' or data.GetParam(3).lower()=='garnet' or data.GetParam(3).lower()=='maroon' or data.GetParam(3).lower()=='tribal' or data.GetParam(3).lower()=='warrior' or data.GetParam(3).lower()=='yellowblue' or data.GetParam(3).lower()=='choco' or data.GetParam(3).lower()=='d-pad' or data.GetParam(3).lower()=='donuts' or data.GetParam(3).lower()=='folk' or data.GetParam(3).lower()=='native' or data.GetParam(3).lower()=='vanilla' or data.GetParam(3).lower()=='whales' or data.GetParam(3).lower()=='driftwood' or data.GetParam(3).lower()=='marble' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'aerobic\', \'garnet\', \'maroon\', \'tribal\', \'warrior\', \'yellowblue\', \'choco\', \'d-pad\', \'donuts\', \'folk\', \'native\', \'vanilla\', \'whales\', \'driftwood\', and \'marble\'.')

                    elif (data.GetParam(2).lower()=='lannie' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='brasilia' or data.GetParam(3).lower()=='creamsicle' or data.GetParam(3).lower()=='duck' or data.GetParam(3).lower()=='fury' or data.GetParam(3).lower()=='golden' or data.GetParam(3).lower()=='magenta' or data.GetParam(3).lower()=='pastel' or data.GetParam(3).lower()=='block' or data.GetParam(3).lower()=='graffiti' or data.GetParam(3).lower()=='owls' or data.GetParam(3).lower()=='pelican' or data.GetParam(3).lower()=='skulls' or data.GetParam(3).lower()=='wild' or data.GetParam(3).lower()=='lizard' or data.GetParam(3).lower()=='tank' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'brasilia\', \'creamsicle\', \'duck\', \'fury\', \'golden\', \'magenta\', \'pastel\', \'block\', \'graffiti\', \'owls\', \'pelican\', \'skulls\', \'wild\', \'lizard\', and \'tank\'.')

                    elif (data.GetParam(2).lower()=='makenna' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='burntsienna' or data.GetParam(3).lower()=='emeraldisle' or data.GetParam(3).lower()=='lemonlime' or data.GetParam(3).lower()=='mustard' or data.GetParam(3).lower()=='pier' or data.GetParam(3).lower()=='rose' or data.GetParam(3).lower()=='royalpurple' or data.GetParam(3).lower()=='skyblue' or data.GetParam(3).lower()=='clovers' or data.GetParam(3).lower()=='heartland' or data.GetParam(3).lower()=='intergalactic' or data.GetParam(3).lower()=='mak' or data.GetParam(3).lower()=='pajamaparty' or data.GetParam(3).lower()=='physics' or data.GetParam(3).lower()=='m-5000' or data.GetParam(3).lower()=='msmidas' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'burntsienna\', \'emeraldisle\', \'lemonlime\', \'mustard\', \'pier\', \'rose\', \'royalpurple\', \'skyblue\', \'clovers\', \'heartland\', \'intergalactic\', \'mak\', \'pajamaparty\', \'physics\', \'m-5000\', and \'msmidas\'.')

                    elif (data.GetParam(2).lower()=='stanton' ):
                        if (data.GetParam(3).lower()=='discjam' or data.GetParam(3).lower()=='aqua' or data.GetParam(3).lower()=='bumblebee' or data.GetParam(3).lower()=='forest' or data.GetParam(3).lower()=='peppermint' or data.GetParam(3).lower()=='picante' or data.GetParam(3).lower()=='seabird' or data.GetParam(3).lower()=='tangerine' or data.GetParam(3).lower()=='unconquered' or data.GetParam(3).lower()=='floral' or data.GetParam(3).lower()=='graffiti' or data.GetParam(3).lower()=='hautepink' or data.GetParam(3).lower()=='hautepink' or data.GetParam(3).lower()=='loverboy' or data.GetParam(3).lower()=='tealsforreals' or data.GetParam(3).lower()=='bronzepenny' or data.GetParam(3).lower()=='steelworker' or data.GetParam(3).lower()=='denkops' or data.GetParam(3).lower()=='updown'):
                            setMain(userId,data.GetParam(2).lower(),data.GetParam(3).lower())
                        else:
                            Parent.SendTwitchMessage('/w ' + data.User + ' Now specify a skin to complete the update. Type "!profile main ' + data.GetParam(2).lower() + ' <skin>" .... Valid skins are: \'discjam\', \'denkops\', \'updown\', \'aqua\', \'bumblebee\', \'forest\', \'peppermint\', \'picante\', \'seabird\', \'tangerine\', \'unconquered\', \'floral\', \'graffiti\', \'hautepink\', \'loverboy\', \'tealsforreals\', \'bronzepenny\', and \'steelworker\'.')

                    else:
                        Parent.SendTwitchMessage('/w ' + data.User + ' Type "!profile main <character>" to update your profile. Valid characters are: \'Gator\' , \'Haruka\' , \'Kahuna\' , \'Lannie\' , \'Makenna\' , and \'Stanton\' ')

                elif (data.GetParam(1).lower()=='sr'):

                    sr=0
                    invalid=False
                    try:
                        sr=int(data.GetParam(2))
                    except:
                        invalid=True

                    if (invalid==False):
                        setSR(userId,sr)
                    else:
                        Parent.SendTwitchMessage('/w ' + data.User + ' Type "!profile sr <number>" to update your profile. Specify your current singles skill rating for <number>.')
 
                elif (data.GetParam(1).lower()=='help'):
                     Parent.SendTwitchMessage('/w ' + data.User + ' Set your preferred REGION, COURT, MAIN, and current SKILL RATING using the \'!profile region\' , \'!profile court\' , \'!profile main\' , and \'!profile sr\' commands.')

                else:
                    Parent.SendTwitchMessage('/w ' + data.User + ' Invalid option. Valid options are: \'region\', \'court\', \'main\', and \'sr\' ')

            ### Return Players Profile  ##########################
            else:   
                getProfile(userId)

        if data.GetParam(0).lower() == '!toasty' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
            PlayToasty(userId)

        if data.GetParam(0).lower() == '!fnjwelcome' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
            m_Response = "Welcome to FRIDAY NIGHT JAMS! This is a viewers game, everyone is welcome to participate. Join in by typing \"!fnj enter\" in chat and set your current singles skill rating in your profile with \"!profile sr <value>\". Good luck and have fun!"
            Parent.SendTwitchMessage(m_Response)        

        if data.GetParam(0).lower() == '!fnjprofile' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
            m_Response = "Personalize your experience via the profile system! Type \"!profile\" and follow the returned instruction to set your preferred Court, Region, Main, and Skin. An alert with your main is displayed upon entering the arena, on the Challenge Tower, and for special events."
            Parent.SendTwitchMessage(m_Response)        

        if data.GetParam(0).lower() == '!fnjcommands' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):
            m_Response = "Viewers may interact during matches with these commands: !jam !bonk !stuff !curse !toasty !finish !clap !guy !boo !super !stanton - See the #fnj-commands channel. https://discord.gg/3zvmfmx"
            Parent.SendTwitchMessage(m_Response)        

        if data.GetParam(0).lower() == '!challenge' and not Parent.IsOnCooldown(ScriptName,m_Command) and Parent.HasPermission(data.User,m_CommandPermission,m_CommandInfo):

            if (data.GetParam(1).lower() == 'adv'):
                challengeAdvance()
            else:    
                challenge(userId)
 
    return

def Tick():
    return

#####################################

def enterArena(playerToAdd,skip):

    global playerActiveList
    global playerInactiveList
    
    playerActiveList=[]
    playerInactiveList=[]

    playAlert=False
    playerFoundActive=False
    playerFoundInactive=False

    # Determine if player has already entered the arena by reviewing both the 1)active (participants_in.txt) and 2) inactive (participants_out.txt) lists
    ReadPlayerActiveList()
    
    # Check if player found in active particpants list.
    for player in playerActiveList:
        if (playerToAdd == player.split(',')[0]):
            playerFoundActive=True

    # Return message stating if player has already entered the arena else check retrieve inactive list
    if (playerFoundActive == True):
        Parent.SendTwitchMessage('/w ' + playerToAdd + ' You have already entered the arena. Type "!fnj who" for a list of contestants currently in the arena. Type "!fnj exit" to leave the arena.')
    else:
        ReadPlayerInactiveList()
        for player in playerInactiveList:
            if (playerToAdd == player.split(',')[0]):
                playerFoundInactive=True    
                returningPlayer=player                    

    # If player found inactive then return message for the returning player and process the active and inactive lists accordingly
    if (playerFoundInactive == True):

        playAlert=True

        playerActiveList.append(returningPlayer)
        playerInactiveList.remove(returningPlayer)

        WritePlayerActiveList()
        WritePlayerInactiveList()

        m_Response = str(playerToAdd + ' has returned to the arena!')
        Parent.SendTwitchMessage(playerToAdd + ' has returned to the arena! Type "!fnj who" for a list of contestants currently in the arena. Type "!fnj exit" to leave the arena. ')

    # if player not found in either active or inactive lists then process player as new player
    if (playerFoundActive == False):
        if (playerFoundInactive == False):
            playAlert=True        

            playerActiveList.append(playerToAdd)
            WritePlayerActiveList()

            m_Response = str(playerToAdd + ' has entered the arena!')
            Parent.SendTwitchMessage(playerToAdd + ' has entered the arena! Type "!fnj who" for a list of contestants currently in the arena. Type "!fnj exit" to leave the arena. ')

    if (playAlert==True):
        if (skip==False):
            PlayAlert(playerToAdd, m_Response)

    return

def exitArena(playerToRemove):

    global playerActiveList
    global playerInactiveList
    
    playerActiveList=[]
    playerInactiveList=[]

    playerFoundActive=False
    playerFoundInactive=False

    ReadPlayerActiveList()
    ReadPlayerInactiveList()

    # Check if player found in active particpants list.
    for player in playerActiveList:
        if (playerToRemove == player.split(',')[0]):
            playerFoundActive=True
            leavingPlayer=player                    

    # If not found in active list, check inactive list.
    if (playerFoundActive==False):
        for player in playerInactiveList:
            if (playerToRemove == player.split(',')[0]):
                playerFoundInactive=True    

    # Return message stating if player to be removed was not found.
    if (playerFoundActive == False):

        if (playerFoundInactive == False):
            Parent.SendTwitchMessage('/w ' + playerToRemove + ' You were not not found in the arena. Type "!fnj enter" to re-enter the arena. Type "!fnj who" for a list of remaining contestants in the arena.')
        elif (playerFoundInactive == True):
            Parent.SendTwitchMessage('/w ' + playerToRemove + ' you have already left the arena. Type "!fnj enter" to re-enter the arena. Type "!fnj who" for a list of remaining contestants in the arena.')

    else:

        playerActiveList.remove(leavingPlayer)
        playerInactiveList.append(leavingPlayer)

        WritePlayerActiveList()
        WritePlayerInactiveList()

        Parent.SendTwitchMessage(playerToRemove + ' has left the arena. Type "!fnj enter" to re-enter the arena. Type "!fnj who" for a list of remaining contestants in the arena.')

        # Check for and remove any active challenges
        global challengersList
        challengersList=[]
        challengerFound=False

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','r') as file:
            player = file.readline().replace('\n','')
            while (player != ''):
                if (playerToRemove == player):
                    challengerFound=True
                challengersList.append(player)
                player = file.readline().replace('\n','')
                
        if (challengerFound == True):
            if (playerToRemove == challengersList[0] or playerToRemove == challengersList[1]) :
                challengersList.remove(playerToRemove)
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
                    for player in challengersList:
                        file.writelines(str(player+'\n'))
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challenges_total.txt','w') as file:
                    file.writelines(str(len(challengersList)))
                setChallengers()          
            else :
                challengersList.remove(playerToRemove)
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
                    for player in challengersList:
                        file.writelines(str(player+'\n'))
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challenges_total.txt','w') as file:
                    file.writelines(str(len(challengersList)))        
    return

def who():
    
    ReadPlayerActiveList()

    if (len(playerActiveList) == 0):
        Parent.SendTwitchMessage('The arena is empty. Jammers may type \'!kotc join\' to enter the arena.')
    else:

        playerList=''
        numPlayers = len(playerActiveList)

        random.shuffle(playerActiveList)
        for player in playerActiveList:
            playerList = playerList + player.split(',')[0] + ', ' 

        Parent.SendTwitchMessage(str(numPlayers) + ' contestants have entered the arena. They are: ' + playerList )

    return

#####################################

def AddPlayer(playerToAdd):

    global playerActiveList
    global playerInactiveList
    
    playerActiveList=[]
    playerInactiveList=[]

    playAlert=False
    playerFoundActive=False
    playerFoundInactive=False

    # Determine if player has already entered the arena by reviewing both the 1)active (participants_in.txt) and 2) inactive (participants_out.txt) lists
    ReadPlayerActiveList()
    
    # Check if player found in active particpants list.
    for player in playerActiveList:
        if (playerToAdd == player.split(',')[0]):
            playerFoundActive=True

    # Return message stating if player has already entered the arena else check retrieve inactive list
    if (playerFoundActive == True):
        Parent.SendTwitchMessage('/w ' + userId + ' ' + playerToAdd + ' has already entered the arena.')
    else:
        ReadPlayerInactiveList()
        for player in playerInactiveList:
            if (playerToAdd == player.split(',')[0]):
                playerFoundInactive=True    
                returningPlayer=player                    

    # If player found inactive then return message for the returning player and process the active and inactive lists accordingly
    if (playerFoundInactive == True):

        playAlert=True

        playerActiveList.append(returningPlayer)
        playerInactiveList.remove(returningPlayer)

        WritePlayerActiveList()
        WritePlayerInactiveList()

        m_Response = str(playerToAdd + ' has returned to the arena!')
        Parent.SendTwitchMessage('/w ' + userId + ' ' + playerToAdd + ' has been returned to the arena.')

    # if player not found in either active or inactive lists then process player as new player
    if (playerFoundActive == False):
        if (playerFoundInactive == False):
            playAlert=True        

            playerActiveList.append(playerToAdd)
            WritePlayerActiveList()

            m_Response = str(playerToAdd + ' has entered the arena!')
            Parent.SendTwitchMessage('/w ' + userId + ' ' + playerToAdd + ' has entered into the arena.')

    if (playAlert==True):
        PlayAlert(playerToAdd, m_Response)

    return

def RemovePlayer(playerToRemove):

    global playerActiveList
    global playerInactiveList
    
    playerActiveList=[]
    playerInactiveList=[]

    playerFoundActive=False
    playerFoundInactive=False

    ReadPlayerActiveList()
    ReadPlayerInactiveList()

    # Check if player found in active particpants list.
    for player in playerActiveList:
        if (playerToRemove == player.split(',')[0]):
            playerFoundActive=True
            leavingPlayer=player                    

    # If not found in active list, check inactive list.
    if (playerFoundActive==False):
        for player in playerInactiveList:
            if (playerToRemove == player.split(',')[0]):
                playerFoundInactive=True    

    # Return message stating if player to be removed was not found.
    if (playerFoundActive == False):

        if (playerFoundInactive == False):
            Parent.SendTwitchMessage('/w ' + userId + ' Failed to remove player. ' + playerToRemove + ' was not found in the active or inactive players list. Faile')
        elif (playerFoundInactive == True):
            Parent.SendTwitchMessage('/w ' + userId + ' Failed to remove player. ' + playerToRemove + ' has already left the arena.')

    else:

        playerActiveList.remove(leavingPlayer)
        playerInactiveList.append(leavingPlayer)

        WritePlayerActiveList()
        WritePlayerInactiveList()

        Parent.SendTwitchMessage(playerToRemove + ' has left the arena.')

        # Check for and remove any active challenges
        global challengersList
        challengersList=[]
        challengerFound=False

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','r') as file:
            player = file.readline().replace('\n','')
            while (player != ''):
                if (playerToRemove == player):
                    challengerFound=True
                challengersList.append(player)
                player = file.readline().replace('\n','')
                
        if (challengerFound == True):
            if (playerToRemove == challengersList[0] or playerToRemove == challengersList[1]) :
                challengersList.remove(playerToRemove)
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
                    for player in challengersList:
                        file.writelines(str(player+'\n'))
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challenges_total.txt','w') as file:
                    file.writelines(str(len(challengersList)))
                setChallengers()          
            else :
                challengersList.remove(playerToRemove)
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
                    for player in challengersList:
                        file.writelines(str(player+'\n'))
                with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challenges_total.txt','w') as file:
                    file.writelines(str(len(challengersList)))                
    return

def ClearArena():

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_in.txt','w') as file:
        file.writelines('')
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_out.txt','w') as file:
        file.writelines('')
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_total.txt','w') as file:
        file.writelines(str('0'))

    return

def ReturnSortedParticipants():

    global playerActiveList
    playerActiveList=[]    
    ReadPlayerActiveList()
    
    # Read SR for each challenged from their profile and update playerActiveList[]
    for x in range(len(playerActiveList)):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + playerActiveList[x-1] + '.txt','r') as file:
            profile = file.readline().replace('\n','')
            playerActiveList[x-1]=str(playerActiveList[x-1]) + ',' + str(profile.split(',')[4])

    for j in range(len(playerActiveList)):
        swapped = False
        i = 0
        while i < (len(playerActiveList) -1):
            if int(playerActiveList[i].split(',')[1]) > int(playerActiveList[i+1].split(',')[1]):
                playerActiveList[i],playerActiveList[i+1] = playerActiveList[i+1],playerActiveList[i]
                swapped = True
            i = i+1
        if swapped == False:
            break

    m_Response = "Current Participants\r\r"

    x=0
    while x < (len(playerActiveList) ):
        m_Response = m_Response + playerActiveList[x].split(',')[1] + '\t' + playerActiveList[x].split(',')[0] + '\r'
        x=x+1

    Parent.SendDiscordMessage(m_Response)
    
    return

#####################################

def ReadPlayerActiveList():  
    global playerActiveList
    playerActiveList=[]

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_in.txt','r') as file:
        player = file.readline().replace('\n','')
        while (player != ''):
            playerActiveList.append(player)
            player = file.readline().replace('\n','')

    return

def ReadPlayerInactiveList():
    global playerInactiveList
    playerInactiveList=[]

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_out.txt','r') as file:
        player = file.readline().replace('\n','')
        while (player != ''):
            playerInactiveList.append(player)
            player = file.readline().replace('\n','')

    return

def WritePlayerActiveList():
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_in.txt','w') as file:
        for player in playerActiveList:
            file.writelines(str(player+'\n'))
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_total.txt','w') as file:
        file.writelines(str(len(playerActiveList)))
    return

def WritePlayerInactiveList():

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\participants_out.txt','w') as file:
        for player in playerInactiveList:
            file.writelines(str(player+'\n'))
    return

#####################################
    
def PlayAlert(user, m_Response):
    
    profileFound=False
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
            profileFound=True

    if (profileFound==False):        

        profile = 'e,stadium,stanton,discjam,0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertText.txt','w') as file:
        file.writelines(str(m_Response))

    # Show players main and play gong...
    shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\' + profile.split(',')[2] + '-' + profile.split(',')[3] + '.png','C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png' )            
    Parent.PlaySound("C:/Users/Jason/AppData/Roaming/AnkhHeart/AnkhBotR2/Services/Scripts/DiscJamArena/alerts/alertBell.mp3", 100)
    time.sleep(3)
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertText.txt','w') as file:
        file.writelines('')
    time.sleep(2)
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png'):
        os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png' )

    return

def PlayNewChallenger(user, m_Response):
    
    profileFound=False
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
            profileFound=True

    if (profileFound==False):        

        profile = 'e,stadium,stanton,discjam,0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertText.txt','w') as file:
        file.writelines(str(m_Response))

    # Show players main and play gong...
    shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\' + profile.split(',')[2] + '-' + profile.split(',')[3] + '.png','C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png' )            
    Parent.PlaySound("C:/Users/Jason/AppData/Roaming/AnkhHeart/AnkhBotR2/Services/Scripts/DiscJamArena/alerts/herecomesanewchallenger.mp3", 100)
    time.sleep(3)
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertText.txt','w') as file:
        file.writelines('')
    time.sleep(2)
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png'):
        os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\alertImage.png' )

    return

def PlayToasty(user):
    
    profileFound=False
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
            profileFound=True

    if (profileFound==False):        

        profile = 'e,stadium,stanton,discjam,0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))

    shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\' + profile.split(',')[2] + '-' + profile.split(',')[3] + '.png','C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\toastyImage.png' )            
    time.sleep(1)
    Parent.PlaySound("C:\\Users\\Jason\\Documents\\My Twitch Stream\\DrWhistler Streamlabs Chatbot Sounds\\DiscJam\\mortal jam\\toasty.mp3", 200)
    time.sleep(2)
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\toastyImage.png'):
        os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\alerts\\toastyImage.png' )

    return

######### Profile ############################

def setRegion(user,region):
   
    profileUpdated=False

    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
        profile=region + ',' + profile.split(',')[1] + ',' + profile.split(',')[2] + ',' + profile.split(',')[3] + ',' + profile.split(',')[4]
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True
    else:
        profile = region + ',stadium,stanton,discjam,0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True

    if (profileUpdated==True) :

        m_Response = 'REGION: ' 
        
        if (profile.split(',')[0] == 'e'):
            m_Response = m_Response + 'US East'
        if (profile.split(',')[0] == 'w'):
            m_Response = m_Response + 'US West'
        if (profile.split(',')[0] == 'eu'):
            m_Response = m_Response + 'Europe'
        if (profile.split(',')[0] == 's'):
            m_Response = m_Response + 'South America'
        if (profile.split(',')[0] == 'o'):
            m_Response = m_Response + 'Oceanic'
        if (profile.split(',')[0] == 'a'):
            m_Response = m_Response + 'Southeast Asia'
            
        m_Response = m_Response + ' | COURT: ' + profile.split(',')[1] + ' | MAIN: ' + profile.split(',')[2] + ' | SKIN: ' + profile.split(',')[3] + ' | SR: ' + profile.split(',')[4]
        Parent.SendTwitchMessage('/w ' + user + ' Your profile has been updated. ' + m_Response)        
    else:
        Parent.SendTwitchMessage('/w ' + user + ' There was a problem updating your profile. Please contact the host or moderator.')

    return

def setCourt(user,court):

    profileUpdated=False
    
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
        profile=profile.split(',')[0] + ',' + court + ',' + profile.split(',')[2] + ',' + profile.split(',')[3] + ',' + profile.split(',')[4]
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True
    else:
        profile = 'e,' + court + ',stanton,discjam,0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True

    if (profileUpdated==True) :
        
        m_Response = 'REGION: ' 
        
        if (profile.split(',')[0] == 'e'):
            m_Response = m_Response + 'US East'
        if (profile.split(',')[0] == 'w'):
            m_Response = m_Response + 'US West'
        if (profile.split(',')[0] == 'eu'):
            m_Response = m_Response + 'Europe'
        if (profile.split(',')[0] == 's'):
            m_Response = m_Response + 'South America'
        if (profile.split(',')[0] == 'o'):
            m_Response = m_Response + 'Oceanic'
        if (profile.split(',')[0] == 'a'):
            m_Response = m_Response + 'Southeast Asia'
            
        m_Response = m_Response + ' | COURT: ' + profile.split(',')[1] + ' | MAIN: ' + profile.split(',')[2] + ' | SKIN: ' + profile.split(',')[3] + ' | SR: ' + profile.split(',')[4]
        Parent.SendTwitchMessage('/w ' + user + ' Your profile has been updated. ' + m_Response)        
    else:
        Parent.SendTwitchMessage('/w ' + user + ' There was a problem updating your profile. Please contact the host or moderator.')

    return

def setMain(user,main,skin):

    profileUpdated=False

    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
        profile= profile.split(',')[0] + ',' + profile.split(',')[1] + ',' + main + ',' + skin + ',' + profile.split(',')[4]
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True
    else:
        profile = 'e,stadium,' + main + ',' + skin + ',0'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True

    if (profileUpdated==True) :
        
        m_Response = 'REGION: ' 
        
        if (profile.split(',')[0] == 'e'):
            m_Response = m_Response + 'US East'
        if (profile.split(',')[0] == 'w'):
            m_Response = m_Response + 'US West'
        if (profile.split(',')[0] == 'eu'):
            m_Response = m_Response + 'Europe'
        if (profile.split(',')[0] == 's'):
            m_Response = m_Response + 'South America'
        if (profile.split(',')[0] == 'o'):
            m_Response = m_Response + 'Oceanic'
        if (profile.split(',')[0] == 'a'):
            m_Response = m_Response + 'Southeast Asia'
            
        m_Response = m_Response + ' | COURT: ' + profile.split(',')[1] + ' | MAIN: ' + profile.split(',')[2] + ' | SKIN: ' + profile.split(',')[3] + ' | SR: ' + profile.split(',')[4]
        Parent.SendTwitchMessage('/w ' + user + ' Your profile has been updated. ' + m_Response)        
    else:
        Parent.SendTwitchMessage('/w ' + user + ' There was a problem updating your profile. Please contact the host or moderator.')

    return

def setSR(user,sr):

    profileUpdated=False
    
    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')
        profile=profile.split(',')[0] + ',' + profile.split(',')[1] + ',' + profile.split(',')[2] + ',' + profile.split(',')[3] + ',' + str(sr)
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True
    else:
        profile = 'e,stadium,stanton,discjam,' + str(sr)
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
            profileUpdated=True

    if (profileUpdated==True) :
        
        m_Response = 'REGION: ' 
        
        if (profile.split(',')[0] == 'e'):
            m_Response = m_Response + 'US East'
        if (profile.split(',')[0] == 'w'):
            m_Response = m_Response + 'US West'
        if (profile.split(',')[0] == 'eu'):
            m_Response = m_Response + 'Europe'
        if (profile.split(',')[0] == 's'):
            m_Response = m_Response + 'South America'
        if (profile.split(',')[0] == 'o'):
            m_Response = m_Response + 'Oceanic'
        if (profile.split(',')[0] == 'a'):
            m_Response = m_Response + 'Southeast Asia'
            
        m_Response = m_Response + ' | COURT: ' + profile.split(',')[1] + ' | MAIN: ' + profile.split(',')[2] + ' | SKIN: ' + profile.split(',')[3] + ' | SR: ' + profile.split(',')[4]
        Parent.SendTwitchMessage('/w ' + user + ' Your profile has been updated. ' + m_Response)
                
    else:
        Parent.SendTwitchMessage('/w ' + user + ' There was a problem updating your profile. Please contact the host or moderator.')

    return

def getProfile(user):

    if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt'):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','r') as file:                    
            profile = file.readline().replace('\n','')

        m_Response = '/w ' + user + ' Your profile is set to REGION: ' 
        
        if (profile.split(',')[0] == 'e'):
            m_Response = m_Response + 'US East'
        if (profile.split(',')[0] == 'w'):
            m_Response = m_Response + 'US West'
        if (profile.split(',')[0] == 'eu'):
            m_Response = m_Response + 'Europe'
        if (profile.split(',')[0] == 's'):
            m_Response = m_Response + 'South America'
        if (profile.split(',')[0] == 'o'):
            m_Response = m_Response + 'Oceanic'
        if (profile.split(',')[0] == 'a'):
            m_Response = m_Response + 'Southeast Asia'
            
        m_Response = m_Response + ' | COURT: ' + profile.split(',')[1] + ' | MAIN: ' + profile.split(',')[2] + ' | SKIN: ' + profile.split(',')[3] + ' | SR: ' + profile.split(',')[4]
        Parent.SendTwitchMessage(m_Response)
        m_Response = '/w ' + user + ' Type "!profile help" for instruction to update you profile '
        Parent.SendTwitchMessage(m_Response)

    else:
        profile = 'e,stadium,stanton,discjam,500'
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + user + '.txt','w') as file:                    
            file.writelines(str(profile+'\n'))
        Parent.SendTwitchMessage('/w ' + user + ' A profile was not found so a default profile has been created for you. Proceed to set your preferred \'region\' and \'court\', \'main\', and current \'sr\' using the "!profile region", "!profile court", "!profile main", and "!profile sr" commands. Ask your host, moderator, and chat for help.')

    return

######### Challenge ############################

def challenge(challenger):
    
    # Check that challenger has entered the arena
    global playerActiveList
    playerActiveList=[]
    playerFoundActive=False
    ReadPlayerActiveList()

    for player in playerActiveList:
        if (challenger == player.split(',')[0]):
            playerFoundActive=True

    if (playerFoundActive == False):
        enterArena(challenger,True)

    global challengersList
    challengersList=[]
    challengerFound=False

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','r') as file:
        player = file.readline().replace('\n','')
        while (player != ''):
            challengersList.append(player)
            player = file.readline().replace('\n','')
        
    for player in challengersList:
        if (challenger == player.split(',')[0]):
            challengerFound=True

    if (challengerFound == True):
        Parent.SendTwitchMessage('/w ' + challenger + ' You already have an active challenge in the queue.')
    else:
        Parent.SendTwitchMessage(challenger + ' has challenged DrWhistler to a match!')
        
        challengersList.append(challenger)
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
            for player in challengersList:
                file.writelines(str(player+'\n'))
        
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challenges_total.txt','w') as file:
            file.writelines(str(len(challengersList)))
        m_Response = str(challenger + ' has challenged DrWhistler to a match!')
        PlayNewChallenger(challenger, m_Response)

        setChallengers()

    return

def challengeAdvance():
    
    global challengersList
    challengersList=[]

    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','r') as file:
        player = file.readline().replace('\n','')
        player = file.readline().replace('\n','')
        while (player != ''):
            challengersList.append(player)
            player = file.readline().replace('\n','')
        
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','w') as file:
        for player in challengersList:
            file.writelines(str(player+'\n'))
        
    setChallengers()

    return

def setChallengers():

    global challengersList
    challengersList=[]
    
    with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\challengers.txt','r') as file:
        player = file.readline().replace('\n','')
        while (player != ''):
            challengersList.append(player)
            player = file.readline().replace('\n','')

    if (len(challengersList) >= 1):
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_name.txt','w') as file:
            file.writelines(str(challengersList[0] + '\n'))

        # Read challengers profile for main and skin
        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + challengersList[0]  + '.txt','r') as file:
            profile = file.readline().replace('\n','')

        # Delete old challenger skin (challenger1.png) from Challenge Tower
        if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_image.png'):
            os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_image.png' )
        # Copy new challenger skin (challenger1.png) for Challenger Tower
        shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\' + profile.split(',')[2] + '-' + profile.split(',')[3] + '.png','C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_image.png' )

        if (len(challengersList)>=2):
            
            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_name.txt','w') as file:
                file.writelines(str(challengersList[1]+'\n'))

            # Read challengers profile for main and skin
            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\profiles\\' + challengersList[1]  + '.txt','r') as file:
                profile = file.readline().replace('\n','')

            # Delete old challenger skin (challenger1.png) from Challenge Tower
            if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png'):
                os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png' )
            # Copy new challenger skin (challenger1.png) for Challenger Tower
            shutil.copyfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamFNJ\\images\\' + profile.split(',')[2] + '-' + profile.split(',')[3] + '.png','C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png' )

        else:

            with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_name.txt','w') as file:
                file.writelines('\n')
            if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png'):
                os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png' )
    else:

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_name.txt','w') as file:
            file.writelines('\n')
        if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_image.png'):
            os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_current_image.png' )

        with open('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_name.txt','w') as file:
            file.writelines('\n')
        if os.path.isfile('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png'):
            os.remove('C:\\Users\\Jason\\AppData\\Roaming\\AnkhHeart\\AnkhBotR2\\Services\\Scripts\\DiscJamArena\\wednesday_jams\\opponent_next_image.png' )

    return
