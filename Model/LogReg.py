import os
cwd = os.getcwd()
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import numpy as np

train = pd.read_csv(os.path.join(cwd, "GEO_train.csv"), na_filter = False)
dev = pd.read_csv(os.path.join(cwd, "GEO_dev.csv"), na_filter = False)
test = pd.read_csv(os.path.join(cwd, "GEO_test.csv"), na_filter = False)
print("==========Train==========")
print(train.info())
print("=========================")
print(train.describe())
print("==========Dev==========")
print(dev.info())
print("========================")
print(dev.describe())
print("==========Test==========")
print(test.info())
print("========================")
print(test.describe())


features = ["min_distance", "avg_distance", "max_population"]

x_train = train[features]
y_train = train["label"]
x_dev = dev[features]
y_dev = dev["label"]
x_test = test[features]

# Modeling
parameters = [{"penalty": ["l2"], "C": [0.0001, 0.001, 0.01, 0.1, 0.5, 1.0, 1.5, 10], "solver": ["lbfgs"]},
              {"penalty": ["l1", "l2"], "C": [0.0001, 0.001, 0.01, 0.1, 0.5, 1.0, 1.5, 10], "solver": ["liblinear"]}]
lg = LogisticRegression(class_weight='balanced')
grid = GridSearchCV(lg, parameters, cv = 10, return_train_score = True, scoring = "roc_auc")
grid = grid.fit(x_train, y_train)

clf = grid.best_estimator_
clf.fit(x_train, y_train)

print("Best Param: ", grid.best_params_)
print("Best_score: ", grid.best_score_)

print("========== Balanced ==========")
predictions_dev = clf.predict(x_dev)
predictions_test = clf.predict(x_test)

print("Accuracy Score (Balanced, Dev): ", accuracy_score(y_dev, predictions_dev))
print("Confusion Matrix (Balanced, Dev): \n", confusion_matrix(y_dev, predictions_dev))
print(classification_report(y_dev, predictions_dev))

print("========= Max Prob of Each Location ==========")
location = dev.Location.unique()
pred_max_dev = np.array([])
for loc in location:
    loc_index = dev["Location"] == loc
    prob = clf.predict_proba(x_dev[loc_index])[:, 1]
    tmp = np.where(prob == prob[prob.argmax()], 1, 0)
    pred_max_dev = np.concatenate([pred_max_dev, tmp])

print("Accuracy Score (Max, Dev): ", accuracy_score(y_dev, pred_max_dev))
print("Confusion Matrix (Max, Dev): \n", confusion_matrix(y_dev, pred_max_dev))
print(classification_report(y_dev, pred_max_dev))

print("=== Feature Importance ===")
print("Coefficient: ", clf.coef_)

location = test.Location.unique()
pred_max_test = np.array([])
for loc in location:
    loc_index = test["Location"] == loc
    prob = clf.predict_proba(x_test[loc_index])[:, 1]
    tmp = np.where(prob == prob[prob.argmax()], 1, 0)
    pred_max_test = np.concatenate([pred_max_test, tmp])

prediction = pd.Series(pred_max_dev, name = "prediction")
df_pred = pd.concat([dev, prediction], axis = 1)
df_pred.to_csv("GEO_pred_dev.csv", index = False)

prediction = pd.Series(pred_max_test, name = "prediction")
df_pred = pd.concat([test, prediction], axis = 1)
df_pred.to_csv("GEO_pred_test.csv", index = False)
