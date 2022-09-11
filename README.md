
# Aim
 
Deploy or delete Kubernetes projects by adding and deleting specific labels to GitLab merge requests.

Add 2 labels to your project repository

- Deploy-K8S
- Deploy-ERR

When you add the "Deploy-K8S" label, runs scripts/deploy.sh bash file.
You can edit it depending on your specific goals.

When you delete the "Deploy-K8S" label, runs scripts/delete.sh bash file.
You can edit it depending on your specific goals.

The results are pushed on Slack or Rocket Chat channels and you can find logs in the "logs" directory.

If any occur error, the "Deploy-K8S" label will be removed and added "Deploy-ERR" label.


# Preparation

## Adding kubeconfig file
Put "kubeconfig" file of your Kubernetes to the project's root directory. The name  of the file must be "kubeconfig"

## Raneme and edit Env file
At first, rename "env" file to  ".env", then edit your values 

## Docker Compose
Install Docker Compose on bastion host machine.

https://docs.docker.com/compose/install/

# Run

```
docker-compose up -d
```

# Stop

```
docker-compose down
```