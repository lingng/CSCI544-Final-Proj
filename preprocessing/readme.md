## Preprocessing Readme

### Overview

Preprocess the reviews for future classification. 

Only keep reviews for restaurants, and with environment, service, and flavor scores, and the reviews should be in Simplified Chinese. Split the large file into smaller files for processing.

Add segmentation and pinyin to the filtered results, and the output the result in a json format.


### Process Procedure

**FilterRecord.py**

1. Construct restaurant url dictionary from the "review.txt". 
2. For reviews for these restaurants, use langdetect lib to detect the language, and filter out the reviews written in Simplified Chinese, and with the environment, service and flavor scores. (Scores range: [0,4] ). Get the total count as:
3. Split the large review file into smaller files.

**Preprocess.py**

1. Get the review contents. For each line in the reviews, call NLP for segmentation.
2. For each word in the segmentation, use pinyin to get the pinyin for this word.
3. Construct the result json for each review in the following format:
	
		{	
			'flavor': flavor score,
			'environment': environment score,
			'service': service score,
			'content': original review content,
			'segmentation': segmentation of the review content,
			'pinyin': pinyin for the segmentation
		}
		
### Used Libs
* [Langdetect (v 1.0.6)](https://pypi.python.org/pypi/langdetect) | [Github](http://lxyu.github.io/pinyin/)
* [pinyin (v 0.3)](https://pypi.python.org/pypi/pinyin) | [Github](https://github.com/lxyu/pinyin)
* [jieba (v 0.38)](https://pypi.python.org/pypi/jieba) | [Github](https://github.com/fxsjy/jieba)
* [LTP (v 3.1.0)](http://www.ltp-cloud.com/intro/en/)
* [requests (v 2.9.1)](http://docs.python-requests.org/en/master/)
* [urllib2](https://docs.python.org/2/library/urllib2.html#module-urllib2)
* [codecs](https://docs.python.org/2/library/codecs.html)
* [json](https://docs.python.org/2/library/json.html)

### Other Resources
* Commonly mistyped word