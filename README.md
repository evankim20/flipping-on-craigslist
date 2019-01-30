# Flipping Craigslist's "Free" Section

Web scrapping Craigslist's "Free" section for items that can be resold for a profit, finished product will include how much one can profit off of the items and rate the avaliable free items by the profit the user can potential gain.

### Prerequisites

In order to run this on your machine download the following modules:

```
pip3 install pandas
pip3 install bs4
pip3 install selenium
```

### Usage

Simply call the cl_flip.py script to run.  It was ask for your zipcode and maximum radius in miles.

```python
python3 cl_flip.py
```

### To Do:
- [x] Add weighted score section
- [ ] Find the approximate distance from user to item and use this information in weighted score

