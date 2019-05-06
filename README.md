# Toponym Disambiguation

In this subtask, all names of locations are known by the resolver but not their precise coordinates. 
The resolver has to select the GeoNames ID corresponding to the expected place among all possible candidates.

it contains:

1. Preprocessing for GEO dictionary
2. feature engineering (distance and population)
3. Logistic Regression Modeling
4. Evaluation

## Getting Started

### Prerequisites

```
python>=3.72
numpy>=1.15
scikit-learn>=0.20
```

### Installing

Clone this repository

```
git clone https://github.com/AllenTiTaiWang/SemEval2019_Task12.git
```

### Going to the right Directory

First of all, go to EnrollDec file.

```
cd SemEval2019_Task12
```

Make sure you have a file named **Final_dataset** under file **Feature**.
Final_dataset should be provided by the task , which contains train, dev, 
and test data.

```
cp -r /path/to/Final_dataset /path/to/SemEval2019_Task12/Feature/
```

Also, create a file named **data** which contains three empty files: dev, train, and test, 
and make sure you have a dictionary called **geo_dict_with_population_lonalt.txt** in 
this same directory.

```
mkdir /path/to/SemEval2019_Task12/data
mkdir /path/to/SemEval2019_Task12/data/train
mkdir /path/to/SemEval2019_Task12/data/test
mkdir /path/to/SemEval2019_Task12/data/dev

cp /path/to/geo_dict_with_population_lonalt.txt /path/to/SemEval2019_Task12/data/
```

This task can't run without data and dictionary.

## Pipeline

The command below assumes that Feature engineering and modeling runnung under HPC environment.

### Preprocessing

downsize the dictionary and store it in json file.

```
cd Feature
python3 DicGEO.py
```

This code generates geoname2id.json and geoid2la.json.

###Feature Engineering

and then upload files on HPC, and run the following scripts under HPC. (highly recommend)
1. **Make sure you change the path in .sh file before running them.**
2. **Make sure create output and error file in the directory you want.**

```
qsub < CalDistance.sh
qsub < CalDistance_train.sh
qsub < CalDistance_test.sh
```

These three jobs will create the features for each involved geonameid.
it could take a while, since minimum and average distance will be calculated.
The result will be in data/dev, data/train, and data/test.


### Modeling

In this step, the data in data/train, data/dev, and data/test will be organized into a
huge feature matrix, and logistic regression model will then be trained.

```
qsub < LogReg.sh
```

### Evaluation

Evaluation doesn't need to be conducted under HPC.

#### Dev Performance

Generate the annotation file from your prediction results

```
python3 Evaluation/generateann.py
```

Run their evaluator

```
python3 Evaluation/SemEvalTask12Evaluator/Evaluator/ToponymEvaluator.py disambiguation/ results/ Disambiguation
```

Check the dev score

```
less results/scores.txt
```

Generate the test annotation predictions

```
python3 testfinal.py
```

then the annotation files should be in testann file.
