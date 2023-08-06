from .dataTransform import analyze_data
from .processdata import load_data
import os
import pandas as pd



def NewsAnalyzer (workType, api,token,name,path,count):

    if workType == 'sample':
        print('Entered {} mode'.format(workType))
        df = pd.read_csv('1700pages.csv')
        df = df[1000:1100]
        df.to_csv('sample.csv',index = False)
        analyze_data('sample.csv', 'companies.csv',api,token)
        os.remove('sample.csv')
        return

    if workType == 'full':
        print('Entered {} mode'.format(workType))
        completed, failed = load_data('FullRaw', 2100)
        analyze_data('FullRaw.csv', 'companies.csv',api, token)
        os.remove('FullRaw.csv')
        return
    
    if workType == 'demo':
        print('Entered {} mode'.format(workType))

        completed, failed = load_data('RawDemo', 10)
        df = pd.read_csv('1700pages.csv')
        df = df[1000:1100]
        df.to_csv('sample.csv',index = False)
        analyze_data('sample.csv', 'companies.csv',api,token)
        os.remove('sample.csv')
        os.remove('RawDemo.csv')
        return
    
    if workType == 'existing':
        print('Entered {} mode'.format(workType))

        print(" Download already analyzed data at 'https://github.com/mykhailoivaniuk/reutersanalyzer' ")
        return 
    
    if workType == 'scrape':
        print('Entered {} mode'.format(workType))

        name = str(input('Filename for scraped data(without format extension): '))
        completed,failed = load_data(name,count)
        return

    if workType == 'analyze':
        print('Entered {} mode'.format(workType))
        path = '{}.csv'.format(name)

        analyze_data(path, 'companies.csv',api,token)
        return

    if workType == 'custom':
        print('Entered {} mode'.format(workType))

        name = str(input('Filename for scraped data(without format extension): '))
        completed,failed = load_data(name,count)
        path = '{}.csv'.format(name)
        analyze_data(path, 'companies.csv',api,token)
        return

