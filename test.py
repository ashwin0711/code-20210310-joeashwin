import unittest
import csv
import pathlib
from code import Calculator


class CodeTest(unittest.TestCase):

    def setUp(self):
        directory = str(pathlib.Path(__file__).parent.absolute())
        input_file = directory+"/test_case.csv"
        self.rows = []
        self.calculate = Calculator()
        with open(input_file, 'r') as csv_file: 
            csv_data = csv.reader(csv_file)
            field_names = next(csv_data) 
            for row in csv_data: 
                self.rows.append(row)
    
    def test_bmi(self):
        for row in self.rows:
            height = int(row[0])
            weight = int(row[1])
            expected_bmi = float(row[2])
            bmi = self.calculate.calculate_bmi(height,weight)
            self.assertEqual(bmi, expected_bmi)
            
    def test_category(self):
        for row in self.rows:
            bmi = float(row[2])
            expected_category = row[3].upper()
            expected_category = expected_category.replace("\xa0", " ")
            category, risk = self.calculate.calculate_category_risk(bmi)
            self.assertEqual(category.upper(),expected_category)
    
    def test_risk(self):
        for row in self.rows:
            bmi = float(row[2])
            category, risk = self.calculate.calculate_category_risk(bmi)
            expected_risk = row[4].upper()
            expected_risk = expected_risk.replace("\xa0"," ")
            self.assertEqual(risk.upper(), expected_risk)



if __name__ == '__main__':
    unittest.main()