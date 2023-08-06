===================
Phobos
===================


Utility package for satellite machine learning training


* Free software: MIT license
* Documentation: docs.granular.ai/phobos.

Dependencies
------------

* polyaxon>=1.5.4
* poetry
* twine

Features
--------

* Polyaxon auto-param capture
* Configuration enforcement and management for translation into Dione environment
* Precomposed loss functions and metrics


TODO
----

* Shift build logic from cloudbuild to github actions


Build Details
-------------

* packages are managed using poetry
* packages poetry maintains pyproject.toml
* PRs and commits to `develop` branch trigger a google cloudbuild (image: cloudbuild.yaml, docs: cloudbuild_docs.yaml)
* Dockerfile builds image by exporting poetry dependencies as tmp_requirements.txt and installing them

Tests
-----

>>> make install
>>> make test-light


A GPU machine is requried for test-heavy

>>> make install
>>> make test-heavy


Testing polyaxon functionality requires setting up a kubernetes cluter with polyaxon, skip these steps if cluster exists

* Install gcloud and connect to your gcloud.

* Install kubectl

* Check if ``phobos-dev`` cluster exists or not, if it exists skip next 4 steps

>>> gcloud container clusters list | grep phobos-dev

* Create a ``phobos-dev`` cluster on kubernetes with default pool named as ``polyaxon-core-pool``

>>> gcloud container clusters create phobos-dev --zone=us-central1-c --node-locations=us-central1-c \
  --machine-type=e2-standard-2 --num-nodes=1 --node-labels=polyaxon=core-pool

* Connect to the ``phobos-dev`` cluster

>>> gcloud container clusters get-credentials phobos-dev --zone us-central1-c --project granular-ai

* Create ``phobos-test`` node pool

>>> gcloud container node-pools create phobos-test --cluster phobos-dev  --machine-type=n1-highcpu-8 \
--disk-size=50GB --node-labels=polyaxon=phobos-test --num-nodes=1   --preemptible \
--enable-autoscaling --max-nodes=1 --min-nodes=0
>>> kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.8.0/nvidia-device-plugin.yml
>>> kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml

* Deploy ``polyaxon``

>>> kubectl create namespace polyaxon
>>> helm repo add stable https://charts.helm.sh/stable
>>> helm install plx-nfs stable/nfs-server-provisioner --namespace=polyaxon
>>> kubectl apply -f artifacts-pvc.yaml
>>> pip install -U polyaxon
>>> polyaxon admin deploy -f polyaxon-config.yaml

* Create a ``phobos-test`` project if it does not exist and init it

>>> polyaxon port-forward -p 8001
>>> polyaxon project create --name=phobos-test
>>> polyaxon init -p phobos-test --polyaxonignore

* Test on ``polyaxon``

>>> make test-polyaxon

Check the experiment url shown after running this command.
Go to artifacts/code  and click on test.log to see the complete log of tests.
