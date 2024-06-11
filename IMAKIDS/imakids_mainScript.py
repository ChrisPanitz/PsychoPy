########################
### import libraries ###
########################

from psychopy import visual, core, event, sound, gui, logging, parallel
from psychopy.hardware import keyboard
import os
import random
import csv
from datetime import datetime
import numpy as np
import imakids_settings as settings



###############################
### define custom functions ###
###############################

# Function to quit experiment
def check4exitKey(exitKeys):
    keys = kb.getKeys()
    if exitKeys[0] in keys:
        core.wait(1)
        keys = kb.getKeys()
        if exitKeys[1] in keys:
            core.quit()



# Function to collect ratings via keyboard
def collectRatings(scaleImage, scaleSound, stimulusImage, scaleButtons):
    presFixCross(1.5)
    
    stimulusImage.draw()
    scaleImage.draw()
    win.flip()
    soundStim = sound.Sound(scaleSound)
    soundStim.play()
    #core.wait(soundStim.getDuration()) # commented out: you can rate before end of audio
    while True:
        check4exitKey(settings.exitKeys)
        stimulusImage.draw()
        scaleImage.draw()
        win.flip()
        win.mouseVisible = False
        pressedKey = kb.getKeys(keyList = scaleButtons)
        if pressedKey:
            frameStim = visual.Rect(win, width = settings.frameWidth, height = settings.frameHeight, pos = settings.framePositions[scaleButtons.index(pressedKey[0].name)], lineColor = "green", lineWidth = 10)
            stimulusImage.draw()
            scaleImage.draw()
            frameStim.draw()
            win.flip()
            win.mouseVisible = False
            soundStim.stop()
            core.wait(1)
            
            return scaleButtons.index(pressedKey[0].name)



# Function to present audio file together with picture (for instructions)
def presentAudio(audioFile, picStim, contAfter):
    presFixCross(1.5)
    
    check4exitKey(settings.exitKeys)
    instSound = sound.Sound(audioFile)
    
    picStim.draw()
    win.flip()
    win.mouseVisible = False
    instSound.play()
    core.wait(instSound.getDuration())
    check4exitKey(settings.exitKeys)
    
    if isinstance(contAfter, int):
        core.wait(contAfter)
    elif isinstance(contAfter, str):
        while True:
            core.wait(0.010)
            if kb.getKeys(keyList = [contAfter]):
                break


# Function to present fixation cross
def presFixCross(fixDur):
    fixCross = visual.TextStim(win, text = "+", pos = (0, 0))
    fixCross.size = settings.crossSize
    fixCross.draw()
    win.flip()
    win.mouseVisible = False
    core.wait(fixDur)    
    check4exitKey(settings.exitKeys)
    
    
    
# Function to present conditioning trial    
def presTrial(csImage, usImage, usOnset, usDur, minITI, maxITI, PPcodes):
    itiThisTime = random.uniform(minITI, maxITI)
    check4exitKey(settings.exitKeys)
            
    csImage.draw()
    win.flip()
    win.mouseVisible = False
    port.setData(PPcodes[0])
    core.wait(usOnset)
    port.setData(0)
    check4exitKey(settings.exitKeys)
    
    csImage.draw()
    usImage.draw()
    win.flip()
    win.mouseVisible = False
    port.setData(PPcodes[1])
    core.wait(usDur)
    port.setData(0)
    check4exitKey(settings.exitKeys)
            
    presFixCross(itiThisTime)



# Function to send marker via parallel port
def sendMarker(portCode):
    port.setData(portCode)
    core.wait(0.010)
    port.setData(0)



# Function to ask experimenter whether experiment section should be repeated    
def checkIfRepeat(repKeys, contKeys, exitKeys, textStr, picStim):
    instText = visual.TextStim(win, text = textStr, pos = (0, -0.45))
    instText.size = 0.03
    instText.draw()
    if picStim is not None:
        picStim.draw()
    win.flip()
    win.mouseVisible = False
    
    while True:
        core.wait(0.010)
        keys = kb.getKeys()
        if repKeys[0] in keys:
            core.wait(1)
            keys = kb.getKeys()
            if repKeys[1] in keys:
                return True
        if contKeys[0] in keys:
            core.wait(1)
            keys = kb.getKeys()
            if contKeys[1] in keys:
                return False
        if exitKeys[0] in keys:
            core.wait(1)
            keys = kb.getKeys()
            if exitKeys[1] in keys:
                core.quit()



