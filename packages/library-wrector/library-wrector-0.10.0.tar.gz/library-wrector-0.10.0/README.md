# library.wrector

![gif](https://media.giphy.com/media/YOqbsB7Ega18s/giphy.gif)

Original implementation: https://github.com/grammarly/gector

Tested (and works only :sob:) with python 3.7

### Installation
```sh
pip install library-wrector
```
### Quick start

```python
from library_wrector import Wrector
import spacy

nlp = spacy.load("en_core_web_sm")
wrector = Wrector(nlp, model_paths=["path/to/your/gector/like/model"])

wrector("Does you like cats?")
'Do you like cats ?'
```

### Models:

- original gec: [link](https://drive.google.com/file/d/1mHIwsPAE1J_D2fh1RFU266qlA0Qlx1Kz/view?usp=sharing)