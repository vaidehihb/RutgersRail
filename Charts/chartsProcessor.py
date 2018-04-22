from data_manager import DataManager

class chartsProcessor(object):
    def __init__(self, filters = [], groupbycolumns = [], columnstoretain = []):
        self._filters = filters
        self._groupByColumns = groupbycolumns
        self._columnsToRetain = columnstoretain
        self._dm = DataManager('Charts/vgsales.csv')

    def filterData(self):
        try:
            if self._filters and len(self._filters) > 0:
                for filter in self._filters:
                    if filter['column'] in self._dm._data.columns and filter['type'] == 'range':
                        self._dm.filter_by_range(column = filter['column'], params = filter['params'])
                    elif filter['column'] in self._dm._data.columns and filter['type'] == 'list':
                        self._dm.filter_by_list(column_name = filter['column'], filter_list = list(filter['params']))
        except KeyError:
            print(f'Year filter does not exist')


    def groupData(self):
        try:
            if self._groupByColumns and len(self._groupByColumns) > 0:
                self._dm.group_sales_by(self._groupByColumns)
        except KeyError:
            print(f'Year filter does not exist')

    def selectColumns(self):
        try:
            if self._columnsToRetain and len(self._columnsToRetain) > 0:
                self._dm.getColumns(self._columnsToRetain)
        except KeyError:
            print(f'Year filter does not exist')

    def getAggregates(self, column):
        try:
            return self._dm.getColumnPercentage(column)
        except KeyError:
            print(f'Year filter does not exist')

    def getRegions(self):
        try:
            regions = []
            for c in self._dm._data.columns:
                if '_Sales' in c:
                    regions.append(c[:c.index('_Sales')])
                else:
                    continue

            return regions
        except KeyError:
            print(f'Year filter does not exist')

    def getMinMaxYear(self):
        try:
            years = list(self._dm._data['Year'].values)
            return min(years), max(years)
        except KeyError:
            print(f'Year filter does not exist')

    def getUniqueValues(self,column):
        try:
            return list(self._dm._data[column].unique())
        except KeyError:
            print(f'Year filter does not exist')





