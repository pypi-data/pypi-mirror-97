import pandas 

class schemas:

    def __init__(self, bucket='ephod-tech.trading-advisor.auto-trade.tw.data'):

        try:
            self.bucket = bucket
            self.s3_keys = {
                'index': 'index_schema.csv',
                'stock': 'stock_schema.csv',
                'warrant': 'warrant_schema.csv'
            }

            self.data = None
            for key, value in self.s3_keys.items():
    
                df = pandas.read_csv(f's3://{bucket}/schemas/{value}')
                df['attribute'] = key
                df['display'] = df['display'].apply(lambda x: x.strip())
                df['filename'] = df['filename'].apply(lambda x: x.strip())
                df.set_index('name')

                if self.data is None:
                    self.data = df.copy()
                else:
                    self.data = self.data.append(df.copy())                    
                    
        except Exception as ex:
            print('schema obj initiation failed', ex)

    def filenames(self, fields, attr, exclude=[], include=[]):

        result = self.data.loc[(self.data['display'].isin(fields))&(self.data['attribute']==attr)]['filename'].tolist()
        result = list(dict.fromkeys(result))
        
        for e in exclude:
            if e in result:
                result.remove(e)
        
        for i in include:
            if i not in result:
                result.append(i)

        return result

    def rename(self, df, attr):

        mapper = {}
        found_list = self.data.loc[(self.data['name'].isin(df.columns)) & (self.data['attribute']==attr)][['name', 'display']].to_numpy()
        
        for arr in found_list:
            mapper[arr[0]] = arr[1]
        
        return df.rename(columns=mapper)

    def columns(self, attr):
        return self.data[self.data['attribute']==attr]['display'].tolist()

    def descriptions(self, attr):
        return self.data[self.data['attribute']==attr][['name','display','description']]