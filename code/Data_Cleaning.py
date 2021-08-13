##################################################################################################################
#Data_Cleaning.py includes following steps and functions:
#            - Language Identification:
#                               for detecting languages;
#                               for filtering only english posts;
#                               for fixing bad-encoding text
#            - SpaCy NLP Pipeline:
#                               spacy.tokenizer for tokenization;
#                               (udf)emoji_remover for removing Emojis;
#                               spacy.tagger for tagging part-of-speech;
#                               spacy.parser for assigning dependency labels;
#                               spacy.ner for assigning name entity;
#                               (udf)noun_selector for selecting only NOUN, PROPN and filtering non-stopwords
##################################################################################################################
#Import modules###################################################################################################
import pandas as pd
import numpy as np
import string
import re
import os
import glob
import ftfy
import ftfy.bad_codecs
import emoji
import langid
from langid.langid import LanguageIdentifier, model
import spacy
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA, TAG
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
##################################################################################################################
#UDF##############################################################################################################
#Bulk-reading .csv files from specified path, concatenate and split into spam/nonspam dataframes
def loaddata (path) :
    d = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            d[file[:-4]] = pd.read_csv(path+'/'+file, encoding = 'utf-8')
            df = pd.concat(d, axis = 0)
            df.index = df.index.droplevel(0)
    df_nonspam = df[df.modr_status == 2]
    df_spam = df[df.modr_status == 3]
    return df_nonspam, df_spam

#Detect Languages and add column 'lang' and 'confidence' to dataframe
def langdetect(dataframe, text_column):
    result_list = []
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    for i in range(0,len(dataframe[text_column].values)):
        dataframe[text_column].values[i] = dataframe[text_column].values[i].encode('sloppy-windows-1252').decode('utf-8')
        text = dataframe[text_column].values[i]
        result_list.append(identifier.classify(text.lower()))
    lan_list = np.array([w for w,c in result_list]).reshape((len(result_list),1))
    conf_list = np.array([c for w,c in result_list]).reshape((len(result_list),1))
    dataframe['lang'] = lan_list
    dataframe['confidence'] = conf_list
    return dataframe

#Remove Emojis from text body of post
def emoji_remover(doc):
    def keep_token(token):
        if not any(j in token.text for j in emoji.UNICODE_EMOJI):
            return token
    emoji_removed = list(filter(keep_token,doc))
    result = ' '.join(token.string for token in emoji_removed)
    return tokenizer(result)

#Select only nouns (NOUN, PROPN), containing only alphabetic characters, and are not in stop words
def noun_selector(doc):
    def keep_token(token):
        if (token.pos_ in ('NOUN', 'PROPN')) & (token.is_alpha) & (token.is_stop == False):
            return token
    removed_result = list(filter(keep_token,doc))
    result = ''.join(token.string for token in removed_result)
    return tokenizer(result)
##################################################################################################################
##################################################################################################################
#Bulk-load and split data into spam/nonspam dataframes
df_nonspam, df_spam = loaddata("./new_posts")

#Detect languages
test_df = langdetect(df_nonspam, "body") #135836 non-spam

#Select posts written in EN
all_en = test_df[test_df.lang == "en"]
text_body = all_en.body.values.tolist()

#Load SpaCy pipeline
nlp = spacy.load('en')
#Add customized components to SpaCy pipeline
nlp.add_pipe(emoji_remover, name='emoji_remover', first=True)
nlp.add_pipe(noun_selector, name='noun_selector', first= False)
tokenizer = English().Defaults.create_tokenizer(nlp)
print(nlp.pipe_names)

#Clean text body through pipeline
cleaned_text = list(map(lambda x : nlp(u"{}".format(x.lower())), text_body))
cleaned_text_array = np.array(cleaned_text).reshape((len(cleaned_text),1))
all_en['cleaned_text'] = cleaned_text_array

#Save output to .csv file in the current working directory
all_en.to_csv("cleaning_np_output.csv", index= False)
