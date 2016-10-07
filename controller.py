#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import requests
import json
from database import Database
from prettytable import PrettyTable

state = [
    "在途",
    "揽件",
    "疑难",
    "签收",
    "退签",
    "派件",
    "退回"
]

class Controller():

    db = Database()
    session = requests.Session()

    def __init__(self):
        pass

    def list(self, nu="all"):
        query = self.db.get_item_query()
        ptable = PrettyTable(["运单号", "描述", "最后一次更新时间", "最后一次更新信息"])
        ptable.sort_key("最后一次更新时间")
        ptable.reversesort = True
        for item in query:
            ptable.add_row([item.nu, item.description, item.lastUpdateTime, item.lastUpdateInfo])
        print(ptable)

    def get_com_code(self, nu):
        url = "http://www.kuaidi100.com/autonumber/autoComNum?text=" + nu
        data = self.session.get(url).text
        jsonData = json.loads(data)
        return jsonData["auto"][0]["comCode"]

    def new_item(self, nu, des="None"):
        if not self.db.has_item(nu):
            com_code = self.get_com_code(nu)
            url = "http://www.kuaidi100.com/query?type=" + com_code + "&postid=" + nu;
            data = self.session.get(url).text
            jsonData = json.loads(data)
            status = jsonData["status"]
            state_code = int(jsonData["state"])
            data = jsonData["data"]
            for info in data:
                time = info["time"]
                context = info["context"]
                time = time[:10] + " " + time[11:14] + time[15:]
                self.db.insert_info(self.db.get_new_info_id(), nu, time, context)
            last_time = data[-1]["time"]
            last_time = last_time[:10] + " " + last_time[11:14] + last_time[15:]
            last_context = data[-1]["context"]
            self.db.insert_item(self.db.get_new_item_id(), nu, des, com_code, state_code, status, last_time, last_context)
        else:
            print("已存在")

    def delete_item(self, nu):
        self.db.delete_item(nu)
        self.db.delete_info(nu)

    def update_all(self):
        for nu in self.db.get_all_nu():
            url = "http://www.kuaidi100.com/query?type=" + self.get_com_code(nu) + "&postid=" + nu;
            data = self.session.get(url).text
            jsonData = json.loads(data)
            status = jsonData["status"]
            state_code = int(jsonData["state"])
            data = jsonData["data"]
            for info in data:
                time = info["time"]
                context = info["context"]
                time = time[:10] + " " + time[11:14] + time[15:]
                self.db.insert_info(self.db.get_new_info_id(), nu, time, context)
            last_time = data[-1]["time"]
            last_time = last_time[:10] + " " + last_time[11:14] + last_time[15:]
            last_context = data[-1]["context"]
            self.db.update_item(nu, state_code, status, last_time, last_context)

if __name__ == "__main__":
    control = Controller()
    control.new_item("882967786411263996")
    control.new_item("610100445741")
    control.new_item("882909215041897319")
    control.update_all()
