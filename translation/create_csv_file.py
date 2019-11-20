import re

""" script pour créer les csv finaux """

def display_file(file,n):
    """Affiche les n 1ere ligne du fichiers """
    i=0
    with open(file,'r',encoding="utf8") as f:
        for line in f:
            if(i==n):
                break
            i+=1
            print(line)



def clean_text_file(input_name,output_name):
    input = open(input_name,"r",encoding='utf8')
    output = open(output_name,'w',encoding='utf8')

    for line in input:
        line = re.sub(r'__en__', '', line)
        line = re.sub(r'&quot;', '\'', line)
        line = re.sub(r'&#91;', '[', line)
        line = re.sub(r'&#93;', ']', line)
        line = re.sub(r';','',line)
        output.write("%s" % (line))


def create_dict_from_textfile(input_fr,input_en):
    """Cree un dict de la forme {"fr":[str,str...],"en":[str,str,...]}
        input : un fichier text """

    file_fr = open(input_fr,"r",encoding="utf8")
    file_en = open(input_en,"r",encoding="utf8")
    dataset_dict = {"fr":[],"en":[]}
    for line in file_fr:
        dataset_dict["fr"].append(line.rstrip('\n\r'))
    for line in file_en:
        dataset_dict["en"].append(line.rstrip('\n\r'))

    return dataset_dict


def create_csv_file_from_dict(dict,output):

    """ A partir du dict générer avant, créer un fichier csv avec comme séparateur le ';' """
    fout = open(output,'w',encoding='utf8')
    #fout.write("fr;en\n")
    fr = dict["fr"]
    en=dict["en"]
    for f,e in zip(fr,en):
        fout.write("%s;%s\n" % (f,e))


clean_text_file("data/fr_en/train.fr","data/fr_en/train_fr.txt")
clean_text_file("data/fr_en/train.en","data/fr_en/train_en.txt")
clean_text_file("data/fr_en/test.fr","data/fr_en/test_fr.txt")
clean_text_file("data/fr_en/test.en","data/fr_en/test_en.txt")
clean_text_file("data/fr_en/dev.fr","data/fr_en/dev_fr.txt")
clean_text_file("data/fr_en/dev.en","data/fr_en/dev_en.txt")
create_csv_file_from_dict(create_dict_from_textfile("data/fr_en/train_fr.txt","data/fr_en/train_en.txt"),"data/fr_en/train.csv")
create_csv_file_from_dict(create_dict_from_textfile("data/fr_en/test_fr.txt","data/fr_en/test_en.txt"),"data/fr_en/test.csv")
create_csv_file_from_dict(create_dict_from_textfile("data/fr_en/dev_fr.txt","data/fr_en/dev_en.txt"),"data/fr_en/dev.csv")
