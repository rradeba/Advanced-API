Module 16 Mini-Project: E-commerce API CI/CD
The e-commerce project, developed in Module 13, requires a streamlined Continuous Integration and Continuous Deployment (CI/CD) pipeline for optimal performance. This pipeline should automate the process of building, testing, and deploying the application to Render, a cloud platform. Key components include setting up a robust CI/CD workflow using GitHub Actions, configuring a PostgreSQL database hosted on Render for the Flask API, and implementing unit tests using unittest and pytest for application reliability. The project will emphasize documentation and knowledge sharing to ensure efficient collaboration and project management. 🛠️🔧🚀🌟

Project requirements
Utilize the e-commerce project generated in Module 13:
Use the e-commerce project created in Module 13 as the basis for this CI/CD project.
Send the project to the GitHub repository (if haven’t already):
Push the e-commerce project to a GitHub repository to facilitate version control and collaboration.
Implement a Continuous Integration (CI) flow of build and test in GitHub Actions:
Create a main.yml file within the .github/workflows directory to define the CI workflow.
Configure the workflow to automatically trigger code pushes to the main branch.
Use GitHub Actions to build the project and run unit tests using unittest and pytest.
Ensure that the workflow fails if any tests fail, preventing the deployment of faulty code.
Deploy a PostgreSQL database on Render and link it with the Flask API:
Set up a PostgreSQL database service on Render to host the application's database.
Modify the Flask API code to use the psycopg2 library to connect to the Render-hosted PostgreSQL database.
Configure the database connection settings in the Flask API to establish a successful connection.
Implement a Continuous Deployment (CD) flow in GitHub Actions with deployment to Render:
Extend the existing GitHub Actions workflow to include a deployment stage.
Define deployment jobs to deploy the application to Render.
Ensure that the deployment only occurs after the CI tests have passed successfully.
Validate the API's functionality through Swagger-generated documentation:
Integrate the Swagger documentation into the Flask API to provide a comprehensive overview of the API's endpoints and functionality.
Ensure that the Swagger documentation is up-to-date and reflects the current state of the API.
Use the Swagger UI to interact with the API and verify its functionality, including testing various endpoints and verifying responses.
GitHub Repository:
Maintain a clean and interactive README.md file in the GitHub repository, providing clear instructions on how to run the application and explanations of its features.
Include a link to the GitHub repository in the project documentation.
Submission
Upon completing the project, submit your code, including all source code files, and the README.md file in your GitHub repository to your instructor or designated platform.
Project Tips
Database Connection Configuration:
Install the psycopg2-binary and psycopg2 libraries within the requirements.txt file to establish a PostgreSQL database connection.
Ensure that libpq-dev is installed to resolve any potential dependency issues.
Pipeline Configuration:
Utilize multiple jobs within the GitHub Actions workflow to achieve a better understanding of the CI/CD process.
Create a .github/workflows directory and a main.yml file to define the CI/CD workflow.
Integration Continuous Testing:
Implement unit tests for the Flask API using the unittest and pytest libraries.
Ensure that the CI workflow includes a test step that runs these unit tests to validate the functionality of the e-commerce project.
Deploy Databases in Render:
Leverage Render's built-in PostgreSQL database service to host the application's database.
Configure the database connection settings in the Flask API to connect to the Render-hosted PostgreSQL database.
Install Gunicorn for Production Deployment
Install the gunicorn library within the requirements.txt file to facilitate the deployment of the Flask API to Render.
Project Rubric: Module 16 Mini Project Rubric

NOTE: On completion of this project, please reach out to your instructor letting them know you have finished the coursework. They will check to ensure that all of your assignments have passing marks and they may provide you with a list of required resubmissions that will need to be resubmitted. Once that is done and your codewars account has 400 points or more, you instructor will provide next steps!
