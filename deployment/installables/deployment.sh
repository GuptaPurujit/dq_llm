# Input Pipeline Name
BRANCH_NAME = $1
cd /home
rm -rf deployment
mkdir deployment
cd deployment

# git clone the repo according to Pipeline Name
sh "git clone -b {$BRANCH_NAME} https://github.com/super-app-backend.git"

# place all files in same folder
cp -r super-app-backend/common/rds/* .
cp -r super-app-backend/common/utility_files/* .
cp -r super-app-backend/deployment/environment/environment_params.json .
cp -r super-app-backend/pipeline/tracker/* .

# create zip file
zip -r super-app.zip super-app