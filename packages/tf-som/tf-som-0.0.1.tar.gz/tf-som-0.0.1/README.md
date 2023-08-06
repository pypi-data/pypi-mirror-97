# tf-som
Tensorflow self-organizing maps.
![](https://img.shields.io/badge/build-failing-red)
![](https://img.shields.io/badge/version-0.0.1-informational)

Locally competitive algorithms demonstrate superior convergence to their supervised
counterparts over a suite of tasks. Try them yourself:

```bash
pip install tf-som
```

```python
from .models import ConvNet

# build unsupervised base
unsupervised_base = ConvNet((H, W))

# train unsupervised
for x, _ in train_ds:
    unsupervised_base(x, training=True) 

...

# build supervised head
supervised_head = keras.Sequential([
    tfkl.Input(unsupervised_base.output_shape),
    tfkl.Conv2D(8, (3, 3), activation='relu'),
    tfkl.Flatten(),
    tfkl.Dense(N_classes, activation='softmax')
])

# assemble full classifier
unsupervised_base.trainable = False
classifier = keras.Sequential([
    unsupervised_base,
    supervised_head
])
classifier.compile('sgd', 'cross_entropy', 'accuracy')

# train supervised
classifier.fit(train_ds)

# compare model sizes
print(unsupervised_base.summary())
print(supervised_head.summary())
```