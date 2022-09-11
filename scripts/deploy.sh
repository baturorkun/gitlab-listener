#!/usr/bin/env bash
set -xo pipefail

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
        --iid)
            IID=$VALUE
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
exec > /root/logs/gitlab-listener/deploy-$(date '+%Y-%m-%d-%H_%M_%S')-$PROJECT 2>&1

BASE_PATH=$(pwd)

kubectl create ns "$PROJECT"

echo "Adding deployment codes here..."

