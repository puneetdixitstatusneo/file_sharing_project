import json
import csv
import yaml
from yaml import SafeLoader
import os


class FileConversion():
    def __init__(self, source_file_path, source_ext, destination_ext, destination_file_name = ""):
        self.source_file_path = source_file_path
        self.source_ext = source_ext
        self.destination_ext = destination_ext
        self.destination_file_name = destination_file_name
        self.status, self.destination_file_path = self.convert(self.source_ext, self.destination_ext, self.source_file_path, self.destination_file_name)




    def convert(self, source_ext, destination_ext, source_file_path, destination_file_name):

        if destination_file_name == "":
            destination_file_path = source_file_path.replace("."+source_ext, "."+destination_ext)
        else:
            destination_file_path = os.path.join(os.path.dirname(source_file_path), destination_file_name+"."+destination_ext)

        if source_ext == "json" and destination_ext == "csv":
            return True, self.json_to_csv(source_file_path, destination_file_path)
            
        elif source_ext == "csv" and destination_ext == "json":
            return True, self.csv_to_json(source_file_path, destination_file_path)
        
        elif source_ext == "json" and destination_ext == "yaml":
            return True, self.json_to_yaml(source_file_path, destination_file_path)
        
        elif source_ext == "yaml" and destination_ext == "json":
            return True, self.yaml_to_json(source_file_path, destination_file_path)
        return False, ""

    def json_to_csv(self, source_file_path, destination_file_path):
        with open(source_file_path, encoding='utf-8-sig') as json_file:
            jsondata = json.load(json_file)
        data_file = open(destination_file_path, 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 0
        for data in jsondata:
            if count == 0:
                header = data.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(data.values())
        data_file.close()
        return destination_file_path


    def csv_to_json(self, csvFilePath, jsonFilePath):
        jsonArray = []
        with open(csvFilePath, encoding='utf-8-sig') as csvf: 
            csvReader = csv.DictReader(csvf) 
            for row in csvReader: 
                jsonArray.append(row)
    
        with open(jsonFilePath, 'w', encoding='utf-8-sig') as jsonf: 
            jsonString = json.dumps(jsonArray, indent=4)
            jsonf.write(jsonString)

        return jsonFilePath


    def json_to_yaml(self, source_file_path, destination_file_path):
        with open(source_file_path, encoding='utf-8-sig') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                file=open(destination_file_path,"a")
                yaml.dump(data,file)
            file.close()
            return destination_file_path


    def yaml_to_json(self, source_file_path, destination_file_path):
        with open(source_file_path) as yaml_file:
            python_dict=yaml.load(yaml_file, Loader=SafeLoader)
        file=open(destination_file_path,"w")
        json.dump(python_dict,file)
        file.close()
        return destination_file_path

