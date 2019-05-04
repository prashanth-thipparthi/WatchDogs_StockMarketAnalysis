#!bin/bash
echo "running deploy script"
set -e
ls -l
gcloud auth activate-service-account --key-file gcloud_project.json
echo "Login success in gcloud."
docker-credential-gcr configure-docker
docker build -t flask_app .
docker tag flask_app gcr.io/vaulted-zodiac-236605/flask_api_server

echo "docker build done"
docker push gcr.io/vaulted-zodiac-236605/flask_api_server
#kubectl delete deployment.apps/api-deployment
gcloud --quiet config set project "vaulted-zodiac-236605"
gcloud --quiet container clusters get-credentials "standard-cluster-1"
kubectl apply -f deploy.yml

echo "script Complete"
