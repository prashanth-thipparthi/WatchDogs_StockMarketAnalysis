#!bin/bash
echo "running deploy script"
set -e
ls -l
gcloud auth activate-service-account --key-file gcloud_project.json
echo "Login success in gcloud."
docker-credential-gcr configure-docker
docker build -t dbpopulator .
docker tag dbpopulator gcr.io/vaulted-zodiac-236605/dbpopulator

echo "docker build done"
docker push gcr.io/vaulted-zodiac-236605/dbpopulator
gcloud --quiet config set project "vaulted-zodiac-236605"
gcloud --quiet config set compute/zone "us-central1-a"
gcloud --quiet config set container/cluster "standard-cluster-1"
gcloud --quiet container clusters get-credentials "standard-cluster-1"
kubectl delete pod --ignore-not-found=true dbpopulator-pod
kubectl apply -f pod.yml

echo "script Complete"
