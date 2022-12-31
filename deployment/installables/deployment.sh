cd /home/ec2-user
rm -rf deployment
mkdir deployment
cd deployment

# git clone the repo according to Branch Name
git clone -b $1 https://github.com/GuptaPurujit/super-app-backend.git

# place all files in same folder
cp -r super-app-backend/common/rds/* .
cp -r super-app-backend/common/utility_files/* .
cp -r super-app-backend/deployment/environment/environment_params.json .
cp -r super-app-backend/pipelines/* .

# create zip file
rm -rf super-app-backend
zip -r super-app.zip .

# copy zip to target location for lambda to be triggered and update relevant pipeline lamdba
aws s3 cp super-app.zip s3://super-app-data/$1/
