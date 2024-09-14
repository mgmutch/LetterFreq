import glob
import docx
import re
import pandas as pd

#
# to run this script, you need to install pandas and python-docx on your computer.
#
# put your *.docx file in the same folder

def wc(filename):
    text = ""
    doc = docx.Document(filename)
    for paragraph in doc.paragraphs:
        text += paragraph.text + " "
    tmpdf = pd.DataFrame({'word': re.sub(r'[^a-z]', ' ', text.lower()).split()})
    result = pd.DataFrame()
    for word in tmpdf['word'].unique():
        count = len(tmpdf[tmpdf['word']==word])
        result = result.append({'word': word, 'count': count}, ignore_index=True)
        print(len(tmpdf['word'].unique()) - len(result))
    result.sort_values('count', ascending=False).to_csv(filename + '_wc.csv')

def days_number():
    counter = 63
    df = pd.DataFrame()
    for d in pd.date_range('2018/12/05', '2021/06/11'):
        df = df.append({'date': d, 'number': counter}, ignore_index=True)
        print(d, counter)
        counter += 1
        if counter > 90:
            counter = 1
    df.to_csv('./date.csv')

def main(run_word_count, run_days_number):
    if run_word_count:
        for filename in glob.glob('./*.docx'):
            wc(filename)
    if run_days_number:
        days_number()

if __name__ == '__main__':
    run_word_count = True # change to False if you do not want to run word count
    run_days_number = True
    main(run_word_count, run_days_number)

