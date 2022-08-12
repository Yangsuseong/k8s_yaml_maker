import os
import fileinput
import sys
import getpass
import time
import tty, termios


"""
변수 목록
---------------
user_name = 유저 이름
image_list = 도커 이미지 리스트
tag_list = 도커 태그 리스트
image_id = 이미지 UUID
max_gpu_avail = 최대 사용가능 GPU 개수
"""



# Password 입력
def certified():
    password_org = "miruware0115!"
    # get password
    user_password = ""
    sys.stdout.write('Password : ')
    sys.stdout.flush()
    while True:
        ch = getch()
        if ch == '\r':
            print(" ")
            break
        if ch == '\b':
            user_password = user_password.rstrip(ch)
            sys.stdout.write('-')
            sys.stdout.flush()
        else:
            user_password += ch
            sys.stdout.write('*')
            sys.stdout.flush()
    if(password_org == user_password):
        print("Certification Success!")
        print(" ")
        print(" ")
    else:
        print("Failed to certification. Please check password.")
        exit()


# 변수 초기화
user_name = 0
image = 0
image_name = 0
image_id = 0
image_tag = 0
image_list = 0
mount_point = 0
max_gpu_avail = 0



def save_output(os_command,filename):
    # join 값 저장
    command=os_command + " > ./" + filename + ".txt"
    os.system(command)
    command="./" + filename + ".txt"
    f = open(command, "rt", encoding="utf-8")
    output = f.readlines()
    f.close()
    command="rm ./" + filename + ".txt"
    os.system(command)

    output = "".join(output).split("\n")
    
    var = 0
    var_list = []
    for i in range(len(output)):
        var = "".join(output[i]).split(" ")
        var_list.append(var)
    #print(var_list)
    output = (var_list[0])
    #print("output : ")
    #print(output)
    return output



#---------------------------------------------------------------
# username 저장
def user_name():
    command = os.popen("whoami").read()
    #print(command)
    user_name = command[:-1]
    #print('user_name : ',user_name)
    #print("user_name() complete")
    return user_name

#---------------------------------------------------------------
# 도커 이미지:태그 전처리
def docker_preprocessing():
    #os.system(ssh_connect.format(**data) + "docker images > /home/"+user_id+"/flask/yaml_maker_data/docker_image_list")
    current_path = str(os.popen("pwd").read())
    current_path = current_path.rstrip('\n')
    os.system(str("docker images | grep -v k8s | grep -v weaveworks | grep -v kubernetes | grep -v registry > " + current_path + "/yaml_maker_data/docker_image_list"))
    #os.system(scp_connect.format(**data) + "docker_image_list ./yaml_maker_data/")

# 파일을 로컬로 복사해버리자.
# sshpass scp 하는 방법 찾아서 수정할것.
# 수정해야할 부분. 모든 파일을 읽는 부분에서 경로를 수정해야함.


    f = open(current_path + "/yaml_maker_data/docker_image_list", "rt", encoding="utf-8")
    image = f.readlines()
    f.close()
    #print(image)

    image = "".join(image).split("\n")
    #image = ",".join(image).split(" ")
    #print(image[1])

    var = 0
    var_list = []

    for i in range(len(image)):
        #print(i)
        var = "".join(image[i]).split(" ")
        #print(var)
        var_list.append(var)
        

    var_list = var_list[1:-1]

    #print(var_list)

    image_name = []
    tag = []
    image_id = []
    image_list = []
    idx = 0
    for i in range(len(var_list)):
        temp=[]
        temp = ' '.join(var_list[i]).split()
        #print("temp : ", temp)
        image_name.append(temp[0])
        tag.append(temp[1])
        image_id.append(temp[2])
        image_list.append(temp[0]+ ':' +temp[1])
        print(" ")
        print(str(idx) + " : " + temp[0]+ ':' +temp[1])
        idx += 1
    """
    print('image_name : ', image_name)
    print('tag : ', tag)
    print('image_id : ', image_id)
    """
    #print('image list : ', image_list)
    
    #print("docker_preprocessing complete")
    return image_list

def get_hub_image_list():
    command = "curl --cacert /etc/docker/certs.d/mw.hub:5000/ca.crt -X GET https://mw.hub:5000/v2/_catalog > /dev/null 2>&1"
    image_list = save_output(command,"tmp.txt")
    image_list = "".join(image_list).split('"')
    image_list = image_list[3:-1:2]
    #print(image_list)

    for i in image_list:
        command = "curl --cacert /etc/docker/certs.d/mw.hub:5000/ca.crt -X GET https://mw.hub:5000/v2/"+i+"/tags/list > /dev/null 2>&1"
        tag_list = save_output(command, "tmp.txt")
        tag_list = save_output(command,"tmp.txt")
        tag_list = "".join(tag_list).split('"')
        tag_list = tag_list[7:-1:2]
        #print(tag_list)

        for j in range(len(tag_list)):
            output = i + ":" + tag_list[j]
            #print("image_list = " + output)
            image_list.append(output)



