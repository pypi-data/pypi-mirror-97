# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phobos',
 'phobos.augs',
 'phobos.grain',
 'phobos.logger',
 'phobos.loss',
 'phobos.metrics',
 'phobos.runner']

package_data = \
{'': ['*']}

install_requires = \
['MedPy==0.4.0',
 'albumentations==0.5.2',
 'numpy==1.18.1',
 'numpydoc>=1.1.0,<2.0.0',
 'polyaxon-sdk==1.5.4',
 'polyaxon==1.5.4',
 'pytorch_lightning>=0.9.0,<0.10.0',
 'rasterio>=1.2.0,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'sphinx-issues>=1.2.0,<2.0.0',
 'sphinx-prompt>=1.3.0,<2.0.0',
 'sphinx_rtd_theme>=0.4.3,<0.5.0',
 'torch==1.7.1',
 'torchvision>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'phobos',
    'version': '0.9.19',
    'description': 'Training utility library and config manager for Granular Machine Vision research',
    'long_description': '===================\nPhobos\n===================\n\n\nUtility package for satellite machine learning training\n\n\n* Free software: MIT license\n* Documentation: docs.granular.ai/phobos.\n\nDependencies\n------------\n\n* polyaxon>=1.5.4\n* poetry\n* twine\n\nFeatures\n--------\n\n* Polyaxon auto-param capture\n* Configuration enforcement and management for translation into Dione environment\n* Precomposed loss functions and metrics\n\n\nTODO\n----\n\n* Shift build logic from cloudbuild to github actions\n\n\nBuild Details\n-------------\n\n* packages are managed using poetry\n* packages poetry maintains pyproject.toml\n* PRs and commits to `develop` branch trigger a google cloudbuild (image: cloudbuild.yaml, docs: cloudbuild_docs.yaml)\n* Dockerfile builds image by exporting poetry dependencies as tmp_requirements.txt and installing them\n\nTests\n-----\n\n>>> make install\n>>> make test-light\n\n\nA GPU machine is requried for test-heavy\n\n>>> make install\n>>> make test-heavy\n\n\nTesting polyaxon functionality requires setting up a kubernetes cluter with polyaxon, skip these steps if cluster exists\n\n* Install gcloud and connect to your gcloud.\n\n* Install kubectl\n\n* Check if ``phobos-dev`` cluster exists or not, if it exists skip next 4 steps\n\n>>> gcloud container clusters list | grep phobos-dev\n\n* Create a ``phobos-dev`` cluster on kubernetes with default pool named as ``polyaxon-core-pool``\n\n>>> gcloud container clusters create phobos-dev --zone=us-central1-c --node-locations=us-central1-c \\\n  --machine-type=e2-standard-2 --num-nodes=1 --node-labels=polyaxon=core-pool\n\n* Connect to the ``phobos-dev`` cluster\n\n>>> gcloud container clusters get-credentials phobos-dev --zone us-central1-c --project granular-ai\n\n* Create ``phobos-test`` node pool\n\n>>> gcloud container node-pools create phobos-test --cluster phobos-dev  --machine-type=n1-highcpu-8 \\\n--disk-size=50GB --node-labels=polyaxon=phobos-test --num-nodes=1   --preemptible \\\n--enable-autoscaling --max-nodes=1 --min-nodes=0\n>>> kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.8.0/nvidia-device-plugin.yml\n>>> kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml\n\n* Deploy ``polyaxon``\n\n>>> kubectl create namespace polyaxon\n>>> helm repo add stable https://charts.helm.sh/stable\n>>> helm install plx-nfs stable/nfs-server-provisioner --namespace=polyaxon\n>>> kubectl apply -f artifacts-pvc.yaml\n>>> pip install -U polyaxon\n>>> polyaxon admin deploy -f polyaxon-config.yaml\n\n* Create a ``phobos-test`` project if it does not exist and init it\n\n>>> polyaxon port-forward -p 8001\n>>> polyaxon project create --name=phobos-test\n>>> polyaxon init -p phobos-test --polyaxonignore\n\n* Test on ``polyaxon``\n\n>>> make test-polyaxon\n\nCheck the experiment url shown after running this command.\nGo to artifacts/code  and click on test.log to see the complete log of tests.\n',
    'author': 'Sagar Verma',
    'author_email': 'sagar@granular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/granularai/phobos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
