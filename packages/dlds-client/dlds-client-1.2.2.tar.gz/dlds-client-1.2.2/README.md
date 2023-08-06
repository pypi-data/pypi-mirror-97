# Deep Learning DS Client
The Deep Learning DS (DLDS) Client acts as an interface to the data spree vision platform and provides an command-line
tool that allows importing datasets of the following formats:
* DLDS
* KITTI
* COCO

Furthermore, it is possible to export datasets from the platform.

## Usage

### General Usage
```
Usage: dlds [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export
  import
```

### Dataset Import
```
Usage: dlds import [OPTIONS]

Options:
  --format [dlds|kitti|coco]  Dataset format to import
  --dataset_name TEXT         Name of the newly created dataset.
  --dataset_id INTEGER        ID of the dataset to which new items should be
                              imported. If set to '-1', a new dataset will be
                              created
  --images PATH               Directory containing the images to import.
                              [required]
  --annotations PATH          Directory or file containing the annotations to
                              import.  [required]
  --http_retries INTEGER      Number of HTTP retries.  [default: 10]
  --username TEXT             Username for data spree vision platform.
  --password TEXT             Password for data spree vision platform.
  --url TEXT                  URL to the API of the platform.
  --help                      Show this message and exit.
```

### Dataset Export
```
Usage: dlds export [OPTIONS]

Options:
  -o, --output_dir DIRECTORY   Output directory.  [required]
  -i, --id INTEGER             ID of the dataset to download.
  -n, --n_items INTEGER        Number of items to download. Download all
                               items: '-1'  [default: -1]
  --http_retries INTEGER       Number of HTTP retries.  [default: 10]
  --parallel_requests INTEGER  Number of parallel requests.  [default: 16]
  --username TEXT              Username for data spree vision platform.
  --password TEXT              Password for data spree vision platform.
  --url TEXT                   URL to the API of the platform.
  --help                       Show this message and exit.
```

## License
Apache License 2.0