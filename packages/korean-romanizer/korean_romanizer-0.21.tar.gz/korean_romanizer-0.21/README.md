# korean-romanizer
korean-romanizer is a python module that romanizes Korean text in Hangul into its alphabet equivalent.

It currently follows the [Revised Romanization of Korean](https://www.korean.go.kr/front_eng/roman/roman_01.do) rule developed by the National Institute of Korean Language, the official romanization system being used in the Republic of Korea.


## Usage

### Installation
```bash
pip install korean_romanizer
```

### Basic Usage
```python
from korean_romanizer.romanizer import Romanizer

r = Romanizer("안녕하세요")
r.romanize() 
# returns 'annyeonghaseyo'
```
