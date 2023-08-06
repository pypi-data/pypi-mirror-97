# CV Datasets Wrapper

<!-- For more deatils to see how to use this library take a look at [nabirds/display.py](nabirds/display.py). -->

## Annotation and Image Loading

Here is some example code how to load images and use the predefined train-test split.

```python
# replace NAB_Annotations with CUB_Annotations to load CUB200-2011 annotations
from cvdatasets import NAB_Annotations, Dataset

annot = NAB_Annotations("path/to/nab/folder")

train_data = Dataset(uuids=annot.train_uuids, annotations=annot)
test_data = Dataset(uuids=annot.test_uuids, annotations=annot)

print("Loaded {} training and {} test images".format(len(train_data), len(test_data)))
```

Alternatively, you can create an annotation and a dataset instance from a YAML dataset file:

```python
annot = NAB_Annotations("path/to/yaml/config_file.yml")

train_data = annot.new_dataset("train")
test_data = annot.new_dataset("test")
```

An example YAML dataset file could be the following:

```yaml
BASE_DIR: /data/your_data_folder/

# in BASE_DIR should be "datasets" and "models" folder
DATA_DIR: datasets
MODEL_DIR: models


# in /data/your_data_folder/datasets should be "birds" and  there should be a "cub200_11" folder with the CUB200 dataset. this represents default annotation folder.
DATASETS:
  CUB200:         &cub200
    folder: birds
    annotations: cub200_11

# Here we define different types of part annotations
PARTS:
  # uniform 5x5 parts
  UNI:            &parts_uni
    <<: *cub200
    is_uniform: true
    annotations: cub200_11
    rescale_size: !!int -1
    scales:
     - 0.2

  # ground truth parts
  GT:             &parts_gt
    <<: *cub200
    annotations: cub200_11
    rescale_size: !!int -1
    scales:
     - 0.31

  # NAC parts with 2 scales
  NAC:            &parts_nac
    <<: *cub200
    annotations: NAC/2017-bilinear
    feature_suffix: 20parts_gt
    rescale_size: !!int 224
    scales:
      - 0.31
      - 0.45
```


## Dataset Iteration
```python
import matplotlib.pyplot as plt

# either access the images directly
im, parts, label = test_data[100]
plt.imshow(im)
plt.show()

# or iterate over the dataset
for im, parts, label in train_data:
    plt.imshow(im)
    plt.show()

```

## Working with Part Annotations
Both datasets (NAB and CUB) have part annotations. Each annotation has for each of the predefined parts the location of this part and a boolean (`0` or `1`) value whether this part is visible. A [`Dataset`](cvdatasets/dataset/__init__.py) instance returns besides the image and the class label this information:

```python

im, parts, label = train_data[100]

print(parts)
# array([[  0, 529, 304,   1],
#        [  1, 427, 277,   1],
#        [  2, 368, 323,   1],
#        [  3,   0,   0,   0],
#        [  4, 449, 292,   1],
#        [  5, 398, 502,   1],
#        [  6, 430, 398,   1],
#        [  7,   0,   0,   0],
#        [  8, 365, 751,   1],
#        [  9,   0,   0,   0],
#        [ 10,   0,   0,   0]])
...
```



### Visible Parts

In order to filter by only visible parts use the [`visible_locs`](cvdatasets/dataset/part.py#L46) method. It returns the indices and the x-y positions of the visible parts:

```python
...

idxs, xy = parts.visible_locs()

print(idxs)
# array([0, 1, 2, 4, 5, 6, 8])
print(xy)
# array([[529, 427, 368, 449, 398, 430, 365],
#        [304, 277, 323, 292, 502, 398, 751]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
```

### Uniform Parts
In case you don't want to use the ground truth parts, you can generate parts uniformly distributed over the image. Here you need to pass the image as well as the ratio, which tells how many parts will be extracted (ratio of `1/5` extracts 5 by 5 parts, resulting in 25 parts). In case of uniform parts all of them are visible.


```python
...
from cvdatasets.dataset.part import UniformParts

parts = UniformParts(im, ratio=1/3)
idxs, xy = parts.visible_locs()

print(idxs)
# array([0, 1, 2, 3, 4, 5, 6, 7, 8])
print(xy)
# array([[140, 420, 700, 140, 420, 700, 140, 420, 700],
#        [166, 166, 166, 499, 499, 499, 832, 832, 832]])

x, y = xy
plt.imshow(im)
plt.scatter(x,y, marker="x", c=idxs)
plt.show()
...
```

### Crop Extraction
From the locations we can also extract some crops. Same as in [`UniformParts`](cvdatasets/dataset/part.py#L76) you have to give a ratio with which the crops around the locations are created:

```python
...

part_crops = parts.visible_crops(im, ratio=0.2)

fig = plt.figure(figsize=(16,9))
n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in enumerate(part_crops, 1):
    ax = fig.add_subplot(rows, cols, j)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
...
```


### Random Crops
In some cases randomly selected crops are desired. Here you can use the [`utils.random_index`](cvdatasets/utils/__init__.py#L3) function. As optional argument you can also pass a `rnd` argument, that can be an integer (indicating a random seed) or a `numpy.random.RandomState` instance. Additionally, you can also determine the number of crops that will be selected (default is to select random number of crops).

```python
...
from cvdatasets import utils
import copy

part_crops = parts.visible_crops(im, ratio=0.2)
idxs, xy = parts.visible_locs()

rnd_parts = copy.deepcopy(parts)
rnd_idxs = utils.random_idxs(idxs, rnd=rnd, n_parts=n_parts)
rnd_parts.select(rnd_idxs)
# now only selected parts are visible
rnd_part_crops = rnd_parts.visible_crops(im, ratio=0.2)

fig = plt.figure(figsize=(16,9))

n_crops = part_crops.shape[0]
rows = int(np.ceil(np.sqrt(n_crops)))
cols = int(np.ceil(n_crops / rows))

for j, crop in zip(rnd_idxs, rnd_part_crops):
    ax = fig.add_subplot(rows, cols, j + 1)
    ax.imshow(crop)
    ax.axis("off")

plt.show()
...
```


### Revealing of the Parts
In order to create a single image, that consist of the given parts on their correct location use [`reveal`](cvdatasets/dataset/part.py#L58) function. It requires again besides the original image and the locations the ratio with which the parts around the locations should be revealed:

```python

plt.imshow(parts.reveal(im, ratio=0.2))
plt.show()

plt.imshow(rnd_parts.reveal(im, ratio=0.2))
plt.show()
```


## Hierarchies
Hierachy file is currently only loaded. Code for proper processing is needed!
