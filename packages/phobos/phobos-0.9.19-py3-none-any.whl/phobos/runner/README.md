# Granular.ai - Runner
Runner class to manage train and validation epoch and metrics computation for an epoch.

# Basic pattern of use

```python
from phobos.experiment import Runner

runner = Runner(device=0, model=model,
                optimizer=optimizer, criterion=criterion,
                train_loader=train_loader, val_loader=val_loader,
                train_metrics=train_metrics, val_metrics=val_metrics, polyaxon_exp=None)

for epoch in range(epochs):
  runner.set_epoch_metrics()
  train_metrics = runner.train_model()
  eval_metrics = runner.eval_model()

```
