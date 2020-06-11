# Endpoints

* `/auth`
  * Request body format
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  * POST - Register new user
  * PUT - Log a user in
* `/auth/:uid`
  * DELETE - Delete a user (ONLY IF JWT IDENTITY IS THE SAME AS THE UID)