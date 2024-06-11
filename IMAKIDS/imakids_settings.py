usOnset = 2 # CS-US interval in seconds
usDur = 6 # US duration in seconds
minITI = 3 # minimal ITI duration in seconds
maxITI = 5 # maximal ITI duration in seconds

nrBlocks = 3 # number of blocks in conditioning phase
nrTrials = 6 # per CS and block

picSize = 0.5 # in units of screen height
crossSize = 0.05 # size for fixation cross in units of screen height

scaleSize = (1.25, 0.25)
scalePos = (0, -0.25)
frameWidth = scaleSize[0] / 5
frameHeight = scaleSize[1]
framePositions = [(scalePos[0] + i*frameWidth, scalePos[1]) for i in (-2, -1, 0, 1, 2)]

buttonsVal = ["f","g","h","j","k"] # keyboard buttons for valence rating (values from 0 to len-1)
buttonsArous = ["v","b","n","m","comma"] # keyboard buttons for arousal rating (values from 0 to len-1)
exitKeys = ["q","t"] # press the first key and - within a second - the second key to abort experiment
contKeys = ["c","t"] # press the first key and - within a second - the second key to continue experiment after instructions
repKeys = ["r","p"] # press the first key and - within a second - the second key to repeat information / imagery instructions
eegKeys = ["e","g"]
partContKey = "space" # button for participants to continue
#successKey = "rightbracket" # press key to inform that contingencies have been learned and experiment can continue --- bracketright = '+' on German keyboard
#repeatKey = "slash" # press key to inform that contingencies have not been learned and learning trial will be repeated  --- slash = '-' on German keyboard
