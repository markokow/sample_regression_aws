# Sample Machine Learning Regression Application Prototype

## Project Objective

The objective of this repository is to provide a scalable and efficient machine learning regression API application designed for predicting sales for a business.

It demonstrates the end-to-end process of deploying a machine learning model, from training using Scikit-Learn's Linear models to implementing a FastAPI-based web service.

The application is containerized with Docker, offering deployment flexibility across platforms like Heroku and AWS ECS.

Additionally, the repository includes a CI/CD component using GitHub Workflows, which automates the process of testing, building, and deploying the application.

This prototype serves as a practical example of integrating machine learning models into production environments, enabling real-time sales predictions through a RESTful API interface.

## Background

This repository contains the Rossmann Sales Prediction API, which is designed to forecast the sales for Rossmann stores, Germany's second-largest drug store chain. The API leverages historical sales data from 1,115 Rossmann stores, taking into account the impact of temporary store closures during refurbishment.

## Model and Implementation Overview

The sales prediction model in this API is trained using Scikit-Learn's Linear Models, including Linear Regression, Ridge, Lasso, and Elastic Net. Among these models, Ridge has been selected as the final model for its superior performance and is used in the deployment of the API.

The API is implemented using FastAPI, a high-performance web framework for building APIs with Python. FastAPI enables efficient request handling and real-time predictions, ensuring a seamless user experience.

And lastly the API is containerized using Docker, and deployed in Heroku. Prediction sales can be accessed at https://sample-regression-9f9bc0ae0810.herokuapp.com/docs

In addition, this app is also deployed in AWS Cloud infrastructure via Terraform (which can be found in `aws_infra/` folder). Thus an alternative deployment can be accessed at https://fastapi-alb-344459632.ap-southeast-1.elb.amazonaws.com/docs (**NOTE: It is still WIP**)

CI/CD is also implemented via Github workflow to automate the testing, building and deployment of the application. This is to ensure reliable and efficient code delivery to production

## Basic Feature

The core feature of this API is its RESTful architecture, allowing users to predict sales based on a set of input parameters. The API provides a single endpoint, `/predict`, which accepts a POST request. The request body should include the following fields:

| Field         | Type    | Input                                                           |
| ------------- | ------- | --------------------------------------------------------------- |
| Store         | Integer | Store entry is within the store.csv information                 |
| DayOfWeek     | Integer | Between 1 to 7, corresponding to Sunday to Saturday             |
| Date          | String  | Must be converted to date time format                           |
| Customers     | Integer | Must not be negative                                            |
| Open          | Integer | 0 = closed, 1 = open                                            |
| Promo         | Integer | 0 = no, 1 = yes                                                 |
| StateHoliday  | String  | a = public holiday, b = Easter holiday, c = Christmas, 0 = None |
| SchoolHoliday | Integer | 0 = no, 1 = yes                                                 |

Upon receiving the request, the API will respond with a JSON object that contains the predicted sales value. The sales value will be represented as a float and will be included in the `sales` field of the response JSON. Here is an example of the expected request and response JSON objects:

**Request JSON:**

```json
{
  "Store": 1111,
  "DayOfWeek": 4,
  "Date": "2014-07-10",
  "Customers": 410,
  "Open": 1,
  "Promo": 0,
  "StateHoliday": "0",
  "SchoolHoliday": 1
}
```

**Here is the sample output**

```json
{
  "sales": 3589.86
}
```

To see the sales prediction in action, you can use the following code snippet:

```python
import requests

# via Heroku
r = requests.post('https://sample-regression-9f9bc0ae0810.herokuapp.com/predict', json={
  "Store": 1111,
  "DayOfWeek": 4,
  "Date": "2014-07-10",
  "Customers": 410,
  "Open": 1,
  "Promo": 0,
  "StateHoliday": "0",
  "SchoolHoliday": 1
})

print(r.json())

# for AWS one can use https://fastapi-alb-344459632.ap-southeast-1.elb.amazonaws.com/predict instead
```

For more information about the model and its implementation details, please visit this [presentation](https://drive.google.com/file/d/1EqAc-g6hRHoy80VoQF-IHpJRKvz1yQC9/view) for the project overview
