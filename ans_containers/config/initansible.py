#importing library
import os
import sys
import subprocess
from time import sleep

def initansible(count, name):
    with open(f"file.tmp", "wb") as f:
        for i in range(1, count+1):
            subprocess.run(['docker', 'run', '-itd', f'--name={name}_{i}', 'managed'], stdout=subprocess.PIPE)
            subprocess.check_call(['docker', 'inspect', '-f', '{{ .NetworkSettings.IPAddress }}', f'{name}_{i}'], stdout=f)
            print(i); sleep(0.1); os.system('clear')
        print(f"Succesfully created {count} containers\n")

def delete_containers(count, name):
    for i in range(1, count+1):
        subprocess.run(['docker', 'rm', '-f', f'{name}_{i}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(i); sleep(0.1); os.system('clear')
    print(f"Succesfully deleted {count} containers\n")

def choises():
    print()
    print("1. Initansible")
    print("2. Init the cluster")
    print("3. Create image of containers")
    print("4. Delete cluster")
    print("5. Delete containers")
    print("6. Delete inventory & playbook & tmp")
    print("7. Exit\n")

def delete_file(filename):
    subprocess.run(['rm', '-f', f'../{sys.argv[1]}/{filename}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_inventory(filename, ip_s, group):
    delete_file(f"../{sys.argv[1]}/{filename}.yml")
    login = "root"
    password = "123456789"
    with open(f"../{sys.argv[1]}/{filename}.yml", 'a') as file:
        file.write(f"{group}:\n")
        file.write("  hosts:\n")
        for idx, i in enumerate(ip_s):
            file.write(f"    vm{idx}:\n")
            file.write(f"      ansible_host: {i}\n")
        file.write("  vars:\n")
        file.write(f"    ansible_user: {login}\n")
        file.write(f"    ansible_password: {password}\n")

def inventory(filename, group):
    ip_s = list()
    with open('file.tmp', 'r') as file:
        for line in file:
            ip_s.append(line[:-1])
    delete_file("file.tmp")
    create_inventory(filename, ip_s, group)

def question_answer_module_one():
    count = int(input("\nHow many containers? ")); print()
    name = input("What name you'd preffer to apply => "); print()
    return count, name

def question_answer_module_two():
    filename = input("Write down the name of the inventory... ")
    group = input("Write down the name of the group... ")
    return filename, group
    
def delete_inventory_playbook_tmp():
    inventory = input("Write down the name of the inventory... ")
    playbook = input("Write down the name of the playbook... ")
    subprocess.run(['rm', '-f', f'../{sys.argv[1]}/{inventory}.yml', f'../{sys.argv[1]}/{playbook}.yml', 'file.tmp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def create_image():
    subprocess.run(['docker', 'build', '-t', 'managed', '../config/'])

if __name__ == "__main__":
    choises()
    point = input("What do you choose? ")
    if point == '1':
        count, name = question_answer_module()
        initansible(count, name)
        filename, group = question_answer_module_two()
        inventory(filename, group)
    elif point == '2':
        initansible(3, "test")
        inventory("inventory", "first")
    elif point == '3':
        create_image()
    elif point == '4':
        delete_containers(3, "test")
    elif point == '5':
        count, name = question_answer_module()
        delete_containers(count, name)
    elif point == '6':
        delete_inventory_playbook_tmp()
    else:
        sys.exit(0)
