FROM python:3.9.10-slim

RUN apt update

RUN apt install jq curl -y

RUN pip install tornado
RUn pip install requests

WORKDIR /root/gitlab-listener
COPY . .

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl

RUN curl -LO https://github.com/ahmetb/kubectx/releases/download/v0.9.4/kubens
RUN chmod +x ./kubens
RUN mv ./kubens /usr/local/bin/kubens

RUN chmod 777 /usr/local/bin/*

RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && \
    chmod 700 get_helm.sh && \
    ./get_helm.sh

EXPOSE 8888

ENTRYPOINT ["python3", "-u", "webserver.py"]
