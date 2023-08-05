# properly-model-python

Contains the models used by multiple systems to describe a property, by using the common models the shape
of the data is consistent

## Quick Run

1. Setup the environment for development by calling `source ./setup.sh`
2. Make your changes to the code
3. Increase the `major` or `minor` values in if appropriate [setup.py](https://github.com/GoProperly/properly-model-python/blob/master/setup.py#L8)
4. Run `./test.sh` to run automated tests.

## Uploading the Package

To upload package: 
Merge changes to master branch and push. Package is uploaded automatically to pypi on a merge of a branch to master. 

(Note Source: https://packaging.python.org/tutorials/packaging-projects/ )


## Installing the Package 

`pip install properly-model-python`

or

`pip install --no-cache-dir --upgrade properly-model-python`


## Updating the Models
* This project makes use of [Swagger API Models](https://app.swaggerhub.com/)
* In Swagger, use the [swagger.yml](./properly_model_python/models/swagger.yml) to recreate the models.
* Configure the export settings:
    * Click the `Export` button in the top right.
    * Click `Codegen Options`.
    * Go to the `Servers` > `python-flask` section.
    * Set the `packageName` option to `properly_model_python`.
    * Click the `Save Options` button. 
* Export the models:
    * Click the `Export` button in the top right.
    * Select `Server Stub` > `python-flask`.
    * Save the zip file from Swagger.
* Copy the model files into the project:
    * Unzip the downloaded file.
    * From the unzipped content, copy to this project the following files: 
    ```
    ./python-flask-server-generated/properly_model_python/models/model_property.py
    ./python-flask-server-generated/properly_model_python/models/sold_property.py
    ./python-flask-server-generated/properly_model_python/models/listing_property.py
    ./python-flask-server-generated/properly_model_python/models/room.py
    ./python-flask-server-generated/properly_model_python/models/image.py
    ./python-flask-server-generated/properly_model_python/models/custom_annotation.py

    ./python-flask-server-generated/properly_model_python/models/swagger.yml
    ```
    * **Do not update** the following files because we have put custom code in them:
    ```
    ./python-flask-server-generated/properly_model_python/models/base_model_.py
    ```
    * Checking the git diff, you'll notice that 3 imports (CustomAnnotation, Image, Room) were removed in the generated model_property.py, listing_property.py, and sold_property.py files.  Modify those generated files to add them back.
