import pandas as pd

class DataManager:
    
    def __init__(self, file_path):
        self._data = pd.read_csv(file_path)
        self._back_up = self._data.copy()
      
    def load_dataframe(self, df):
        self._data = df

    def getColumns(self,columns):
        try:
            if (c in self._data.columns for c in columns):
                self._data = self._data[columns]

        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
            return

    def getRowSum(self,columns = []):
        try:
            if len(columns) > 0:
                self._data['Total'] = self._data[columns].sum(axis=1)
            else:
                self._data['Total'] = self._data.sum(axis=1)

        except KeyError:
            print(f'Column \'{column[0]}\' does not exsist')
            return

    def getColumnSum(self, column):
        try:
            if column:
                return self._data[column[0]].sum()

        except KeyError:
            print(f'Column \'{column[0]}\' does not exsist')
            return

    def getColumnPercentage(self, column):
        try:
            self.getRowSum(column)
            total = self.getColumnSum(column)
            self._data['Total'] = self._data['Total'].apply(pd.to_numeric)
            self._data['percentage'] = self._data['Total'] * (100 / total)
            return self._data[[column,'percentage']]
        except KeyError:
            print(f'Column \'{column[0]}\' does not exsist')
            return


    def group_sales_by(self, column_name):
        try:
            self._data = self._data.groupby(column_name, as_index=False).sum()
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
            return
        
        for c in self._data.columns:
            if '_Sales' in c or c in column_name:
                pass
            else:
                del self._data[c]
                
    
    def filter_by_list(self, column_name, filter_list):
        try:
            self._data = self._data.loc[self._data[column_name].isin(filter_list), :]
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
        
    
    def filter_by_range(self, column = 'Year', params = {'min_val' : None, 'max_val' : None, 'include_max':True, 'include_min' : True}):
        try:
            if column == 'Year' or '_Sales' in column:
                params['min_val'] = int(params['min_val'])
                params['max_val'] = int(params['max_val'])

            if params['include_max']:
                self._data = self._data.loc[
                             (self._data[column] >= params['min_val']) & (self._data[column] <= params['max_val'])]
            else:
                self._data = self._data.loc[
                             (self._data[column] >= params['min_val']) & (self._data[column] < params['max_val'])]
        except KeyError:
            print(f'Column \'{column}\' does not exsist')
            
    
    def sort(self, column_name, ascending=True):
        try:
            self._data = self._data.sort_values(by=column_name, ascending=ascending)
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
    
    
    def reset_data(self):
        self._data = self._back_up
        
    
    def get_data(self):
        return self._data
    
    
    @property
    def data(self):
        return self._data
    
    
    @property
    def column_names(self):
        return list(self._data.columns)