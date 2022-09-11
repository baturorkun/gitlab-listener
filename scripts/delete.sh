#!/usr/bin/env bash
#set -xo pipefail
### ENVs
echo "Checking parameters..."

while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --project)
            PROJECT=$VALUE
            ;;
        --channel)
            CHANNEL=$VALUE
            ;;
        --debug)
            DEBUG=$VALUE
            ;;
        *)
            echo "<ERROR> Unknown parameter [ $PARAM ] </ERROR>"
            usage
            exit 1
            ;;
    esac
    shift
done
exec > /root/gitlab-listener/logs/delete-$(date '+%Y-%m-%d-%H_%M_%S')-$PROJECT 2>&1

BASE_PATH=$(pwd)


if [[ "$PROJECT" == "default" ]]; then
    echo "<ERROR> Active project is default </ERROR>"
    exit
fi

kubectl get project $PROJECT

if [[ "$?" != "0" ]]; then
    echo "<WARNING> $PROJECT  is not exists! </WARNING>"
    exit
fi

kubectl delete ns "$PROJECT"
