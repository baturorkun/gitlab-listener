import json
import subprocess
import os
import requests


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def exists_deployK8S_label(labels):
        for label in labels:
            if label["title"] == "Deploy-K8S":
                return True
        else:
            return False

    @staticmethod
    def exists_deployERR_label(labels):
        for label in labels:
            if label["title"] == "Deploy-ERR":
                return True
        else:
            return False

    @staticmethod
    def findOwner(dict):
        sent = False
        if "assignees" in dict:
            channel = dict["assignees"][0]["username"]
            sent = channel
        elif "last_commit" in dict:
            channel = dict["last_commit"]["author"]["email"]
            sent = channel
        return sent

    @staticmethod
    def sendMessage(dict, message):

        notifMethod = os.environ["NOTIFICATION_METHOD"]
        channel = Utils.findOwner(dict)

        if notifMethod == "rocketchat":
            Utils.sendRocketChat("@" + channel, message)
        elif notifMethod == "slack":
            Utils.sendSlackNotif("@" + channel, message)
        else:
            print("!!!!!!! Error !!!!!!! Invalid notification method:", notifMethod)

    @staticmethod
    def sendRocketChat(channel, message):

        rocketChatURL = os.environ["ROCKETCHAT_URL"]

        data = {"text": message, 'channel': channel}
        r = requests.post(url=rocketChatURL,
                          data=json.dumps(data), headers={'Content-Type': 'application/json'})
        return json.dumps({'status': r.status_code})

    @staticmethod
    def sendSlackNotif(channel, message):

        slackHookUrl = os.environ["SLACK_HOOK_URL"]
        token = os.environ["ROCKETCHAT_TOKEN"]
        userid = os.environ["ROCKETCHAT_USERID"]
        headers = {
            "X-Auth-Token:" + token,
            "X-User-Id:" + userid,
            "Content-type:application/json"
        }

        data = {"text": message, 'channel': channel}
        r = requests.post(url=slackHookUrl + "/api/v1/chat.postMessage",
                          data=json.dumps(data), headers=headers)
        return json.dumps({'status': r.status_code})

    @staticmethod
    def gitlabUpdateLabelsForFail(dict):
        gitlab_token = os.environ['GITLAB_TOKEN']
        gitlab_url = os.environ["GITLAB_URL"]
        gitlab_project_id = os.environ["GITLAB_PROJECT_ID"]

        iid = dict["object_attributes"]["iid"]
        cmd = [
            "curl",
            "--request",
            "PUT",
            "--header",
            f"PRIVATE-TOKEN: {gitlab_token}",
            "--data",
            "'add_labels=Deploy-ERR'",
            "'remove_labels=Deploy-OCP'"
            f"{gitlab_url}/api/v4/projects/{gitlab_project_id}/merge_requests/{iid}"
        ]

        cmd = subprocess.run(cmd, capture_output=True, text=True)
        if cmd.stderr != "":
            print("!!!!!!! Error !!!!!!!", cmd.stderr, cmd.stdout)
        else:
            print(">>> Output <<<", cmd.stdout)
