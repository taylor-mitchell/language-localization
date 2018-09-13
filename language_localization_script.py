import os
import re
from pathlib import Path
from google.cloud import translate


credential_path = "C:\Creds\Translation-project-fa071178a5fd.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def read_file_into_dict(filename):
    file_dict = dict()
    with open(filename, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        index = 0
        for line in lines:
            try:
                m = re.search(r'\'[\w\W]*\'', line)
                
                data = m.group(0).replace("'", '').split(',')

                key = data[0] + data[1] + data[2]
                file_dict[key] = data[3]
                index += 1
            except:
                print("Error at line " + str(index) + " in read_file_into_dict")

    return file_dict    
                  

def translate_elements(filename = "en_csv.csv", filepath = '.\\', language = 'en'):
    """filepath goes to where the english text file is and where the resulting text file will be
        written to

        filename is the csv created by the english records in the localized text table

        language is the language code used by google"""
    
    output_str = ""

    file_exists = False

    my_file = Path(filepath + "\\" + language[:2] + "_text.txt")
    if my_file.is_file():
        file_exists = True
        file_dict = read_file_into_dict(filepath + "\\" + language[:2] + "_text.txt")
        
    with open(filepath + "\\" + filename, 'r') as f:
        lines = f.readlines()

        first_line = lines.pop(0)[:-1].replace('"', '').split(',')
        
        app_index = first_line.index('app')
        field_name_index = first_line.index('field_name')
        language_id_index = first_line.index('language_id')
        localized_text_index = first_line.index('localized_text')
        
        total = len(lines)
        
        translate_client = translate.Client()
        index = 0
        
        for line in lines:
            data = line.replace('"', '').split(',')
            
            for i in range(0, len(data)):
                data[i] = data[i].replace('"', '\'')
                
            key = data[field_name_index]+data[app_index]+language[:2]
            output_str+='insert into localized_text'
            output_str+=' values(\''
            output_str+=data[field_name_index]
            output_str+='\',\''
            output_str+=data[app_index]
            output_str+='\',\''
            output_str+=language[:2]
            output_str+='\',\''

            if file_exists and key in file_dict.keys():
                output_str+= file_dict[key]
            elif language == 'en':
                output_str+= data[localized_text_index]            
            else:
                print('Translation')
                translation = translate_client.translate(data[localized_text_index], source_language = 'en', target_language = language)
                output_str+=translation['translatedText'].replace("\n", "")
            output_str+='\');\n'
            index+=1
            print(str(index) + " out of " + str(total))
            

    with open(filepath + "\\" + language[:2] + "_text.txt", 'w', encoding = 'utf-8') as f:
        f.write(output_str)
        
    return output_str
    
def translate_all(fp = "c:\\devel\\Language Localization"):
    with open(fp + "\\localization_text.txt", 'w', encoding = 'utf-8') as f:
        print("English")
        output = translate_elements(filepath = fp, language = 'en');
        f.write(output)

        print("French")
        output = translate_elements(filepath = fp, language = 'fr');
        f.write(output)
        
        print("Spanish")
        output = translate_elements(filepath = fp, language = 'es');
        f.write(output)

        print("German")
        output = translate_elements(filepath = fp, language = 'de');
        f.write(output)
        
        print("Dutch")
        output = translate_elements(filepath = fp, language = 'nl');
        f.write(output)
        
        print("Arabic")
        output = translate_elements(filepath = fp, language = 'ar');
        f.write(output)
        
        print("Chinese")
        output = translate_elements(filepath = fp, language = 'zh-CN');
        f.write(output)

def main():
    languages = list()
    cred_path = ''
    with open('./specs.txt', 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines)):
            if lines[i] == 'Languages\n':
                languages = lines[i+1].split(',')
            if lines[i] == 'Credential Path\n':
                cred_path = lines[i+1]

    if cred_path is not '':
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
    
    for lan in languages:
        with open('./language_inserts/localization_text.txt', 'w', encoding = 'utf-8') as f:
            output = translate_elements(filepath = './language_inserts', language = lan)
            f.write(output)
            f.write('\n')





    
        
    

    

