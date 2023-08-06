# Granular.ai - Metrics
Loss function and metrics repository for granular ai geo-ops.
Metrics allows automatic logging of training time metrics to polyaxon.

Elements:
1. Loss functions.
2. Metrics class that allows metrics computation and logging in polyaxon.

# Basic pattern of use

```python
from phobos.metrics import Metrics
from phobos.metrics.loss import DiceLoss

metrics = Metrics(['dc', 'jc', 'prec', 'recall'])

model = UNet()
criterion = DiceLoss()

for epoch in range(10):
  for img, lbl in loader:
    pred = model(img)
    loss = criterion(pred, lbl)
    metrics.compute(pred, lbl, loss)

  metrics.crunch_it(epoch)
  metrics.reset()
```
