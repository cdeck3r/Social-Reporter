import time
import cv2
import cvlib
import validator
import photo_object as po
import config
import image_to_text_converter as txtConv
import helper
import os


def isValidContent(current_photo, savedContentList):
    if(validator.relevantLecturerGiven(current_photo, savedContentList)):
        return "lecturer"
    if(validator.personsFromBehindGiven(current_photo, savedContentList)):
        return "persons_from_behind"
    if(validator.personsFromFrontGiven(current_photo, savedContentList)):
        return "persons_from_front"
    validation1, use_case1 = validator.nonLectureObjectGiven(current_photo, savedContentList)
    if(validation1):
        return use_case1
    if(validator.relevantTextGiven(current_photo, savedContentList)):
        return "text_available"
    else:
        return "no_identifer"

def main():
    config.init()
    iteration = 0
    savedContentList = []

    for framename in os.listdir(config.input_dir):
        print("iteration: " + str(iteration))

        frame = cv2.imread(config.input_dir + "/" + framename)
        if frame is None:
            print("{} skipped".format(framename))
            continue
            
        #collect infos
        frame, emotions, face_boxes = config.emotion_model.recognise_emotion(frame)
        person_boxes, env_boxes, person_labels, env_labels, confs = cvlib.detect_common_objects(frame, confidence=.75)
        frame = cvlib.object_detection.draw_person_bbox(frame, person_boxes, person_labels, confs, write_conf=False)
        frame = cvlib.object_detection.draw_env_bbox(frame, env_boxes, env_labels, confs, write_conf=False)
        words = txtConv.convert(frame)
        # create photoObject
        photo_object = po.PhotoObject(emotions, face_boxes, person_boxes, env_boxes, person_labels, env_labels, words, time.time())
        #check
        content_identifier = isValidContent(photo_object, savedContentList)

        if(content_identifier != "no_identifer"):
            cv2.imwrite(config.output_dir + '%s_%s.jpeg' % (iteration, content_identifier), frame)
            row_content = [framename[4:5],iteration,content_identifier,time.strftime('%H:%M:%S', helper.getLocalTime(photo_object.photo_time))]
            helper.save_to_csv('output/contents.csv', row_content)
            savedContentList.append(po.ContentToSave(content_identifier, photo_object))
            print("relevant picture saved.")
        
        iteration+=1


if __name__ == '__main__':
    main()