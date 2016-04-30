import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import h5py
import sys
def softmax(x, axis=1):
    """Compute softmax values for each sets of scores in x."""
    sf = np.exp(x)
    sf = sf/np.sum(sf, axis=axis)[:,np.newaxis]
    return sf
# input format: python roc.py FEAT_PATH FIGURE_PATH
feat_path = sys.argv[1]#'../train_yelp/3m/extracted_layer_23.json'
fig_path = sys.argv[2]
h5file = h5py.File(feat_path,'r')
scores = h5file['features']
labels = h5file['labels']

scores = np.array(scores)
labels = np.array(labels)
scores = softmax(scores)
score_sums = np.sum(scores,axis=1)
pos_scores = scores[:,1]
labels = labels - 1#1-base to 0-base
tot_n = len(labels)
fpr, tpr,_ = roc_curve(labels, pos_scores)
roc_auc = auc(fpr, tpr)
print 'AUC score: %f' % roc_auc
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.01])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.savefig(fig_path)

#calculate F1 score
preds = pos_scores > 0.5
precision = float(np.sum(labels & preds)) / np.sum(preds)
recall = float(np.sum(labels & preds)) / np.sum(labels)
f1score = 2 * precision * recall / (precision + recall)
accuracy = float(np.sum(labels == preds)) / tot_n
print 'precision: %f' % precision
print 'recall: %f' % recall
print 'accuracy: %f' % accuracy
print 'f1score: %f' % f1score