# Function for pause that can be ended by participant via key press                
def participantContinues(audioFile, picStim, contKey, exitKeys):
    instSound = sound.Sound(audioFile)
    
    picStim.draw()
    win.flip()
    win.mouseVisible = False    
    instSound.play()
    core.wait(instSound.getDuration())
    
    while True:
        core.wait(0.010)
        if contKey in keys:
            break
        if exitKeys[0] in keys:
            core.wait(1)
            keys = kb.getKeys()
            if exitKeys[1] in keys:
                core.quit()
                

    
#############################       
### set up the experiment ###
#############################
                
# setup keyboard object to register key presses
kb = keyboard.Keyboard()
kb.clock.reset()
            
# Get the current directory of the script
currentDir = os.path.dirname(os.path.abspath(__file__))

# Get current date
currentDate = datetime.now().strftime("%d.%m.%Y")

# Create a GUI for experimenter prompts
expInfo = {"PartID": "", "PermAnimal": "", "PermLandscape": "", "Birthdate (dd.mm.yyyy)": "", "Current Date (dd.mm.yyyy)": currentDate, "Gender (m/f/d)":""}
expDialog = gui.DlgFromDict(expInfo, title = "Enter Participant Information", sortKeys = False)
if not expDialog.OK:
    core.quit()
if int(expInfo['PermAnimal']) < 1 or int(expInfo['PermAnimal']) > 3 or int(expInfo['PermLandscape']) < 1 or int(expInfo['PermLandscape']) > 3:
    print("Please use numbers from 1 to 3 for permutations")
    core.quit()
if expInfo['Gender (m/f/d)'] not in ["m","f","d"]:
    print("Please use m, f, or d for gender")
    core.quit()

# save GUI input into variables with more convenient names
partID = expInfo["PartID"]
permAnimal = expInfo["PermAnimal"]
permLandscape = expInfo["PermLandscape"]
partGender = expInfo["Gender (m/f/d)"]

# compute age of participant
birthdate = datetime.strptime(expInfo["Birthdate (dd.mm.yyyy)"], "%d.%m.%Y")
currentDate = datetime.strptime(expInfo["Current Date (dd.mm.yyyy)"], "%d.%m.%Y")
# age in months
yearsDiff = currentDate.year - birthdate.year
monthsDiff = currentDate.month - birthdate.month
ageInMonths = yearsDiff*12 + monthsDiff
if currentDate.day < birthdate.day:
    ageInMonths = ageInMonths - 1
# age in days
#age = datetime.strptime(expInfo["Current Date (dd.mm.yyyy)"], "%d.%m.%Y") - datetime.strptime(expInfo["Birthdate (dd.mm.yyyy)"], "%d.%m.%Y")
#ageInDays = age.days

# Set up logging
logFile = logging.LogFile(f"logfiles/{partID}_imakids_log.log", level = logging.INFO, filemode = "w")
logging.console.setLevel(logging.WARNING)

# Create window (DOUBLE CHECK) ##################################################
win = visual.Window(
    size = [1920, 1080],
    fullscr = True,
    allowGUI = False,
    winType = 'pyglet',
    units = 'height',
    #allowStencil = True,
    checkTiming = False,
    waitBlanking = True
)

### Load images and audio files ###
# define stimulus folders
picFolder = os.path.join(currentDir, "pictures")
audioFolder = os.path.join(currentDir, "audioscripts")

