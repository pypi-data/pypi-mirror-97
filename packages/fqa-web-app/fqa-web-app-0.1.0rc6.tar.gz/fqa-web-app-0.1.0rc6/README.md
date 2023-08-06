# FeedbackQA Web App
<!-- 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plotly/dash-sample-apps/blob/master/apps/feedbackqa-web-app/ColabDemo.ipynb)
 -->

## Quickstart

To get started, run:
```
pip install fqa-web-app
```

If you want to use the toy feedback QA model (which is a simple sklearn LSA model), you will need to further install:

```
pip install scikit-learn
```


## Running tests

First install the library in editable mode and scikit-learn:
```
pip install -e .
pip install scikit-learn
```

Then, you can run any test you want:
```python
python tests/test_toy_models.py
```