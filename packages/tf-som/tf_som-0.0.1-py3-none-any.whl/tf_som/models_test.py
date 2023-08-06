import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as tfkl

from .models import ConvNet

# get and preprocess data
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Add a channels dimension
x_train = x_train[..., tf.newaxis].astype("float32")
x_test = x_test[..., tf.newaxis].astype("float32")

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(16)

H = x_train.shape[1]
W = x_train.shape[0]
N_classes = y_train.shape[-1]

# build unsupervised base
unsupervised_base = ConvNet((H, W))

# train unsupervised
for x, _ in train_ds:
    unsupervised_base(x, training=True)

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

# test model
test_images, test_labels = next(iter(test_ds))

unsupervised_annotations = unsupervised_base(test_images)
greyscale_annotations = tf.argmax(unsupervised_annotations, axis=-1,
                    output_type=tf.float32) / unsupervised_base.output_shape[-1]
y_pred = supervised_head(unsupervised_annotations)[0]
pred_indeces = tf.argmax(y_pred)

# visualize test results
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
plt.figure(figsize=(10, 10))
for i in range(test_images.shape[0]):
    image = test_images[i]

    # this shows unmodified image and label
    plt.subplot(8, 4, 2*i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(image)
    # The CIFAR labels happen to be arrays,
    # which is why you need the extra index
    plt.xlabel(class_names[y_train[i][0]])
    plt.show()

    # this shows annotated image and predicted labels
    plt.subplot(8, 4, 2*i + 2)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(greyscale_annotations[i][..., None])
    plt.xlabel(class_names[pred_indeces[i]])
    plt.show()
