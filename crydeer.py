#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

from sys import argv
import sys
import os
sys.path.append(os.path.abspath(".."))
import CryDeer
from CryDeer.controller import Controller
import click


controller = Controller()


@click.group(help="包裹查询助手")
def main():
    pass


@main.command("add", help="新增包裹")
@click.argument("number")
@click.option("-d", "--description", help="包裹描述")
def add_package(number, description):
    controller.new_item(number, description)


@main.command("remove", help="新增包裹")
@click.argument("number")
@click.option("-d", "--description", help="包裹描述")
def remove_package(number, description):
    controller.delete_item(number)


@main.command("list", help="显示所有包裹信息")
def list_packages(number):
    controller.list()


@main.command("detail", help="显示包裹详细信息")
@click.argument("number")
def show_detail(number):
    controller.show_info(number)


@main.command("update", help="更新包裹信息")
def update_packages():
    controller.update_all()


if __name__ == "__main__":
    main()
