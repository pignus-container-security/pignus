# Create Cluster

Creates a cluster on the Pignus Api.

**URL** : `/cluster`

**Method** : `POST`

**Auth required** : YES

**Data**
    Query Params: `create=True`
    Body
    ```
    {
        "name:" "The Cluster Pretty Name",
        "slug_name": "the-cluster-slug-name"
    }
    ```

## Success Response

**Code** : `201 OK`

**Content** : 
    ```
    {
        "data"
    }
    ```
