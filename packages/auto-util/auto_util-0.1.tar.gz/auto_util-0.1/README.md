# Auto Util

A command line tool for image matching.

## Install

```
pip install auto_util  #(3.7>=python>=3.4)
```

## Usage
```
auto_util match --help
```
```
Usage: auto_util match [OPTIONS]

  Result: 0 is Ok -101 is Fail -102 is Error

Options:
  --src TEXT         Source image path  [required]
  --search TEXT      The path of the image to be matched  [required]
  --threshold FLOAT  Confidence threshold
  --methods TEXT     Matching algorithm, can pass in multiple
                     [tpl,kaze,brisk,akaze,orb,sift,surf,brief]

  --help             Show this message and exit.
```
