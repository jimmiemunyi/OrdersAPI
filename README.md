# Comprehensive Guide to Orders API

[![codecov](https://codecov.io/gh/jimmiemunyi/OrdersAPI/graph/badge.svg?token=7LPIS8SCJX)](https://codecov.io/gh/jimmiemunyi/OrdersAPI)

## Introduction

Welcome to the repository for the Orders API application. This platform is accessible via <a href="https://jimmie-orders-api-e6327f2ac0f9.herokuapp.com/" target="_blank"> this link </a>. In addition to its primary functionality, this application also boasts a robust API layer. Detailed information about the supported endpoints can be found <a href="https://jimmie-orders-api-e6327f2ac0f9.herokuapp.com/apidocs" target="_blank">here </a>.

This guide provides an in-depth overview of both the application's features and the underlying codebase.

## Technology Stack

The Orders API application is developed using the [Flask](https://flask.palletsprojects.com/en/2.3.x/) framework and Python Programming Language (version 3.10.12). It also utilizes several Flask extensions, including:

- `flassger`: This extension is used for constructing the Swagger documentation of the API.
- `flask-migrate`: This tool manages database migration functionality.
- `flask-sqlalchemy`: This ORM (Object Relational Mapper) interfaces with the database to facilitate read/write operations.
- `flask-wtf`: This extension aids in the creation and management of WTF Forms.

The application is hosted on [Heroku](https://www.heroku.com/), a popular Platform-as-a-Service (PaaS) provider.

## Database

The Orders API application utilizes a [PostgreSQL](https://www.postgresql.org/) database for data storage. PostgreSQL was selected as the database for the OrdersAPI due to its superior capabilities in areas such as:

- Data modeling
- ACID compliance
- Scalability
- Data integrity

In addition, PostgreSQL's support for advanced data types, extensions, and security features, coupled with a vibrant ecosystem and extensive community support, make it an excellent choice for managing structured data. This is particularly true for Python and Flask-based applications like OrdersAPI.

Before running the application, the databases must be properly set up. Detailed instructions for this process can be found in the [Setup](#setup) section.

The databases used in this application consist of two tables: `Customers` and `Orders`. The structure of these tables is as follows:

### Customers

| Field     | Description                      |
| --------- | -------------------------------- |
| `id`      | The Primary Key of the table     |
| `name`    | The name of the customer         |
| `email`   | The email of the customer        |
| `contact` | The phone number of the customer |

### Orders

| Field         | Description                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `id`          | The Primary Key of the table                                                                                                 |
| `customer_id` | A foreign key linking to the `Customers` table                                                                               |
| `item`        | Details of the item being ordered                                                                                            |
| `amount`      | The price of the item being ordered                                                                                          |
| `time`        | The timestamp when the order was made                                                                                        |
| `updated`     | The timestamp when the order was updated. If the order has not been updated, this value will be the same as the `time` field |

## Functionality from External Services Provides

The application integrates with several external APIs to provide unique functionality and ensure smooth operation. These are:

### Google Open ID Connect (OIDC)

This service is used for its secure and user-friendly authentication, single sign-on (SSO) capabilities, industry-standard protocols, and ease of integration. It enhances user security and convenience while reducing the complexity of authentication in the application.

**Key Points:**
- The application does not store any login details.
- Once a user is authenticated, we extract the available details from Google and store them in the `Customers` table.
- In some cases, the contact information may not be retrieved from the Google profile as this depends on whether the user has chosen to share their primary contact publicly.
- If the contact detail cannot be extracted, the customer will have a default value of `NULL` in the contact field. They will then be required to update it manually before making an order.

### Africastalking SMS API

This API is used to send confirmation texts to customers once they place an order.

**Key Points:**
- This functionality is currently in sandbox mode.
- To receive the confirmation text, you must have a running Simulator in Africastalking's developer sandbox.


## Continuous Integration and Continuous Deployment (CI-CD)

The application uses a robust DevOps pipeline to ensure high-quality code and seamless deployments. The key components of this pipeline are:

### Automated Testing with pytest

We use `pytest` to write and run our tests.

To execute the tests and generate a coverage report, use the following command in your terminal:

```bash
pytest --cov=backend
```

This command runs all the tests in the `backend` directory and calculates the code coverage, i.e., the percentage of your code covered by the tests.

### CI/CD with GitHub Actions and Heroku

We use GitHub Actions for our CI/CD pipeline. This service allows us to automate workflows, including running tests and deploying our application.

Here's how it works:

1. When you push changes to your repository, GitHub Actions triggers the CI/CD workflow.
2. It starts by running the automated tests using `pytest`.
3. If the tests pass successfully, the workflow proceeds to the deployment stage.
4. The application is then deployed to Heroku, a cloud platform that lets you build, deliver, monitor, and scale apps.

This setup ensures that we only deploy code that has passed all tests, reducing the chances of introducing bugs into the production environment.

# Environment Variables

For the OrdersAPI application, several environment variables need to be set up to run the application offline. These include API keys for Google OICD, Africastalking, and details for connecting to the Postgres database.

## Setting Up Your Environment Variables

Here's a brief description of each variable:

- **SECRET_KEY**: This is used by Flask for functionality like forms security.
- **CONFIG_MODE**: This tells Flask what environment we are running on. The possible values are: `development`, `testing`, and `production`.
- **DEVELOPMENT_DATABASE_URL**: This tells Flask where the database to be used in the development environment is located.
- **PRODUCTION_DATABASE_URL**: This tells Flask where the database to be used in the production environment is located.
 
- **OAUTH2_CLIENT_ID**, **OAUTH2_CLIENT_SECRET**, **OAUTH2_META_URL**: This are required for the Google OICD login in functionality and can be obtained from the Google Cloud API page.
- **AFRICASTALKING_USERNAME**, **AFRICASTALKING_API_KEY**, **AFRICASTALKING_SENDER_ID**: This is used to enable communication features in the application.

To set these up, follow these steps:

1. Copy the sample environment file provided in the repository.
2. Replace the placeholders with your actual values for each of the above variables.
3. Save this file and ensure it is in your `.gitignore` to prevent it from being tracked by Git.

```bash
cp .env.sample .env
```

After running the above command, open the `.env` file and replace the placeholders with your actual values.

<hr>

# Future Additions

The OrdersAPI is a robust and functional application, but as with any software, there's always room for improvement and expansion. The developers have identified several areas that could be enhanced in future iterations of the application.

## Super-Admin Functionality

One significant addition would be the implementation of super-admin functionality. This feature would allow a super-admin to view all orders and customers and perform various operations on them. It would provide an additional layer of control and oversight within the application.

## Improved UI/UX

While the current user interface and user experience are functional, there's always room for improvement. Future updates could include a more intuitive layout, better navigation, and improved aesthetics to make the application more user-friendly and visually appealing.

## Additional Login Providers

Currently, the application only supports login via Google. In future iterations, it would be beneficial to add more login providers. This would offer users more flexibility and convenience when accessing the application. Potential additions could include other popular OAuth providers like Facebook, Twitter, or even email-based authentication.

## Moving from SMS sandbox

Currently, the application's order confirmation texting service is in sandbox mode and requires the user to launch a simulator with their contact details in order to receive the confirmation texts. In future iterations, this functionality will move to production mode and the users will be able to receive the confirmation texts on their personal mobile phones.


<hr>

# Setup

Follow the steps below to set up the OrdersAPI on your local machine.

## Step 1: Clone the Repository

First, clone the code from GitHub. The repository is located at `github.com/jimmiemunyi/OrdersAPI`. You can clone it using the following command:

```bash
git clone https://github.com/jimmiemunyi/OrdersAPI.git
```

## Step 2: Create a Conda Environment

Next, create a conda environment named `orders-api` with Python version 3.10.12. Use the following command to do this:

```bash
conda create -n orders-api python=3.10.12
```

## Step 3: Install Dependencies

Activate your new environment and install the necessary dependencies from the provided `requirements.txt` file:

```bash
conda activate orders-api
pip install -r requirements.txt
```

## Step 4: Create .env File

Create a `.env` file in the root directory of the project. This file should match the `.env.sample` file provided in the repository. Refer to earlier sections of the documentation for more details on how to configure this file.

## Step 5: Set Up the Database

Finally, set up the database by running the following commands:

```bash
sudo su - postgres
psql
```

Then, within the `psql` interface, run the following SQL commands:

```sql
CREATE USER testuser WITH PASSWORD 'testpass';
CREATE DATABASE orders_db WITH OWNER testuser ENCODING='UTF8';
CREATE DATABASE orders_api_db_test WITH OWNER testuser ENCODING='UTF8';
```

After completing these steps, you should have a fully functional local development environment for the OrdersAPI.
