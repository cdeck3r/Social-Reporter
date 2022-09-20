import time
import config
from csv import writer

def isFocusOnRelevantPart(relevant_boxes, frame_height_factor):
    #print("relevant_boxes")
    #print(relevant_boxes)
    myContentList = list(filter(lambda x: getRelevantObject(x, frame_height_factor), relevant_boxes))
    soll_value = round(len(relevant_boxes) * 0.5)
    #print('len(relevant_boxes)=%s' % (len(relevant_boxes)))
    #print('len(myContentList)=%s > soll_value=%s' % (len(myContentList), soll_value))
    if(len(myContentList) > soll_value):
        return True

def getRelevantObject(rbox, frame_height_factor):
    #print("rbox")
    #print(rbox)
    r_center_Xcoord = rbox[2] - rbox[0]
    x_diff_to_center =  abs(r_center_Xcoord - config.frame_width / 2)

    r_center_Ycoord = rbox[3] - rbox[1]
    y_diff_to_ceter = abs(r_center_Ycoord - config.frame_height / 2)
    #print('x_diff_to_center=%s < config.frame_width*0.5=%s' % (x_diff_to_center, config.frame_width * 0.5))
    #print('y_diff_to_ceter=%s < config.frame_height*%s=%s' % (y_diff_to_ceter, frame_height_factor, config.frame_height * frame_height_factor))
    if(x_diff_to_center <  config.frame_width * 0.5 and y_diff_to_ceter < config.frame_height * frame_height_factor):
        return True


def isNotSavedInGivenTime(savedContentList, content_identifier):
    myContentList = list(filter(lambda x: x.content_identifier == content_identifier, savedContentList))
    if not myContentList:
        #print("frist " + content_identifier + "--> valid")
        return True
    
    oldestValue = myContentList[-1]
    #print("current time: " + str(time.time()))
    #print("oldest photo: "+ str(oldestValue.photo_object.photo_time))
    diff_time = time.time() - oldestValue.photo_object.photo_time
    #print("dif: "+ str(diff_time))
    if(diff_time > config.time_to_leave_in_sec):
        #print("after long time: " + content_identifier + "--> valid")
        return True

def save_to_csv(file_name, list_of_elem):
    # camnr,sequenznr,usecase,timestamp
    with open(file_name, 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def getLocalTime(t):
    return time.localtime(t)

### not used for now
def resolutionChanged(current_photo, savedContentList):
    if len(savedContentList) > 0:
        height_current_person = current_photo.main_person[2] - current_photo.main_person[0]
        weight_current_person = current_photo.main_person[3] - current_photo.main_person[1]
        last_photo_object =  savedContentList[-1].photo_object
        height_last_saved_person = last_photo_object.main_person[2] - last_photo_object.main_person[0]
        weight_last_saved_person =  last_photo_object.main_person[3] - last_photo_object.main_person[1]
        height_diff = abs(height_current_person - height_last_saved_person)
        weight_diff = abs(weight_current_person - weight_last_saved_person)

        if(height_diff > height_last_saved_person * 0.3 and weight_diff > weight_last_saved_person * 0.2):
            #print("Resolution change --> valid")
            return True