# picture stimuli (animals & landscapes)
animalImages = [visual.ImageStim(win, image = os.path.join(picFolder, f"animal{i}.png"), size = (settings.picSize, settings.picSize)) for i in range(1, 4)]
animalImages4ratings = [visual.ImageStim(win, image = os.path.join(picFolder, f"animal{i}.png"), size = (0.50, 0.50), pos = (0, 0.20)) for i in range(1, 4)]
landscapeImages = [visual.ImageStim(win, image = os.path.join(picFolder, f"landscape{i}.png"), size = (settings.picSize, settings.picSize)) for i in range(1, 4)]
landscapeImages4ratings = [visual.ImageStim(win, image = os.path.join(picFolder, f"landscape{i}.png"), size = (0.50, 0.50), pos = (0, 0.20)) for i in range(1, 4)]
# pictures and audio instructions for valence & arousal ratings
scaleValence = visual.ImageStim(win, image = os.path.join(picFolder, "ratingVal.png"), size = settings.scaleSize, pos = settings.scalePos)
scaleArousal = visual.ImageStim(win, image = os.path.join(picFolder, "ratingArous.png"), size = settings.scaleSize, pos = settings.scalePos)
valenceAnimalSoundFile = os.path.join(audioFolder, "scalesValenceAnimal.wav")
arousalAnimalSoundFile = os.path.join(audioFolder, "scalesArousalAnimal.wav")
valenceLandscapeSoundFile = os.path.join(audioFolder, "scalesValenceLandscape.wav")
arousalLandscapeSoundFile = os.path.join(audioFolder, "scalesArousalLandscape.wav")
# pictures & audio stimuli for breaks, etc.
waitImage = visual.ImageStim(win, image = os.path.join(picFolder, "waitForExperimenter.png"), size = (settings.picSize, settings.picSize))
waitSoundFile = os.path.join(audioFolder, "wait4experimenter.wav")
greenArrowImage = visual.ImageStim(win, image = os.path.join(picFolder, "greenArrow.png"), size = (settings.picSize, settings.picSize))
continueSoundFile = os.path.join(audioFolder, "continueAfterPause.wav")
startSoundFile = os.path.join(audioFolder, "startConditioning.wav")



# apply permutations
# animal <==> threat info / imagery:
# 1st in list = harmless info / harmless imagery
# 2nd in list = threat info / harmless imagery
# 3rd in list = threat info / threat imagery

# animals
if permAnimal == "1":
    # use original picture list when permAnimal == 1
    infoSoundList = [os.path.join(audioFolder, "info_animal1_harmless.wav"), os.path.join(audioFolder, "info_animal2_threat.wav"), os.path.join(audioFolder, "info_animal3_threat.wav")]
    imagerySoundList = [os.path.join(audioFolder, "imagery_animal1_harmless.wav"), os.path.join(audioFolder, "imagery_animal2_harmless.wav"), os.path.join(audioFolder, "imagery_animal3_threat.wav")]
elif permAnimal == "2":
    animalImages = [animalImages[i] for i in (1, 2, 0)]
    animalImages4ratings = [animalImages4ratings[i] for i in (1, 2, 0)]
    infoSoundList = [os.path.join(audioFolder, "info_animal2_harmless.wav"), os.path.join(audioFolder, "info_animal3_threat.wav"), os.path.join(audioFolder, "info_animal1_threat.wav")]
    imagerySoundList = [os.path.join(audioFolder, "imagery_animal2_harmless.wav"), os.path.join(audioFolder, "imagery_animal3_harmless.wav"), os.path.join(audioFolder, "imagery_animal1_threat.wav")]
elif permAnimal == "3":
    animalImages = [animalImages[i] for i in (2, 0, 1)]
    animalImages4ratings = [animalImages4ratings[i] for i in (2, 0, 1)]
    infoSoundList = [os.path.join(audioFolder, "info_animal3_harmless.wav"), os.path.join(audioFolder, "info_animal1_threat.wav"), os.path.join(audioFolder, "info_animal2_threat.wav")]
    imagerySoundList = [os.path.join(audioFolder, "imagery_animal3_harmless.wav"), os.path.join(audioFolder, "imagery_animal1_harmless.wav"), os.path.join(audioFolder, "imagery_animal2_threat.wav")]

# landscapes
# use original picture list when permLandscape == 1    
if permLandscape == "2":
    landscapeImages = [landscapeImages[i] for i in (1, 2, 0)]
    landscapeImages4ratings = [landscapeImages4ratings[i] for i in (1, 2, 0)]
elif permLandscape == "3":
    landscapeImages = [landscapeImages[i] for i in (2, 0, 1)]
    landscapeImages4ratings = [landscapeImages4ratings[i] for i in (2, 0, 1)]



# ratings
# variables to write rating index into file and randomize order of ratings
# ratOrder will also be used for rendomized order of animal info/ imagery instructions
ratingCounter = 1
ratingOrder = [0, 1, 2]

