# Granular.ai - Grain
Lightweight and un-opinionated experiment initializer for Granular.
Instantiating a grain experiment will allow any model developed to be used in production in the granular app _while allowing flexible experimentation_
Grain now also allows you to pass polyaxon experiment to grain. This allows user to pass all arguments to the polyaxon experiment.

Elements:
1. Argument parser with precomposed fields necessary for granular models.
2. Argument parser with autopush to polyaxon experiment.

# Basic pattern of use

```python
from phobos.grain import Grain

grain_exp = Grain()
grain_exp.add_argument(...) # use this exactly as you might use argparse
args = grain_exp.parse_args()

...

```

# Basic pattern of use with polyaxon experiment

```python
from polyaxon_client.tracking import Experiment
from phobos.grain import Grain

exp = Experiment()

grain_exp = Grain(polyaxon_exp=exp)
grain_exp.add_argument(...) # use this exactly as you might use argparse
args = grain_exp.parse_args()

...

```
