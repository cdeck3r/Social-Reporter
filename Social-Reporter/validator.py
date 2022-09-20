import time
import config
import helper

def relevantLecturerGiven(current_photo, savedContentList):
    if(isAPerson(current_photo) == False):
        return False
    if(isEmotionRelevant(current_photo) == False):
        return False
    if(isRatioOkay(current_photo) == False):
        return False
    if(isPositionNew(current_photo, savedContentList)):
        return True
    if(isLongTimeSpent(savedContentList)):
        return True

def isAPerson(current_photo):
    if not current_photo.person_boxes:
        print('no person found')
        return False

def isEmotionRelevant(current_photo):
    if not current_photo.emotions:
        print('0 emotion found')
        return False
    if(len(current_photo.emotions) > 2):
        print('to much emotions')
        return False

    myList = list(filter(lambda x: getListOfHappyEmotions(x), current_photo.emotions))
    if len(myList) == 1:
        return True
    else:
        print('only irrelevand emotion')
        return False

def getListOfHappyEmotions(emotion):
    if(emotion=='Angry' or emotion=='Disgust' or emotion=='Fear' or emotion=='Sad' or emotion=='Neutral'):
        return False
    else:
        return True

def isRatioOkay(current_photo):
# x1, y1, x2, y2 = int(round(boxes[i][0])), int(round(boxes[i][1])), int(round(boxes[i][2])), int(round(boxes[i][3]))
    person_box = current_photo.main_person
    if not person_box:
        print('person not in main place of center')
        return False

    ToBreitPersons = list(filter(lambda x: getToBreitPersonForDozent(x), current_photo.person_boxes))
    if(len(ToBreitPersons) > 0):
        print('to big person available')
        return False

    face_box = current_photo.face_boxes

    ToBigFaces = list(filter(lambda x: getToBigFacesForDozent(x), face_box))
    if(len(ToBigFaces) > 0):
        print('to big faces available')
        return False

    face_in_person = 0
    for i in range(len(face_box)):
        #print('person_x1=%s < face_x1=%s  person_y1=%s < face_y1=%s  person_x2=%s > face_x2=%s  person_y2=%s > face_y2=%s' 
        #    % (person_box[0], face_box[i][0], person_box[1], face_box[i][1], person_box[2], face_box[i][2], person_box[3], face_box[i][3]))
        if(person_box[0] < face_box[i][0] and person_box[1] < face_box[i][1] and person_box[2] > face_box[i][2] and person_box[3] > face_box[i][3]):
            face_in_person = 1       
        if(face_in_person != 1):
            #print('face not in main person box')
            return False

def isPositionNew(current_photo, savedContentList):
    current_person_box = current_photo.main_person
    current_center = (current_person_box[0] + current_person_box[2]) / 2
    myList = list(filter(lambda x: isPosNotChanged(x, current_center), savedContentList))
    if not myList:
        #print('PosChanged --> Valid')
        return True
    if not savedContentList:
        #print('not in list --> Valid')
        return True


def isPosNotChanged(x, current_center):
    if(len(x.photo_object.person_boxes) > 0):
        element_box = x.photo_object.person_boxes[0]
        element_center = (element_box[0] + element_box[2]) / 2
        diff_center = abs(current_center - element_center)
        if(diff_center < config.frame_width * 0.15):
            return True

def isLongTimeSpent(savedContentList):
    if(helper.isNotSavedInGivenTime(savedContentList, "lecturer")):
        return True

    myList = list(filter(lambda x: getTimeDiff(x) < config.time_to_leave_in_sec, savedContentList))
    if(len(myList) == 0):
        #print('already similar avail. But far ago --> Valid')        
        return True

def getTimeDiff(listElement):
    return time.time() - listElement.photo_object.photo_time

####################################################################################

def personsFromBehindGiven(current_photo, savedContentList):
    if(len(current_photo.emotions) != 1):
        return False

    if( current_photo.emotions[0] != "Happy"):
        return False

    ToBigPersons =  list(filter(lambda x: getToBigPerson(x), current_photo.person_boxes))
    if(len(ToBigPersons) > 0):
        return False

    if len(current_photo.person_boxes) >= 4:
        if(helper.isFocusOnRelevantPart(current_photo.person_boxes, 0.25)):
            if(helper.isNotSavedInGivenTime(savedContentList, "persons_from_behind")):
                return True

