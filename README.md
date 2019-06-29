# Hooke
Written in python, and based on quite a few requirements
  
It is yet to work properly

## Installation
Due to some errors, it is required to install textract and download 'punkt' manually.
```
pip install git+https://github.com/oekshido/textract
pip install pyHooke
python
>>import nltk
>>nltk.download('punkt')
```

## Usage
To run a simple textual check:
```python
from Hooke import Hooke

hk = Hooke() #Inits
hk.Textual(input="test/test.txt") #Runs the comparison
hk.print_matches() #Prints matches and source
hk.time() #Prints time taken
```

## Contributing
Just pull request.