# define folder & file to write ratings into
ratFolder = os.path.join(currentDir, "ratings")
ratingFileName = os.path.join(ratFolder, f"{partID}_imakids_ratings.txt")
# check if rating file for participant already exists; if it exists, stop script
if os.path.isfile(ratingFileName):
    print("A rating file for this participant ID already exists.")
    core.quit()

# write header for rating file
ratingFile = open(ratingFileName, "w")
ratingFile.write("partInd; gender; ageInMonths; permAnimal; permLandscape; ratingInd; stimClass; scale; stimInd; rating\n")
ratingFile.close()



# set up parallel port and set pins to low
port = parallel.ParallelPort(address='/dev/parport0')
port.setData(0)
# marker of conditioning phase start (marker code will count up over blocks, marking block starts and ends)
blockMarker = 101



######################
### run experiment ###
######################

# Experimenter gives instructions for experiment start - delivering background info on animals via audio scripts
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tierinfos: weiter mit c + t", None)
    
# Provide background information on animals via audio scripts
# ramdomize oder of animals to be instructed
random.shuffle(ratingOrder)

# play information audio scripts; allows experimenter to repeat each animal and to start over after all three animals 
repeatTraining = True
while repeatTraining:
    repeatAnimal = True
    while repeatAnimal:
        presentAudio(infoSoundList[ratingOrder[0]], animalImages[ratingOrder[0]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[0]])
    repeatAnimal = True
    while repeatAnimal:
        presentAudio(infoSoundList[ratingOrder[1]], animalImages[ratingOrder[1]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[1]])
    repeatAnimal = True
    while repeatAnimal:
        presentAudio(infoSoundList[ratingOrder[2]], animalImages[ratingOrder[2]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[2]])
    repeatTraining = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tiere von vorne: r + p          Fortfahren: c + t", None)

# experimenter announces first round of valence and arousal ratings for animals
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tierratings: weiter mit c + t", None)



# collect ratings for animals in random order
animalRatingsVal = [-99, -99, -99]
animalRatingsArous = [-99, -99, -99]
random.shuffle(ratingOrder)

# allow to repeat valence and arousal ratings for first animal
repeatRatings = True
while repeatRatings == True:
    animalRatingsVal[ratingOrder[0]] = collectRatings(scaleValence, valenceAnimalSoundFile, animalImages4ratings[ratingOrder[0]], settings.buttonsVal)
    animalRatingsArous[ratingOrder[0]] = collectRatings(scaleArousal, arousalAnimalSoundFile, animalImages4ratings[ratingOrder[0]], settings.buttonsArous)
    repeatRatings = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Ratings wiederholen: r + p          Fortfahren: c + t", None)    

# continue with 2nd and 3rd animal
presFixCross(1)
for i in ratingOrder[1:]:
    animalRatingsVal[i] = collectRatings(scaleValence, valenceAnimalSoundFile, animalImages4ratings[i], settings.buttonsVal)
    animalRatingsArous[i] = collectRatings(scaleArousal, arousalAnimalSoundFile, animalImages4ratings[i], settings.buttonsArous)

# write ratings into file
ratingFile = open(ratingFileName, "a")

for rat in range(3):
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; animal; valence; {rat}; {animalRatingsVal[rat]}\n")
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; animal; arousal; {rat}; {animalRatingsArous[rat]}\n")

ratingFile.close()

# set rating counter +1 for next round of ratings (will be written into file)
ratingCounter = ratingCounter + 1



# experimenter explains imagery training
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Instruktionen Imagination: weiter mit c + t", None)

# give instructions for imagery via audio scripts (in random animal order)
random.shuffle(ratingOrder)

repeatTraining = True
while repeatTraining:
    repeatAnimal = True
    while repeatAnimal:
        presentAudio(imagerySoundList[ratingOrder[0]], animalImages[ratingOrder[0]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[0]])
    repeatAnimal = True
    while repeatAnimal:    
        presentAudio(imagerySoundList[ratingOrder[1]], animalImages[ratingOrder[1]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[1]])
    repeatAnimal = True
    while repeatAnimal:
        presentAudio(imagerySoundList[ratingOrder[2]], animalImages[ratingOrder[2]], 0)
        repeatAnimal = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tier wiederholen: r + p          Fortfahren: c + t", animalImages[ratingOrder[2]])
    repeatTraining = checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Tiere von vorne: r + p          Fortfahren: c + t", None)    
        



