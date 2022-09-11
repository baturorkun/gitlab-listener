import tornado.ioloop
import tornado.web
import json
import sys
import subprocess
from pprint import pprint
from utils import Utils

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("************************************************************************\n")
        print("GET >>> %r %s" % (self.request, self.request.body.decode()))

    def post(self):
        data = self.request.body.decode()
        dict = json.loads(data)

        print("************************************************************************\n")
        print(dict)
        print("************************************************************************\n")

        project = dict["object_attributes"]["source_branch"].split("-")[0]
        print(">>>> Project / Source Branch :", project)

        channel = Utils.findOwner(dict)

        print(dict["object_attributes"]["title"])

        if Utils.exists_deployERR_label(dict["labels"]):
            print("<WARNING> There is Deploy-ERR label </WARNING>")
            print("Ignore & Exit")
            return

        if not channel:
            print("<ERROR>There is not any owner for this MR</ERROR>")
            Utils.sendRocketChat("@batur.orkun", "<ERROR>There is not any owner for this MR</ERROR>")
            return

        if  dict["object_attributes"]["state"] in ("closed", "merged"):
            action = dict["object_attributes"]["state"]
            mr_url = dict["object_attributes"]["url"]
            print(f"----------- Starting DELETE Project as Action: {action} -------------")
            Utils.sendMessage(dict, f"{project} Merge Request was {action}. {mr_url}")

            self.terminateProject(project, channel)

        elif Utils.exists_deployK8S_label(dict["labels"]):
            print(f"----------- Starting ADD Project as Action: {action} -------------")
            self.deployProject(project, channel)

        else:
            print("Action >>> Deleted LABEL!")
            print("----------- Starting DELETE Project as Deleting LABEL -------------")
            cmd = subprocess.run(["bash", "./scripts/delete.sh", "--project=" + project, "--channel=" + channel], capture_output=True, text=True)
            if cmd.stderr != "":
                print("!!!!!!! Error Begin !!!!!!!")
                print(cmd.stderr)
                print("!!!!!!! Error End !!!!!!!")
            print("<<<<<<<< Output Begin >>>>>>>>")
            print(cmd.stdout)
            print("<<<<<<<< Output End >>>>>>>>")


    def terminateProject(self, project, channel):
        print("Added any Label!")
        print("+++++++++++ Starting Deployment ++++++++++")
        Utils.sendMessage(dict, f"Started checking resources for OCP Deploying {project}")
        self.terminateProject(PROJECT, channel)

    def deployProject(self, project, channel ):
        print("Added DEPLOY label!")
        cmd = subprocess.run(["bash", "./scripts/delete.sh", "--project=" + project, "--channel=" + channel],
                             capture_output=True, text=True)
        if cmd.stderr != "":
            print("!!!!!!! Error Begin !!!!!!!")
            print(cmd.stderr)
            print("!!!!!!! Error End !!!!!!!")
        print("<<<<<<<< Output Begin >>>>>>>>")
        print(cmd.stdout)
        print("<<<<<<<< Output End >>>>>>>>")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    print("Started listening...:8888\n")
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()