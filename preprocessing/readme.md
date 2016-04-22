## Preprocessing Readme

### Overview

Preprocess the reviews for future classification. 

Only keep reviews for restaurants, and with environment, service, and flavor scores, and the reviews should be in Simplified Chinese. Split the large file into smaller files for processing.

Add segmentation and pinyin to the filtered results, and the output the result in a json format.


### Process Procedure Introduction

**FilterRecord.py**

1. Construct restaurant url dictionary from the "review.txt". 
2. For reviews for these restaurants, use langdetect lib to detect the language, and filter out the reviews written in Simplified Chinese, and with the environment, service and flavor scores. (Scores range: [0,4] ). Get 3,235,043 records total.
3. Split the large review file into smaller files. (190 files total)

*Note: Maunally deleted the first row in reviews.txt for the format*

**Preprocess.py**

1. Get the review contents. For each line in the reviews, call LTP for segmentation.
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
		
### How to run the code
* Install needed packages. (langdetect, pinyin)
* Install pyltp from the github.
* Download pyltp's version 3.3.0 model from [Baidu Pan](http://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569).
* Copy the ltp_data folder under the root folder for this project (ltp_data folder has the same level as the preprocessing folder)
* Run 


		$python FilterRecord.py
		
* Run

		$python Preprocess.py 0 190

It will generate 190 files with the name of o\_[index].txt, and 190 files with the name of p\_[index].txt.

The files with the name of p\_[index].txt are the input files for further processing.



## Used Libs
* [Langdetect (v 1.0.6)](https://pypi.python.org/pypi/langdetect) | [Github](http://lxyu.github.io/pinyin/)
* [pinyin (v 0.3)](https://pypi.python.org/pypi/pinyin) | [Github](https://github.com/lxyu/pinyin)
* [pyltp (v 3.3.0)](https://github.com/HIT-SCIR/pyltp)
* [codecs](https://docs.python.org/2/library/codecs.html)
* [json](https://docs.python.org/2/library/json.html)
