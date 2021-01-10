# Description

pfinsim stands for Personal FINance Simulation.

Its goal is to allow for users to easily investigate the effect of taxes and investing on their personal financial situation. Use cases can be found on [the author's blog](https://xgerrmann.github.io/geld-en-zo/).

As of writing this project is focused on the Dutch tax system. Efforts to extend towards other countries is highly appreciated.

The following is currently supported

* Investing
* Real estate
  * Mortgages
* Taxes
  * Tax credits
  * Income taxes
* Jobs
  * Monthly income
  * Holiday allowance

Python >= 3.7 is required



This project on [Github](https://github.com/xgerrmann/pfinsim)



# Deployment

```
rm build dist *.egg-info -r
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

 You will be asked for your PyPI (python package index) username and password for authentication, enter these.

## Log

* Uploaded to pypi as `pfinsim` 2020-12-26
