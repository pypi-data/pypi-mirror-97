from dataTransform import analyze_data
from processdata import load_data
import os
import pandas as pd


def NewsAnalyzer (workType, api,token,name,path,count):

    if workType == 'sample':

        df = pd.read_csv('1700pages.csv')
        df = df[1000:1100]
        df.to_csv('sample.csv',index = False)
        analyze_data('sample.csv', 'data/companies.csv',api,token)
        os.remove('sample.csv')

    if workType == 'full':

        completed, failed = load_data('FullRaw', 2100)
        analyze_data('FullRaw.csv', 'data/companies.csv',api, token)
        os.remove('FullRaw.csv')
    
    if workType == 'demo':

        completed, failed = load_data('RawDemo', 10)
        df = pd.read_csv('1700pages.csv')
        df = df[1000:1100]
        df.to_csv('sample.csv',index = False)
        analyze_data('sample.csv', 'data/companies.csv',api,token)
        os.remove('sample.csv')
        os.remove('RowDemo.csv')
    
    if workType == 'existing':

        analyze_data('1700pages.csv', 'data/companies.csv',api,token)
    
    if workType == 'scrape':

        name = str(input('Filename for scraped data(without format extension): '))
        completed,failed = load_data(name,count)

    if workType == 'analyze':

        analyze_data(f'{name}.csv', 'data/companies.csv',api,token)

    if workType == 'custom':

        name = str(input('Filename for scraped data(without format extension): '))
        completed,failed = load_data(name,count)
        analyze_data(f'{name}.csv', 'data/companies.csv',api,token)


