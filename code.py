import json
import pathlib
import configparser
import logging
from datetime import datetime

class Calculator:

    def __init__(self):
        directory = str(pathlib.Path(__file__).parent.absolute())
        input_file = directory+"/input.json"
        config_file = directory+"/config.ini"
        log_file = directory+"/calculator_logs.log"
        self.document_path = directory+"/document.txt"
        self.output_file = directory+"/output.json"
        with open(input_file,'r') as json_file:
            self.input_data = json.loads(json_file.read())

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        print("Refer to calculator_logs.log for the logs")
        print("Refer to config.ini for the configurations")
        logging.basicConfig(filename=log_file,level=logging.INFO)
        timenow = datetime.now()
        date = timenow.strftime("%c")
        self.date = "[ "+date+" ] "

    def main_function(self):
        output_list = []
        try:
            for person in self.input_data:
                height = person['HeightCm']
                weight = person['WeightKg']
                BMI = self.calculate_bmi(height,weight)
                person['BMI'] = BMI
                bmi_category, risk = self.calculate_category_risk(BMI)
                person['BMI_category'] = bmi_category
                person['health risk'] = risk
                output_list.append(person)
            with open(self.output_file, 'w') as file:
                output_json = json.dumps(output_list,indent = 4)
                file.write(output_json)
            self.analysis()
            print("Calculations done and results stored in output.json")
        except Exception as e:
            logging.error(self.date+" Error in main_function : "+str(e))

    def calculate_bmi(self,height,weight):
        try:
            height = height/100
            height_squared = height*height
            BMI = round(weight/height_squared,2)
            return float(BMI)
        except Exception as e:
            logging.error(self.date+" Error occured when calculating bmi : "+str(e))
        

    def calculate_category_risk(self,BMI):
        range1 = self.config['BMI_Range']['range1'].split(",")
        range2 = self.config['BMI_Range']['range2'].split(",")
        range3 = self.config['BMI_Range']['range3'].split(",")
        range4 = self.config['BMI_Range']['range4'].split(",")
        range5 = self.config['BMI_Range']['range5'].split(",")
        max_range = self.config['BMI_Range']['max_range'].split(",")
        category = ""
        risk = ""
        try:
            if(BMI>=float(range1[0])) and (BMI<=float(range1[1])):
                category = range1[2]
                risk = range1[3]
            elif(BMI>=float(range2[0])) and (BMI<=float(range2[1])):
                category = range2[2]
                risk = range2[3]
            elif(BMI>=float(range3[0])) and (BMI<=float(range3[1])):
                category = range3[2]
                risk = range3[3]
            elif(BMI>=float(range4[0])) and (BMI<=float(range4[1])):
                category = range4[2]
                risk = range4[3]
            elif(BMI>=float(range5[0])) and (BMI<=float(range5[1])):
                category = range5[2]
                risk = range5[3]
            elif(BMI>float(max_range[0])):
                category = max_range[1]
                risk = max_range[2]
            return category,risk
        except Exception as e:
            logging.error(self.date+" Error occured when assesing category and risk : "+str(e))
        
    def analysis(self):
        male = 0
        female = 0
        overweight_male_count = 0
        overweight_female_count = 0
        underweight_male = 0
        underweight_female = 0
        normalweight_male = 0
        normalweight_female = 0
        obese_male = 0
        obese_female = 0

        overweight_percentage = 0
        male_overweight_percentage = 0
        female_overweight_percentage = 0

        with open(self.output_file,'r') as json_file:
            data_list = json.loads(json_file.read())
        
        total_count = len(data_list)
        for people in data_list:
            if(people['Gender']=="Male" and people['BMI_category']=="Overweight"):
                overweight_male_count+=1
                male+=1
            elif(people['Gender']=="Female" and people['BMI_category']=="Overweight"):
                overweight_female_count+=1
                female+=1
            elif(people['Gender']=="Male" and people['BMI_category']=="Underweight"):
                underweight_male+=1
                male+=1
            elif(people['Gender']=="Female" and people['BMI_category']=="Underweight"):
                underweight_female+=1
                female+=1
            elif(people['Gender']=="Male" and people['BMI_category']=="Normal weight"):
                normalweight_male+=1
                male+=1
            elif(people['Gender']=="Female" and people['BMI_category']=="Normal weight"):
                normalweight_female+=1
                female+=1
            else:
                if(people['Gender']=="Male"):
                    obese_male+=1
                    male+=1
                elif(people['Gender']=="Female"):
                    obese_female+=1
                    female+=1
        try:
            total_normal = normalweight_male + normalweight_male
            total_overweight = overweight_male_count + overweight_female_count
            total_underweight = underweight_male + underweight_female
            total_obese = obese_male + obese_female
            if(total_overweight>0):
                overweight_percentage = round((total_overweight/total_count)*100,2)
                male_overweight_percentage = round((overweight_male_count/total_overweight)*100,2)
                female_overweight_percentage = round((overweight_female_count/total_overweight)*100,2)
        except Exception as e:
            logging.error(self.date+" Error occured when analysing  : "+str(e))


        line1 = "Total number of people in input = "+str(total_count)+" Where there are "+str(male)+ " males and "+str(female)+" females."
        line2 = "There are "+str(total_normal)+" normal weight people and among them, there are "+str(normalweight_male)+" males and "+str(normalweight_male)+" females"
        line3 = "There are "+str(total_overweight)+" over weight people and among them, there are "+str(overweight_male_count)+" males and "+str(overweight_female_count)+" females"
        line4 = "There are "+str(total_underweight)+" under weight people and among them, there are "+str(underweight_male)+" males and "+str(underweight_female)+" females"
        line5 = "There are "+str(total_obese)+" obese people and among them, there are "+str(obese_male)+" males and "+str(obese_female)+" females"
        line6 = "Out of the "+str(total_count)+" people, "+str(overweight_percentage)+'%'+" of the people are overweight"
        line7 = "Among the "+str(total_overweight)+" over weight poeple, "+str(male_overweight_percentage)+'%'+" are male and "+str(female_overweight_percentage)+'%'+" are female"
        line_list = [line1,line2, line3, line4, line5, line6, line7]
        with open(self.document_path, 'w') as document:
            document.writelines(line + '\n' for line in line_list)
        print("Analysis results stored in document.txt")
            
if __name__ == '__main__':
    BMI_Calculator = Calculator()
    BMI_Calculator.main_function()