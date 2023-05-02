#importing library
import os
import sys
import subprocess
from time import sleep

def initansible():
    count = int(input("\nHow many containers do you wanna create? "))
    print()
    name = input("Write down a name of your containers => ")
    print()
    with open(f"file.tmp", "wb") as f:
        for i in range(1, count+1):
            subprocess.run(['docker', 'run', '-itd', f'--name={name}_{i}', 'managed'], stdout=subprocess.PIPE)
            subprocess.check_call(['docker', 'inspect', '-f', '{{ .NetworkSettings.IPAddress }}', f'{name}_{i}'], stdout=f)
            print(i); sleep(0.3); os.system('clear')
        print(f"Succesfully created {count} containers\n")

def delete_containers():
    count = int(input("\nHow many containers do you wanna delete? "))
    print()
    name = input("Write down a name of your containers => ")
    print()
    for i in range(1, count+1):
        subprocess.run(['docker', 'rm', '-f', f'{name}_{i}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(i); sleep(0.3); os.system('clear')
    print(f"Succesfully deleted {count} containers\n")

def choises():
    print()
    print("1. Initansible")
    print("2. Delete containers")
    print("3. Delete inventory & playbook")
    print("4. Exit\n")

def create_inventory(filename, ip_s, group):
    login = "user"
    password = "123456789"
    with open(f"{filename}.yml", 'a') as file:
        file.write(f"{group}:\n")
        file.write("  hosts:\n")
        for idx, i in enumerate(ip_s):
            file.write(f"    vm{idx}:\n")
            file.write(f"      ansible_host: {i}\n")
        file.write("  vars:\n")
        file.write(f"     ansible_ssh_user: {login}\n")
        file.write(f"     ansible_ssh_pass: {password}\n")

def inventory():
    ip_s = list()
    filename = input("Write down the name of the inventory... ")
    group = input("Write down the name of the group... ")
    with open('file.tmp', 'r') as file:
        for line in file:
            ip_s.append(line[:-1])
    create_inventory(filename, ip_s, group)


def delete_inventory_playbook():
    inventory = input("Write down the name of the inventory... ")
    playbook = input("Write down the name of the playbook... ")
    subprocess.run(['rm', '-f', f'{inventory}.yml', f'{playbook}.yml'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    choises()
    point = input("What do you choose? ")
    if point == '1':
        initansible()
        inventory()
    elif point == '2':
        delete_containers()
    elif point == '3':
        delete_inventory_playbook()
    else:
        sys.exit(0)
