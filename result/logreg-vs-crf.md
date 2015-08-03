# Logistic regression VS CRF

## CRF performance

Performance by label (#match, #model, #ref) (precision, recall, F1):
    IC: (11972, 13022, 13889) (0.9194, 0.8620, 0.8897)
    AL: (37048, 39075, 37955) (0.9481, 0.9761, 0.9619)
    AU: (2643, 2651, 2643) (0.9970, 1.0000, 0.9985)
    AN: (5664, 5730, 5674) (0.9885, 0.9982, 0.9933)
    MX: (478, 547, 864) (0.8739, 0.5532, 0.6775)
Macro-average precision, recall, F1: (0.945363, 0.877912, 0.904203)
Item accuracy: 57805 / 61025 (0.9472)
Instance accuracy: 4078 / 5695 (0.7161)


## LogReg performance


Parameters:

	GridSearchCV(cv=None, error_score='raise',
	       estimator=LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
	          intercept_scaling=1, max_iter=100, multi_class='ovr',
	          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
	          verbose=2),
	       fit_params={}, iid=True, loss_func=None, n_jobs=6,
	       param_grid={'penalty': ['l1', 'l2'], 'C': [0.1, 1, 10]},
	       pre_dispatch='2*n_jobs', refit=True, score_func=None, scoring=None,
	       verbose=2)


Evaluation summary:
Subset accuracy: 95.26

             precision    recall  f1-score   support

         AL     0.9527    0.9787    0.9655     37955
         AN     0.9944    0.9989    0.9967      5674
         AU     0.9977    1.0000    0.9989      2643
         IC     0.9269    0.8740    0.8997     13889
         MX     0.9133    0.6215    0.7397       864

avg / total     0.9521    0.9526    0.9517     61025

Precision/Recall/F1(macro) : 0.9570  0.8946  0.9201

Precision/Recall/F1(micro) : 0.9526  0.9526  0.9526


Confusion matrix:

