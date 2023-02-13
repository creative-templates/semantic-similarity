# Schema

### Schema for dataset

| sentence 1 | sentence 2 | label  |
| :--------: | :--------: | :----: |
|   string   |   string   | string |

The label will be either "similar" or "not similar".

The SNLI dataset contains labels "neutral", "contradiction", and "entailment".

### Schema for application

| id  | title  | description | tokens | label  | created_at | updated_at |
| :-: | :----: | :---------: | :----: | :----: | :--------: | :--------: |
| id  | string |   string    | string | string |  datetime  |  datetime  |

We will probably need to add an schema like this for the application. The created_at and updated_at fields are automatically added by the database when we use MongoDB anyways. The id field is automatically added by MongoDB as well. The tokens field will be a list of strings. The label field will be a string (target).
