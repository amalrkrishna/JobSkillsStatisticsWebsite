import pandas as pd

def scrubScrapedData(df):
    df = df[df['4'].str[26:29] == "jk="] #remove sponsored posts
    df['id'] = df['4'].str[29:45] #create unique id from url
    #df = df.sort_values(by=['id'])
    df.drop_duplicates('id', keep='first', inplace=True)
    return df