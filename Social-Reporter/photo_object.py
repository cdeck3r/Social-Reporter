import config

class PhotoObject:
    def __init__(self, emotions, face_boxes, person_boxes, env_boxes, person_labels, env_labels, words, photo_time):
        self.emotions = emotions
        self.face_boxes = face_boxes
        self.person_boxes = person_boxes
        self.main_person = get_person_from_center(person_boxes)
        self.env_boxes = env_boxes
        self.person_labels = person_labels
        self.env_labels = env_labels
        self.words = words
        self.photo_time = photo_time

def get_person_from_center(person_boxes):
# x_1 = person_box[0]  y_1 = person_box[1]  x_2 = person_box[2]  y_2 = person_box[3]
    if len(person_boxes) > 0:
        for pbox in person_boxes:
            p_center_Xcoord = pbox[0] + pbox[2] - pbox[0]
            diff_to_center =  abs(p_center_Xcoord - config.frame_width / 2)
            if(diff_to_center < config.frame_width/4):
                return pbox
    else:
        return []

class ContentToSave:
    def __init__(self, content_identifier, photo_object):
        self.content_identifier = content_identifier
        self.photo_object = photo_object