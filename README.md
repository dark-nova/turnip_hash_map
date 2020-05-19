# Turnip Map

## Overview

[turnips.yaml](turnips.yaml) contains a mapping of all turnip price sequences, organized by patterns (1st level keys), buy price per pattern (2nd level keys), and all sequences of minimums and maximums per day and phase (e.g. Monday AM) of that price.

## Usage

Run [turnips.py](turnips.py) to generate the file.

To access the sequences in Python, try this:

```python
import yaml

with open('turnips.yaml', 'r') as f:
    turnips = yaml.safe_load(f)

# This should print the 2nd sequence (0 index, "[1]") in
# pattern 0 (fluctuating, "[0]") with a buy price of 90 Bells.
print(turnips[0][90][1])
```

## Requirements

This code is designed around the following:

- Python 3+

## Credits

Credits to **Ninji** for the [gist](https://gist.github.com/Treeki/85be14d297c80c8b3c0a76375743325b) that led to this mapping. Credits also to **mikebryant** for https://turnipprophet.io/index.html ([GitHub](https://github.com/mikebryant/ac-nh-turnip-prices)) for inspiration and referencing Ninji's [tweet](https://twitter.com/_Ninji/status/1244818665851289602).

## Disclaimer

This project is not affiliated with or endorsed by *[Nintendo][nintendo]*. See [LICENSE](LICENSE) for more detail.

[acnh]: https://www.animal-crossing.com/new-horizons/
[nintendo]: https://www.nintendo.com/
