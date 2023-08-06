

### There are four ways to check if the predictions are right or wrong:
```bash
  1. TN / True Negative: the case was negative and predicted negative
  2. TP / True Positive: the case was positive and predicted positive
  3. FN / False Negative: the case was positive but predicted negative
  4. FP / False Positive: the case was negative but predicted positive

  Precision:- Accuracy of positive predictions  = TP/(TP + FP)
  Recall:- Fraction of positives that were correctly identified = TP/(TP+FN)
  F1 Score = 2*(Recall * Precision) / (Recall + Precision)

```

## User installation :
If you already have a working installation of numpy and pandas, the easiest way to install plotly_ml_classification is using pip
```bash
pip install plotclassification
```

## This package depend on other packages:
```bash
  1.numpy
  2.pandas
  3.sklearn 
  4.plotly
```

## Usage

```python

# import libraries
import plotclassification 
from sklearn import datasets 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split 


# Load data
iris = datasets.load_iris()
# Create feature matrix
features = iris.data
# Create target vector 
target = iris.target

#create list of classname 
class_names = iris.target_names
class_names


# Create training and test set 
x_train, x_test, y_train, y_test = train_test_split(features,
                                                     target,
                                                     test_size=0.9, 
                                                     random_state=1)


# Create logistic regression 
classifier = LogisticRegression()

# Train model and make predictions
model = classifier.fit(x_train, y_train)

# create predicted probabilty matrix 
y_test__scores = model.predict_proba(x_test)

# initialize parameters value
plot=plotclassification.plot(y=y_test,
	         y_predict_proba=y_test__scores,
	         class_name=['Class 1','class 2','class 3'])

```

```python
plot.class_name
['Class 1', 'class 2', 'class 3']

# classification report plot
plot.plot_classification_report()

#  confusion matrix plot
plot.plot_confusion_matrix()

# precision recall curve plot
plot.plot_precision_recall_curve()

# roc plot
plot.plot_roc()

# predicted probability histogram plot
plot_probability_histogram()

```
[Github file source](https://github.com/vishalbpatil1/ml_classification_plot)