###################################################################################
def getToBigPerson(person):
    personHeight = person[3] - person[1]
    if(personHeight > config.frame_height*0.55):
        return True
    else:
        return False

def getToBreitPersonForDozent(person):
    personWith = person[2] - person[0]
    if(personWith > config.frame_width*0.3):
        return True
    else:
        return False

def getToBigPersonForDozent(person):
    personHeight = person[3] - person[1]
    if(personHeight > config.frame_height*0.80):
        return True
    else:
        return False

def getToBigFacesForDozent(face):
    faceHeight = face[3] - face[1]
    if(faceHeight > config.frame_height*0.35):
        return True
    else:
        return False

def getValidPerson(person):
    personHeight = person[3] - person[1]
    if(personHeight <= config.frame_height*0.55):
        return True
    else:
        return False

####################################################################################
def personsFromFrontGiven(current_photo, savedContentList):
    ToBigPersons =  list(filter(lambda x: getToBigPerson(x), current_photo.person_boxes))
    if(len(ToBigPersons) > 0):
        return False

    if len(current_photo.person_boxes) < 4 or len(current_photo.emotions) < 4:
        return False

    correctEmotions = list(filter(lambda x: getListOfCorrectEmotions(x), current_photo.emotions))
    wrongEmotions = list(filter(lambda x: getListOfWrongEmotions(x), current_photo.emotions))  
    if len(correctEmotions) > len(wrongEmotions):        
        if(helper.isFocusOnRelevantPart(current_photo.person_boxes, 0.55)):
            if(helper.isNotSavedInGivenTime(savedContentList, "persons_from_front")):   
                #print('a lot faces from font. --> Valid')
                return True


def getBiggestPerson(current_photo):
    validPersons =  list(filter(lambda x: getValidPerson(x), current_photo.person_boxes))

    newlist = sorted(validPersons, key=lambda person: person[3]-person[1], reverse=True)
    #print(newlist)
    if(len(newlist)!=0):
        return newlist[0]
    return []

def findEmotion(person_box, current_photo):
    face_box = current_photo.face_boxes
    for i in range(len(face_box)):
        #print('person_x1=%s < face_x1=%s  person_y1=%s < face_y1=%s  person_x2=%s > face_x2=%s  person_y2=%s > face_y2=%s' 
        #    % (person_box[0], face_box[i][0], person_box[1], face_box[i][1], person_box[2], face_box[i][2], person_box[3], face_box[i][3]))
        if(person_box[0] < face_box[i][0] and person_box[1] < face_box[i][1] and person_box[2] > face_box[i][2] and person_box[3] > face_box[i][3]):
            return current_photo.emotions[i]
    return "no_emotion"

def getListOfCorrectEmotions(emotion):
    if(emotion=='Happy' or emotion=='Neutral'):
        return True
    else:
        return False

def getListOfWrongEmotions(emotion):
    if(emotion=='Angry' or emotion=='Disgust' or emotion=='Fear' or emotion=='Sad'):
        return True
    else:
        return False

####################################################################################
def nonLectureObjectGiven(current_photo, savedContentList):
    relevantContents = list(filter(lambda x: (x not in config.lectureKeyWords), current_photo.env_labels))

    if(len(relevantContents) > 0):
        keyWord = "non_lecture_relevant_object_" + relevantContents[0]
        myContentList = list(filter(lambda x: x.content_identifier == keyWord, savedContentList))
        if(len(myContentList) == 0):
            return True, keyWord

    return False, "no_identifer"
    
####################################################################################
def relevantTextGiven(current_photo, savedContentList):
    if(len(current_photo.words) > 30 and len(current_photo.person_boxes) < 3  and len(current_photo.emotions) < 3):
        if(helper.isNotSavedInGivenTime(savedContentList, "relevant_text")):
            print("words > 30 --> valid")
            return True