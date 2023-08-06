# TEXTA Bert Tagger Python package


## Installation

##### Using built package
`pip install texta-bert-tagger`

##### Using Git
`pip install git+https://git.texta.ee/texta/texta-bert-tagger-python.git`

### Testing

`python -m pytest -v tests`

### Documentation

Documentation for version 1.* is available [here](https://git.texta.ee/texta/texta-bert-tagger-python/-/wikis/Documentation-v1.*).

Documentation for version 2.* is available [here](https://git.texta.ee/texta/texta-bert-tagger-python/-/wikis/Documentation-v2.*).

## Usage (for versions >=2.*.*)

### Fine-tune BERT model

```python
from texta_bert_tagger.tagger import BertTagger
bert_tagger = BertTagger()

data_sample = {"good": ["It was a nice day.", "All was well."], "bad": ["It was horrible.", "What a disaster."]}

# Train a model

# pos_label - used in metrics (precision, recall, f1-score etc) calculations as true label
bert_tagger.train(data_sample, pos_label = "bad", n_epochs=2)

# Predict
result = bert_tagger.tag_text("How awful!")
print(result)
```

#### Output

```
{"prediction": "bad", "probability": 0.55200404}
```
