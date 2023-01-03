# super-app-backend
This is the backend for the super-app where each app will be run as a pipeline

## Running the backend (v-0.1)
1. Infra Setup :\
  i. Create a EC2 Machine and assign full permissions to s3 and rds. Attach SSH, HTTPS anywhere outbound and inboud as well.\
  ii. Create a Aurora MySQL RDS instance and create inbound from the EC2 machine created.\
  iii. Create a bucket on AWS S3 named super-app-data.

2. Update these details in the `environemnt_params.json` present in `deployment/installabes`
3. Login to the EC2 machine
4. Copy the `deployment.sh` file in this machine
5. Run the command `sh deployment.sh development`
