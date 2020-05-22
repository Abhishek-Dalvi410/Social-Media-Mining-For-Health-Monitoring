from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask import request
import json
from flask_cors import CORS
# import requests
import csv
import operator
import pickle
from transformers import BertTokenizer
from transformers import BertForSequenceClassification,
# import pandas

app = Flask(__name__)
api = Api(app)
CORS(app)

tokenizer = BertTokenizer.from_pretrained('bio_bert', do_lower_case=False)
model = BertForSequenceClassification.from_pretrained(
    "bio_bert",
    num_labels = 2,          
    output_attentions = False, 
    output_hidden_states = False, 
)
class LiveTest(Resource):
    def post(self):
        input_json = request.get_json()
        print(input_json)
        # op = find_extraction(input_json('tweet'))
        op = {
            'class': 0,
            'adr': [{
                'mention': 'sleep problems',
                'meddra_term': 'sleep paralysis',
                'meddra_code': 10041002
            },
            {
                'mention': 'hungry',
                'meddra_term': 'feeling hungry',
                'meddra_code': 10016336
            }]
        }
        return op, 200
    def find_extraction(sentence,model = model){

    }

class GetData(Resource):
    def get(self):
        f = open('task3_training.tsv')
        m = open('task3_validation.tsv')
        t1 = open('task1_data_predictions.csv')
        t2 = open('task2_dataset_with_sintervals.csv')
        # print(csv_t1[0])
        next(f, None)
        next(m, None)
        next(t1, None)
        next(t2, None)
        csv_f = csv.reader(f, delimiter="\t")
        csv_m = csv.reader(m, delimiter="\t")
        csv_t1 = csv.reader(t1, delimiter=",")
        csv_t2 = csv.reader(t2, delimiter=",")
        modelData = []
        trainData = []
        t2Test = []
        drugDict = {}
        meddraDict = {}
        allDrugsDict = {}
        predMedDict = {}
        drugNames = set()
        t2Data = []
        t3Data = []
        t1Data = []
        t1_right_one = 0
        t1_right_zero = 0
        t1_wrong_one = 0
        t1_wrong_zero = 0
        for each in csv_t1:
            if int(each[2]) == 1 and int(each[4]) == 1:
                t1_right_one += 1
            elif int(each[2]) == 1 and int(each[4]) == 0:
                t1_wrong_one += 1
            elif int(each[2]) == 0 and int(each[4]) == 0:
                t1_right_zero += 1
            else:
                t1_wrong_zero += 1
            # if int(each[4]) == 1:
            #     t1_pred += 1
            t1Data.append({
                'tweet': each[3],
                'data_class': each[2],
                'pred_class': each[4]
            })
        t1_obj = {
            'True Positive': t1_right_one,
            'True Negative': t1_right_zero,
            'False Positive': t1_wrong_zero,
            'False Negative': t1_wrong_one
        }

        with open('final_task2_predictions_joint.pkl', 'rb') as f1:
            testing_data = pickle.load(f1)
        with open('final_task3_predictions.pkl', 'rb') as f2:
            task3_data = pickle.load(f2)
        df = testing_data
        for i in range(len(df)):
            # print(df.iloc[i])
            if str(df.iloc[i]['extraction'][0]) == "nan":
                # print("nan found")
                obj = {
                    'extraction': [],
                    'tweet': df.iloc[i]['tweet'][0],
                    'medra_code': [],
                    'intervals': [],
                    'predictions': df.iloc[i]['predictions']
                }
            else:
                obj = {
                    'extraction': df.iloc[i]['extraction'],
                    'tweet': df.iloc[i]['tweet'][0],
                    'medra_code': df.iloc[i]['meddra_code'],
                    'intervals': df.iloc[i]['new_intervals'],
                    'predictions': df.iloc[i]['predictions']
                }
            t2Data.append(json.dumps(obj))
        
        for i in range(len(task3_data)):
            if str(task3_data.iloc[i]['meddra_code']) == 'nan':
                obj = {
                    'tweet': task3_data.iloc[i]['tweet'],
                    'med_code': [],
                    'med_term': [],
                    'predictions': task3_data.iloc[i]['predictions']
                }
            else:
                obj = {
                    'tweet': task3_data.iloc[i]['tweet'],
                    'med_code': task3_data.iloc[i]['meddra_code'],
                    'med_term': task3_data.iloc[i]['meddra_term'],
                    'predictions': task3_data.iloc[i]['predictions']
                }
            if len(task3_data.iloc[i]['predictions']) > 0:

                if task3_data.iloc[i]['predictions'][1] not in predMedDict:
                    predMedDict[task3_data.iloc[i]['predictions'][1]] = 1
                else:
                    predMedDict[task3_data.iloc[i]['predictions'][1]] += 1
            t3Data.append(json.dumps(obj))

        for each in csv_m:
            if each[3] == 'ADR':
                drugNames.add(each[5])
                if each[5] not in drugDict:
                    drugDict[each[5]] = 1
                else:
                    drugDict[each[5]] += 1
                # if each[5] not in allDrugsDict:
                #     allDrugsDict[each[5]] = 1
                # else:
                #     allDrugsDict[each[5]] += 1
                if each[8] not in meddraDict:
                    meddraDict[each[8]] = 1
                else:
                    meddraDict[each[8]] += 1
            else:
                if each[5] != '':
                    drugNames.add(each[5])
                    if each[5] not in allDrugsDict:
                        allDrugsDict[each[5]] = 1
                    else:
                        allDrugsDict[each[5]] += 1
        for each in csv_f:
            if each[3] == 'ADR':
                drugNames.add(each[5])
                if each[5] not in drugDict:
                    drugDict[each[5]] = 1
                else:
                    drugDict[each[5]] += 1
                # if each[5] not in allDrugsDict:
                #     allDrugsDict[each[5]] = 1
                # else:
                #     allDrugsDict[each[5]] += 1
                # if each[8] not in meddraDict:
                #     meddraDict[each[8]] = 1
                # else:
                #     meddraDict[each[8]] += 1
            else:
                if each[5] != '':
                    drugNames.add(each[5])
                    if each[5] not in allDrugsDict:
                        allDrugsDict[each[5]] = 1
                    else:
                        allDrugsDict[each[5]] += 1
        sorted_drug = dict(sorted(drugDict.items(), key=operator.itemgetter(1),reverse=True))
        sorted_alldrug = dict(sorted(allDrugsDict.items(), key=operator.itemgetter(1),reverse=True))
        sorted_meddra = dict(sorted(meddraDict.items(), key=operator.itemgetter(1),reverse=True))
        sorted_pred_meddra = dict(sorted(predMedDict.items(), key=operator.itemgetter(1),reverse=True))
        sorted_drug = dict(list(sorted_drug.items())[0: 10])
        sorted_alldrug = dict(list(sorted_alldrug.items())[0: 10])
        sorted_meddra = dict(list(sorted_meddra.items())[0: 10])
        sorted_pred_meddra = dict(list(sorted_pred_meddra.items())[0: 10])
        medraChart = []
        predMedraChart = []
        drugChartLabels = []
        drugChartData = []
        drugAllChartLabels = []
        drugAllChartData = []
        t1ChartLabels = []
        t1ChartData = []
        for each in sorted_meddra:
            medraChart.append({
                'name': each,
                'y': sorted_meddra[each]
            })
        for each in sorted_pred_meddra:
            predMedraChart.append({
                'name': each,
                'y': sorted_pred_meddra[each]
            })
        for each in sorted_drug:
            drugChartLabels.append(each)
            drugChartData.append(sorted_drug[each])
        for each in sorted_alldrug:
            drugAllChartLabels.append(each)
            drugAllChartData.append(sorted_alldrug[each])
        for each in t1_obj:
            t1ChartLabels.append(each)
            t1ChartData.append(t1_obj[each])
        # print(drugsChart)
        # print("returned",t2Data)
        # print(t1_right_one, t1_right_zero, t1_wrong_one, t1_wrong_zero)
        result = [t2Data, t3Data, medraChart, [drugChartLabels, drugChartData], [t1ChartLabels, t1ChartData], predMedraChart, [drugAllChartLabels, drugAllChartData], t1Data, list(drugNames)]
        # opdata = json.loads(result)
        return result, 200
api.add_resource(GetData, '/')
api.add_resource(LiveTest, '/live-test')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',debug=True)
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)