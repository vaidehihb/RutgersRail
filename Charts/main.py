from flask import Flask, request, render_template, Response, jsonify
from chartsProcessor import chartsProcessor
import json
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'papillon16591'

@app.route("/")
def main():
    c = chartsProcessor()
    regions = c.getRegions()
    yearmin,yearmax = c.getMinMaxYear()
    genres = c.getUniqueValues('Genre')
    platforms = c.getUniqueValues('Platform')
    publishers = c.getUniqueValues('Publishers')
    return render_template('charts.html', regions=regions, yearmin = yearmin, yearmax = yearmax, genres = genres, plaforms = platforms, publishers = publishers)


@app.route("/linechart", methods=['GET', 'POST'])
def getLineCharts():
    if request.method == 'POST':
        if request.get_json():
            data = request.get_json()
            if data:
                c = chartsProcessor()
                if data['filters']:
                    c._filters = data['filters']
                    c.filterData()
                if data['groupbycolumns']:
                    c._groupByColumns = list(data['groupbycolumns'])
                    c.groupData()
                if data['columnsToRetain']:
                    c._columnsToRetain = list(data['columnsToRetain'])
                    c.selectColumns()

                df = c._dm._data
                columns = df.columns
                data = {}

                for co in columns:
                    data[co] = list(df[co].values)
                return jsonify(data)


@app.route("/piechart", methods=['GET', 'POST'])
def getPieCharts():
    if request.method == 'POST':
        if request.get_json():
            data = request.get_json()
            if data:
                c = chartsProcessor()
                if data['filters']:
                    c._filters = data['filters']
                    c.filterData()
                if data['groupbycolumns']:
                    c._groupByColumns = list(data['groupbycolumns'])
                    c.groupData()
                if data['columnsToRetain']:
                    c._columnsToRetain = list(data['columnsToRetain'])
                    c.selectColumns()
                if data['aggregate']:
                    c._dm.getRowSum()
                    data = {}
                    total = c._dm.getColumnSum(['Total'])
                    for co in c._dm._data.columns:
                        all = list(c._dm._data[co].values)
                        if co == 'Total':
                            data[co] = [float(v)*(100/total) for v in list(c._dm._data[co].values)]
                        else:
                            data[co] = list(c._dm._data[co].values)

                    data['sum'] = total
                    return jsonify(data)





if __name__ == "__main__":
    app.run()
