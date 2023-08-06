import pandas, datetime, json, boto3, os, pytz
import shioaji as sj
import eWarrant
import eQmaster.schema

class eQueries:

    def __init__(self, settings={}):

        s3 = boto3.client('s3')

        if not isinstance(settings, dict):
            print('Error: settings data type mismatch.')
            return None
        
        if 'key' in settings and 'credential' in settings:
            ew = eWarrant.eWarrant(key=settings['key'], credential=settings['credential'])
            self.username = ew.username()
            self.password = ew.password()
        else: 
            print('Missing key and credential. Key and credential are needed for retrieving real-time stock data.')    
        
        if 'stock_data_src' not in settings:
            self.stock_data_src = 's3://ephod-tech.trading-advisor.auto-trade.tw.data/stock/stock={symbol}/{filename}'
        else: 
            self.stock_data_src = settings['stock_data_src']
        
        if 'index_data_src' not in settings:
            self.index_data_src = 's3://ephod-tech.trading-advisor.auto-trade.tw.data/index/index_id={symbol}/{filename}'
        else:
            self.index_data_src = settings['index_data_src']

        if 'config_path' not in settings:
            self.config_path = 's3://ephod-tech.trading-advisor.auto-trade.configuration/query-master/market.json'        
        else: 
            self.config_path = settings['config_path']

        if self.config_path.startswith('s3://'):
            local_file = 'market.json'
            bucket = self.config_path.replace('s3://','').split('/')[0]
            path = self.config_path.replace('s3://','').split('/')[1]
            filename = self.config_path.replace('s3://','').split('/')[2]
            s3.download_file(bucket, f'{path}/{filename}', 'market.json')
            f = open(local_file)
            self.market_config = json.load(f)
            os.remove(local_file)
        else:
            f = open(self.config_path)
            self.market_config = json.load(f)

        self.schema = eQmaster.schema.schemas()
    
    def convert_symbol(self, _list):
            
        result = []
        for s in _list:
            if s.endswith('.tw'):
                result.append(s.replace('.tw', '')) 
            else: 
                result.append(s)        
        return result

    def is_market_open(self):

        if self.market_config is not None:
            timezone = self.market_config['timezone']
            curr_date = datetime.datetime.now().replace(tzinfo=pytz.timezone(timezone))
            curr_date_str = curr_date.strftime('%Y-%m-%d')
            weekday = curr_date.weekday()
            curr_time_stamp = curr_date.timestamp()
            start_timestamp = datetime.datetime.strptime(f'{curr_date_str} 09:00:00','%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(timezone)).timestamp()
            end_timestamp = datetime.datetime.strptime(f'{curr_date_str} 13:30:00','%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone(timezone)).timestamp()
            if ( weekday < 5 and 
                curr_date_str not in j['market_close_dates'] and 
                curr_time_stamp >= start_timestamp and curr_time_stamp <= end_timestamp ):
                return True
        
        return False

    def get_current_quote(self, _list):

        stock_symbol_list = self.convert_symbol(_list)
        api = sj.Shioaji()
        api.login(
            person_id=self.username,
            passwd=self.password, 
            contracts_cb=lambda security_type: print(f'{repr(security_type)} fetch done.')
        )
        stock_symbol = stock_symbol_list[0]
        contracts = [api.Contracts.Stocks[stock_symbol]]
        snapshots = api.snapshots(contracts)
        return pandas.DataFrame(snapshots)

    def get(self, search_list, columns, attr):

        new_stock_list = self.convert_symbol(search_list)
        file_list = self.schema.filenames(fields=columns, exclude=['stock_price.parquet.gzip'], attr=attr)

        # temporary solution, should change before index.parquet.gzip is updated
        if attr == 'index':
            file_list = self.schema.filenames(fields=columns, exclude=['index.parquet.gzip'], attr=attr)

        master_parquet_df = None
        for s in new_stock_list:
            s3_filename = self.stock_data_src.replace('{symbol}', s).replace('{filename}', 'stock_price.parquet.gzip')
            if attr == 'index':
                s3_filename = self.index_data_src.replace('{symbol}', s).replace('{filename}', 'index.parquet.gzip')

            parquet_df = pandas.read_parquet(s3_filename)

            if 'coid' not in parquet_df.columns:
                parquet_df['coid'] = parquet_df['idx_id']

            if parquet_df['coid'].count() > 0:                
                parquet_df['mdate'] = parquet_df['mdate'].apply(lambda x: x[:10])
                for _file in file_list:
                    s3_filename = self.stock_data_src.replace('{symbol}', s).replace('{filename}', _file)

                    if attr == 'index':
                        s3_filename = self.index_data_src.replace('{symbol}', s).replace('{filename}', _file)

                    _file_df = pandas.read_parquet(s3_filename)
                    if 'mdate' in _file_df.columns:
                        _file_df['mdate'] = _file_df['mdate'].apply(lambda x: x[:10])
                    
                    if 'observed_date' in _file_df.columns:
                        _file_df['mdate'] = _file_df['observed_date'].apply(lambda x: x[:10])
                    
                    parquet_df = parquet_df.merge(right=_file_df, how='left', on=['coid','mdate'])

            if master_parquet_df is None:
                master_parquet_df = parquet_df
            else:
                master_parquet_df.append(parquet_df)
        
        master_parquet_df = self.schema.rename(master_parquet_df, attr='stock')

        # if requested columns are not available, requested columns are not returned
        qualified_columns = [x for x in columns if x in master_parquet_df.columns]
        return master_parquet_df[qualified_columns]
    
    def columns(self, attr):
        return self.schema.columns(attr)

    def desc(self, attr):
        return self.schema[self]