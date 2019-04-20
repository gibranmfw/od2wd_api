# od2wd_api
Part of OD2WD project

## Development Guide

### How to set up your machine

1. Setup and activate your Python virtual environment using pipenv.
2. Still in the directory where you've cloned this repo, install all its dependencies.

    ```bash
    pipenv sync
    ```

3. Create word2vec model and elasticsearch index for the first time

    ```bash
    flask setup_all
    ```

4. Run the app using

    ```bash
    flask run
    ```

5. Update index using

    ```bash
    flask update_index [index_name]
    ```
