# SVM Classification README
Extract features with 3 settings:<br>
1. ngram in Chinese characters<br>
2. ngram in pinyin<br>
3. ngram in Chinese characters with pinyin<br>
Note that the unit of a token is a segmented term instead of a single Chinese character.<br>

Convert training data into the format that libsvm accepts:<br>
Rating in three aspects (service, environment, flavor), ranging from 0 to 4, thus is given labels 1 to 5.<br>
Map each feature to an index and set its value to the occurrence within a review.<br>
Output the feature-index mapping table<br>
Train svm model.<br>

Convert developing set data into the libsvm input format with the feature-index mapping table generated in training.<br>
Predict on developing set and tune parameters.<br>
All intermediate results were cached.<br>

Task to be worked on:<br>
1. feature selection and reduce feature set.<br>
2. parameter tuning<br>

Library used:<br>
1. [libsvm](https://www.csie.ntu.edu.tw/~cjlin/libsvm/)<br>
2. [numpy](http://www.numpy.org/)<br>
Spring 2016 CSCI 544 Final Project.
