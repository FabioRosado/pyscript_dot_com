# API ideas

## Get

- `/datastore/{key}`

- returns dict in the form:
    
    ```json
    {
    "key": "value"
    }
    ```

## Post
    
- `/datastore`

- Request body:
    
    ```json
    {
    "key": "value"
    }
    ```

    - Response:
    
    ```json
    {
    "key": "value"
    }
    ```

## Put

- `/datastore/{key}`
- Request body:
    
    ```json
    {
    "key": "value"
    }
    ```

    - Response:
    
    ```json
    {
    "key": "value"
    }
    ```

## Delete

- `/datastore/{key}`
- Response:
    
    ```json
    {
    "key": "value"
    }
    ```

## list
- `/datastore`
- Response:
    
    ```json
    {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
    }
    ```