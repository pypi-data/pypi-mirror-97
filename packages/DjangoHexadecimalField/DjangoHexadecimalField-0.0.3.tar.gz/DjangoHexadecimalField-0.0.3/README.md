# Django-Hexadecimal-Field
Hexadecimal field in Django for hexadecimal inputs

## Installation

## Usage
Import the HexadecimalField from fields.py 

```python

from djangoHexadecimal.fields import HexadecimalField
from django.db import models

class SampleModel(model.Model):
    hex_num = HexadecimalField(max_length='25')

```
Note that user must specify max_length

Similarly , the user can define their own validators which will be appended to hexadecimal validator

```python

from djangoHexadecimal.fields import HexadecimalField
from django.db import models

class SampleModel(model.Model):
    hex_num = HexadecimalField(max_length='25',validators=[custom_validator])

```
