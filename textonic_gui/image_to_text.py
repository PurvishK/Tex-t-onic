from image_helper_functions import *
from preprocess_methods import *
import cv2
import pytesseract
from PIL import Image
from gtts import gTTS
import sys
import nltk
import datetime
global final_file_name 
import time

def preprocessing_pipeline(image,save_path):

    image=shadow(image)
    save_image(image,'_first.png',save_path+"images\\")

    image=denoise(image)
    save_image(image,'_first2.png',save_path+"images\\")

    image = blur_correction(image)

    save_image(image,'_final1.png',save_path+"images\\")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def get_string(img_path):
    result = pytesseract.image_to_string(Image.open(img_path))
    return result

def clean_text(text):
    words = set(nltk.corpus.words.words())
    words = list(words) + ['chaitanya','bharathi','soumya','vemuri','murali','krishna']
    return " ".join(w for w in nltk.wordpunct_tokenize(text) if w.lower() in words or not w.isalpha())

def text_to_speech(text,save_path):
    language = 'en'
    myobj = gTTS(text,lang=language)
    file_name = save_path+final_file_name+"_audio_file.mp3"
    # print(file_name)
    myobj.save(file_name)

def save_text(text,save_path):
    if "leaveapplication" in save_path:
        pass
    text = "".join(text)     
    file_name = save_path+final_file_name+"_data_file.txt"
    # print(file_name)
    text_file = open(file_name,'w',encoding="utf-8")
    text_file.write(text)
    text_file.close()

def main(image_path, save_path):
    start = time.process_time()
    image = load_image(image_path) 
    preprocessing_pipeline(image,save_path)
    preprocess_time = time.process_time()
    print("---Preprocessing took ",str(preprocess_time-start)," seconds---")

    text = get_string(save_path+'images\_final1.png')
    save_text(text,save_path)
    ocr_time = time.process_time()
    print("---Text Extraction took ",str(ocr_time-preprocess_time)," seconds---")

    text = clean_text(text)
    info_extract = time.process_time()
    print("---Information Extraction took ",str(info_extract-ocr_time)," seconds---")

    text_to_speech(text,save_path)
    speech_extract = time.process_time()
    print("---Text to Speech Conversion took ",str(speech_extract-info_extract)," seconds---")


    print("---Entire Process took ",str(info_extract - start)," seconds---")

    print(final_file_name)
    return final_file_name

if __name__=="__main__":
    image_path = sys.argv[1]
    img_name = image_path.split('/')[-1]
    img_name = img_name.split('.')[0]
    final_file_name = str(datetime.date.today())+"_"+img_name
    main(sys.argv[1],sys.argv[2])