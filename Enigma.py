# Change this to True if you want to be able to input the settings manually when this is ran.
manualInput = False
message = input("What is your message: ").upper()
originalMsg = message
blank = ""

# Put in any settings you want the program to auto-start with underneath.

plugboard = "".upper() # Connects two letters together, AB means A becomes B, B becomes A. Crucial for decoding.

initial = ["A", "A", "A"] # The starting position

ringSettings = ["A", "A", "A"] # What letter A starts on for each Rotor, if it's B for Rotor III, then A would be in position 2 instead of 1

# Rotor Pos:   I    II    III
rotorOrder = ["I", "II", "III"]

reflector = "B"

# ----------- Do not touch anything past this point -----------

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotors = {
    # last letter of the the encode is the turnover, point of the next dial turning for the first dial, should not be considered during encryption, but should be when adding.
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJQ", 
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOEE", 
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQOV", 
    "IV":  "ESOVPZJAYQUIRHXLNFTGKDCMWBJ", 
    "V":   "VZBRGITYUPSDNHLXAWMJQOFECKZ"
    }
rotorsInUse = ["", "", ""]
reflectors = {
    # similar to plugboard, every letter corresponds to another, except this is not adjustable by users, other than which reflector to use.
    "B": "AY BR CU DH EQ FS GL IP JX KN MO TZ VW",
    "C": "AF BV CP DJ EI GO HY KR LZ MX NW QT SU"
}

if(manualInput == True):
    plugboard = input("Input which letters you would like to connect (i.e. \"AB CD EF\") Do not use the same letter twice.\n").upper()
    settingsHold = input("Type initial position of the original message (i.e. \"ABC\") Make sure it's the same order and letters.\n").upper()
    initial[0] = settingsHold[0]
    initial[1] = settingsHold[1]
    initial[2] = settingsHold[2]
    settingsHold = input("Type ring setting of the original message (i.e. \"ABC\") If the ring setting is in numbers, type the letters that correspond to each number (i.e. 1 is A, 2 is B).\n").upper()
    ringSettings[0] = settingsHold[0]
    ringSettings[1] = settingsHold[1]
    ringSettings[2] = settingsHold[2]
    rotorOrder[0] = input("Pick 1 of 5 rotors for rotor slot 1, going left to right:\n(I)\n(II)\n(III)\n(IV)\n(V)\n").upper()
    rotorOrder[1] = input("Pick 1 of 5 rotors for rotor slot 2:\n(I)\n(II)\n(III)\n(IV)\n(V)\n").upper()
    rotorOrder[2] = input("Pick 1 of 5 rotors for rotor slot 3:\n(I)\n(II)\n(III)\n(IV)\n(V)\n").upper()
    reflector = input("Pick B or C reflector by typing \"B\" or \"C\".\n").upper()
print(message)
for i in message:
    if i.isalpha() == False:
        continue
    else:
        blank += i
message = blank

#for ring setting, find location of the letter in the alphabet, move back (B to A) by (alphabet.index(ringSetting[num]) and then find that letter in the encrypted code, and shift the index in encryp replace it there.
#FIX THE THING FOR THE RING SETTING
#Shift it over by one? idk
#Allow for Rotors to do multiple of same rotor on different settings
#Fix Rotor settings to allow for multiple of same rotor
for i in range(len(rotorOrder)):
    hold = rotors[rotorOrder[i]]
    notch = rotors[rotorOrder[i]]
    for x in range(26):
        index = alphabet.index(rotors[rotorOrder[i]][x]) - alphabet.index(ringSettings[i])
        if(index < 0):
            index += 26
        index = rotors[rotorOrder[i]].index(alphabet[index])
        index += alphabet.index(ringSettings[i])
        if(index > 25):
            index -= 26
        hold = hold[:index] + rotors[rotorOrder[i]][x] +hold[index+1:]

    rotorsInUse[i] = hold

def rotorEncode(obj, num):

    #r and 0 for obj and num
    indexOffset = alphabet.index(obj) + alphabet.index(initial[num])
    if(indexOffset > 25):
        indexOffset -= 26
    hold = rotorsInUse[num]   [indexOffset]
    indexOffset = alphabet.index(hold) - alphabet.index(initial[num])
    if(indexOffset >= 0):
        hold = alphabet[indexOffset]
    else:
        hold = alphabet[indexOffset + 26]
    return hold

def rotorEncodeBackwards(obj, num):
    indexOffset = alphabet.index(obj) + alphabet.index(initial[num])
    if indexOffset > 25:
        indexOffset -= 26
    indexOffset = rotorsInUse[num].index(alphabet[indexOffset])
    indexOffset -= alphabet.index(initial[num])
    if(indexOffset >= 0):
        hold = alphabet[indexOffset]
    else:
        hold = alphabet[indexOffset + 26]
    return hold

def switchLetters(instructions, obj):
    switch = ""
    for i in range(len(obj)):
        if (obj[i] in instructions):
            if(instructions.index(obj[i]) + 1 < len(instructions) and instructions[instructions.index(obj[i]) + 1] != " "):
                switch += instructions[instructions.index(obj[i]) + 1]
            else:
                switch += instructions[instructions.index(obj[i]) - 1]
        else:
            switch += obj[i]
    return switch

output = switchLetters(plugboard, message)
final = ""
for i in output:
     #if the current letter is (notch) then switch to next letter and tell the next rotor to also switch, if it's the second rotor and its currently the (notch) then rotate the third and first rotors as well as the second
    # for the first rotor, switch make sure to check if Z for every single one, if Z is true, then set to A
    # for the second rotor, check what first is and if second is notch, if true, switch
    # third, check what second is, if second is notch, switch
    # could be an issue if the index is 26
    # if middle is E then move
    if(initial[1] == rotorsInUse[1][26]):
        if(initial[0] == "Z"):
            initial[0] = "A"
        else:
            initial[0] = alphabet[alphabet.index(initial[0]) + 1]
       
    if(initial[2] == rotorsInUse[2][26] or initial[1] == rotorsInUse[1][26]):
        if(initial[1] == "Z"):
            initial[1] = "A"
        else:
            initial[1] = alphabet[alphabet.index(initial[1]) + 1]

    if(initial[2] == "Z"):
        initial[2] = "A"
    else:
        initial[2] = alphabet[alphabet.index(initial[2]) + 1]

        
    hold = rotorEncode(i, 2)
    hold = rotorEncode(hold, 1)
    hold = rotorEncode(hold, 0)
    hold = switchLetters(reflectors[reflector], hold)
    hold = rotorEncodeBackwards(hold, 0)
    hold = rotorEncodeBackwards(hold, 1)
    hold = rotorEncodeBackwards(hold, 2)
    hold = switchLetters(plugboard, hold)
    final += hold

finalMsg = ""
offset = 0
for i in range(len(originalMsg)):
    if(originalMsg[i].isalpha() == False):
        finalMsg += originalMsg[i]
        offset += 1
    else:
        finalMsg += final[i - offset]

print(finalMsg)
# message = open("Output.txt", "w")
# message.write(finalMsg)
# message.close()