#---------------------------------------------------------------
# mountpoint 변수 저장
def mountpoint():
    mountpoint = '/home/'+ str(user_name)
    #print('mountpoint : ',mountpoint)
    #print("mountpoint() complete")
    return mountpoint

#---------------------------------------------------------------
# .yaml 파일 자동 생성
def make_yaml():
    os.system(str("cp ./yaml_maker_data/auto_job_create_frame_back.yaml ./yaml_maker_data/auto_job_create_frame.yaml"))

    print(" ")
    image_select = int(input("몇번 이미지를 사용 하시겠습니까? : "))
    use_gpu_count = str(input("몇개의 GPU를 사용 하시겠습니까? : "))
    command = str(input("명령어 : "))

    name_yaml = '  name: '+user_name + "\n"
    claimName_yaml = '       claimName: ' + user_name + "-pvc" + "\n"
    image_yaml = '    image: '+image_list[image_select] + "\n"
    mountPath_yaml = '    - mountPath: '+mountpoint + "\n"
    gpu_yaml = '        nvidia.com/gpu: '+use_gpu_count + "\n"
    command_yaml = '      - '+command + "\n"

    
    print("name_yaml : ", name_yaml)
    print("claimName_yaml : ",claimName_yaml)
    print("image_yaml : ",image_yaml)
    print("mountPath_yaml : ",mountPath_yaml)
    print("gpu_yaml : ",gpu_yaml)
    print("command_yaml : ",command_yaml)
    

    for line in fileinput.input('./yaml_maker_data/auto_job_create_frame.yaml', inplace = True):
        if 'USERNAME' in line:
            line = line.replace(line, name_yaml)
            
        if 'CLAIMNAME' in line:
            line = line.replace(line, claimName_yaml)
            
        if 'IMAGE' in line:
            line = line.replace(line, image_yaml)
            
        if 'MOUNTPATH' in line:
            line = line.replace(line, mountPath_yaml)
            
        if '      - COMMANDINPUT' in line:
            line = line.replace(line, command_yaml)
            
        if 'nvidia.com/gpu:' in line:
            line = line.replace(line, gpu_yaml)
            sys.stdout.write(line)
        else:
            sys.stdout.write(line)

    os.system(str("cp ./yaml_maker_data/auto_job_create_frame.yaml ./yaml_maker_output.yaml"))
    print("yaml file create complete. please check ./yaml_maker_output.yaml")
    print(" ")
    #---------------------------------------------------------------

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch



# Logo & Copyright
###################################################################

def logo_copyright_print():
    for i in range(3):
        print(" ")
    print("###########################################################################")
    print("#                                                                         #")
    print("#        #########      ##########     ####                ####           #")
    print("#        ##########    ###########     ####                ####           #")
    print("#        ####   ####  ####    ####     ####                ####           #")
    print("#        ####    ########     ####     ####      ####      ####           #")
    print("#        ####      ####       ####     ####    ########    ####           #")
    print("#        ####                 ####     ####   ####  ####   ####           #")
    print("#        ####                 ####     ##########    ##########           #")
    print("#        ####                 ####     #########      #########           #")
    print("#                                                                  OST    #")
    print("###########################################################################")
    for i in range(3):
        print(" ")

    print("****************************************")
    print("-Miruware-")
    print("Made by Suseong Yang")
    print("Email : tntjd5596@miruware.com")
    print("****************************************")
    for i in range(3):
        print(" ")



###########
# run
###########


logo_copyright_print()
#certified()

#ip_addr = str(input("IP : "))
#svr_port = str(input("Port : "))
#user_id = str(input("ID : "))


#data = {"user": user_id,
#        "host": ip_addr,
#        "port" : svr_port,
#        "password": user_password,
#        "path" : "/home/" + user_id + "/flask/data/"}

#ssh_connect = "sshpass -p {password} ssh {user}@{host} -p {port} "
#scp_connect = "sshpass -p {password} scp -P{port} {user}@{host}:{path} "

user_name = user_name()
image_list = docker_preprocessing()
get_hub_image_list()
#print(image_list)
mountpoint = mountpoint()
#max_gpu_avail = gpu_avail()
make_yaml()
