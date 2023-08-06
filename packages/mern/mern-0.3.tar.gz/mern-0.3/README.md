# mern

mern is python library to help us process our dataset, it can process numeric and text data

### Installation

```bash
pip3 install mern
```

or

```bash
git clone https://github.com/bluenet-analytica/mern.git && cd mern && pip3 install -r requirements.txt
```

### 1. Remove outlier in numerical data

There are 2 ways to remove data on numerical data type

1. Z Score
2. Inter Quartile Score Range (IQR Score)

```python
from mern import NumericOutlier

obj = NumericOutlier()
x = [11,31,21,19,8,54,35,26,23,13,29,17]

# using Z Score
print(obj.find(x, "zscore"))

# using Inter Quartile Range Score
print(obj.find(x, "iqr"))
```

### 2. Remove outlier in text data

```python
from mern import TextOutlier

obj = TextOutlier()
text = "abcd!G#45!"

# remove punctuation ex : !@#$%
no_punctuation = obj.remove_punctuation([text])
print(no_punctuation)

# remove stop words ex : this, the, a, etc
# tweets by @SomeGuyAbides

tweets = "Is a burning compressed liquid hydrogen as rocket fuel feasible for a propellant? Could this process be deleveloped through electrolysis of water? "

no_sw = obj.remove_stopwords([tweets], lang="english")

```

That's it.