# conditioning phase
# experimenter instructs conditioning phase
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Instruktionen Bilderaufgabe: weiter mit c + t", None)

# experimenter leaves room and makes sure that EEG/ ECG is recorded
checkIfRepeat(settings.repKeys, settings.eegKeys, settings.exitKeys, "Raum verlassen & EEG starten (Workspace: imakids.rwksp): weiter mit e + g", None)

# participant starts paradigm
presentAudio(startSoundFile, greenArrowImage, settings.partContKey)

# actual conditioning phase
trialVec = np.repeat((0,1,2), settings.nrTrials)

for blInd in range(settings.nrBlocks):  # 3 blocks
    # randomize trial order
    random.shuffle(trialVec)
    
    # send parallel port marker to mark start of trial block
    sendMarker(blockMarker)
    blockMarker = blockMarker + 1
    
    presFixCross(3)
    
    # present all trials in a block
    for trialInd in range(len(trialVec)):
        presTrial(landscapeImages[trialVec[trialInd]], animalImages[trialVec[trialInd]], settings.usOnset, settings.usDur, settings.minITI, settings.maxITI, (11+trialVec[trialInd], 21+trialVec[trialInd]))
    
    # send parallel port marker to mark end of trial block
    sendMarker(blockMarker)
    blockMarker = blockMarker + 1
    
    # after first block
    if blInd == 0:
        # experimenter comes in and makes sure that participant remembers animal - imagery contingencies
        presentAudio(waitSoundFile, waitImage, 5)
        checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Kontingenzen wiederholen: dann Raum verlassen und weiter mit c + t", None)
    # after each following block (except the very last one)
    elif blInd < settings.nrBlocks - 1:
        # break, participants continues experiment with key press
        presentAudio(continueSoundFile, greenArrowImage, settings.partContKey)
    


# after last conditioning trial
# announce to participant that experimenter will come back
presentAudio(waitSoundFile, waitImage, 5)

# make sure to stop recording and announce 2nd rating for animals
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "EEG stoppen & Instruktionen Tierratings: weiter mit c + t", None)

# collect ratings for animals
animalRatingsVal = [-99, -99, -99]
animalRatingsArous = [-99, -99, -99]
random.shuffle(ratingOrder)

for i in ratingOrder:
    animalRatingsVal[i] = collectRatings(scaleValence, valenceAnimalSoundFile, animalImages4ratings[i], settings.buttonsVal)
    animalRatingsArous[i] = collectRatings(scaleArousal, arousalAnimalSoundFile, animalImages4ratings[i], settings.buttonsArous)

# instructions for valence and arousal ratings of landscapes
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Instruktionen Ortsratings: weiter mit c + t", None)

# collect ratings for landscapes
landscapeRatingsVal = [-99, -99, -99]
landscapeRatingsArous = [-99, -99, -99]
random.shuffle(ratingOrder)

for i in ratingOrder:
    landscapeRatingsVal[i] = collectRatings(scaleValence, valenceLandscapeSoundFile, landscapeImages4ratings[i], settings.buttonsVal)
    landscapeRatingsArous[i] = collectRatings(scaleArousal, arousalLandscapeSoundFile, landscapeImages4ratings[i], settings.buttonsArous)

# write ratings into file
ratingFile = open(ratingFileName, "a")

for rat in range(3):
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; animal; valence; {rat}; {animalRatingsVal[rat]}\n")
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; animal; arousal; {rat}; {animalRatingsArous[rat]}\n")
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; landscape; valence; {rat}; {landscapeRatingsVal[rat]}\n")
    ratingFile.write(f"{partID}; {partGender}; {ageInMonths}; {permAnimal}; {permLandscape}; {ratingCounter}; landscape; arousal; {rat}; {landscapeRatingsArous[rat]}\n")

ratingFile.close()



# That's it!
checkIfRepeat(settings.repKeys, settings.contKeys, settings.exitKeys, "Experiment zu Ende: Kontingenzen abfragen und Experiment schließen mit c + t", None)

# Close the window
win.close()
