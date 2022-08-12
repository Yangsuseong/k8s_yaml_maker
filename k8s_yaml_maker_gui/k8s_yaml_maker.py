import os
import time
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import tkinter.messagebox
import fileinput
import sys



def docker_preprocessing():

    os.system(str("docker images | grep -v k8s | grep mw.local > ./docker_image_list"))

    f = open("./docker_image_list", "rt", encoding="utf-8")
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
        #print(" ")
        #print(str(idx) + " : " + temp[0]+ ':' +temp[1])
        image_full_name = str(temp[0]) + ":" + str(temp[1])
        lb1.insert(idx, str(image_full_name))
        idx += 1

    os.system("rm ./docker_image_list")
    
    #return image_list
    
    
    """
    print('image_name : ', image_name)
    print('tag : ', tag)
    print('image_id : ', image_id)
    """
    #print('image list : ', image_list)
    
    #print("docker_preprocessing complete")
    
    # GPU 사용 가능 개수 확인 함수
def gpu_check():
    #os.system(str(ssh_connect.format(**data)) + "nvidia-smi | grep MiB | grep % > /home/" + user_id + "/flask/data/max_gpu_avail")
    current_path = str(os.popen("pwd").read())
    current_path = current_path.rstrip('\n')
    os.system("nvidia-smi | grep MiB | grep % > ./max_gpu_avail")
    #os.system(scp_connect.format(**data) + "max_gpu_avail ./data/")
    f = open("./max_gpu_avail", "rt", encoding="utf-8")
    max_gpu_avail_temp = f.readlines()
    f.close()
    max_gpu_avail = str(len(max_gpu_avail_temp))
    os.system("rm ./max_gpu_avail")
    #print('max_gpu_avail : ',max_gpu_avail)
    #print("gpu_avail() complete")

    if(int(max_gpu_avail)>=1):
        gpu_num_list.append(0)
        for i in range(len(max_gpu_avail)):
            gpu_num_list.append(i+1)
    else:
        gpu_num_list.append(0)
        
def select_image():
    idx = lb1.curselection()
    ent1.delete(0,len(ent1.get()))
    ent1.insert(0, str(lb1.get(idx)))
    global image_select
    image_select = ent1.get()
    
        
def undo_select_image():
    ent1.delete(0,len(ent1.get()))
    
    
def container_name_check():
    global user_name
    user_name = str(os.popen("whoami").read())
    user_name = user_name.rstrip('\n')
    #print(user_name)

    os.system(str("docker ps -a | grep -i $(whoami) > ./docker_container_name"))

    f = open("./docker_container_name", "rt", encoding="utf-8")
    name = f.readlines()
    f.close()
    os.system("rm ./docker_container_name")
    
    name = "".join(name).split("\n")

    var = 0
    var_list = []

    for i in range(len(name)):
        #print(i)
        var = "".join(name[i]).split(" ")
        #print(var)
        var_list.append(var)

    var_list = var_list[:-1]

    #print(var_list)

    name_list = []
    for i in range(len(var_list)):
        temp=[]
        temp = ' '.join(var_list[i]).split()
        #print(temp[-1])
        name_list.append(temp[-1])

    #print(name_list)

    idx = 0
    container_name = ""
    #for i in range(len(name_list)):
    while True:
        idx_1 = 0
        idx_2 = 0
        temp = user_name + str(idx)
        idx += 1
        #print(len(name_list))
        if(len(name_list) == 0):
            container_name = temp
            break
        for j in name_list:
            if(str(temp) == j):
                #print("name_list :", j, "temp : ", temp)
                continue
            else:
                idx_1 += 1

            if(idx_1 == len(name_list)):
                idx_2 += 1
                container_name = temp
                #print(container_name)
        if (idx_2 == 1):
            break
    return container_name

def cancle_button():
    ent1.delete(0,len(ent1.get()))
    r_ent_name.delete(0,len(r_ent_name.get()))
    r_ent_command.delete(0,len(r_ent_command.get()))
    
def refresh_image():
    lb1.delete(0,END)
    docker_preprocessing()
    


def make_yaml():
    os.system(str("cp ./data/auto_job_create_frame_back.yaml ./data/auto_job_create_frame.yaml"))
    global k8s_mountpoint
    k8s_mountpoint = '/home/'+ str(user_name)

    name_yaml = '  name: '+k8s_container_name + "\n"
    claimName_yaml = '       claimName: ' + user_name + "-pvc" + "\n"
    container_name_yaml = '  - name: ' + k8s_container_name + "\n"
    image_yaml = '    image: '+ str(image_select) + "\n"
    mountPath_yaml = '    - mountPath: '+ k8s_mountpoint + "\n"
    gpu_yaml = '        nvidia.com/gpu: '+ use_gpu_count + "\n"
    command_yaml = '      - '+ command + "\n"
    

    for line in fileinput.input('./data/auto_job_create_frame.yaml', inplace = True):
        if 'USERNAME' in line:
            line = line.replace(line, name_yaml)
            
        if 'CLAIMNAME' in line:
            line = line.replace(line, claimName_yaml)

        if 'gpu-container' in line:
            line = line.replace(line, container_name_yaml)
            
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

def createNewWindow():
    newWindow = Toplevel(win)
    labelExample = Label(newWindow, text = "New Window")
    buttonExample = Button(newWindow, text = "New Window button")

    labelExample.pack()
    buttonExample.pack()




def summit_button():
    if(len(image_select) <= 0):
        tkinter.messagebox.showwarning(title="Warnning", message="Please Select Image.")
    
    elif(len(r_ent_name.get()) <= 0):
        tkinter.messagebox.showwarning(title="Warnning", message="Please Insert Pod name.")

    elif(len(r_ent_command.get()) <= 0):
        tkinter.messagebox.showwarning(title="Warnning", message="Please Insert Command.")

    else:
        # gpu
        gpu_command=""
        value = r_combo_gpu.current()
        #print(value)
        if(str(value) != "0"):
            gpu_command = "--gpus " + str(value)
            #print(gpu_command)
        global use_gpu_count
        use_gpu_count = str(value)
            
        # name
        container_name = str(r_ent_name.get())
        global k8s_container_name
        k8s_container_name = str(container_name)
        #print(container_name_command)
            
        
        # command
        global command
        command = str(r_ent_command.get())
        #print(command)
        
        # image
        image_name = str(ent1.get())
        #print(image_name)


        
        make_yaml()
        
        time.sleep(1)
        #win.destroy()

        if(value < 0):
            tkinter.messagebox.showwarning(title="Warnning", message="Please select GPU count.")

        if(value >= 0):    
            app = Tk()
            app.geometry("695x660")
            app.title("Job Create")
            app.option_add("*Font", "Arial 11")
            app.resizable(False, False)

            current_path = str(os.popen("pwd").read())
            current_path = current_path.rstrip('\n') + "/data/"
            #print(current_path)
            yaml_file_path = current_path + "auto_job_create_frame.yaml" 
            f = open(yaml_file_path, 'r', encoding='UTF-8')
            yaml_file_contents = f.read()
            #print(yaml_file_contents)

            # 그냥 출력
            #label = Label(app, text=yaml_file_contents, relief="solid", borderwidth="2")
            #label.pack()

            # 스크롤텍스트로 출력
            scrol_w = 75
            scrol_h = 30
            scr = scrolledtext.ScrolledText(app, width=scrol_w, height=scrol_h, font= ("Arial", 12))
            scr.insert(INSERT, yaml_file_contents)
            #scr.yview(END)
            scr.place(x=0, y=0)
            scr.configure(state="disabled")
            scr.focus()

            def app_cancle_button():
                app.destroy()

            def app_summit_button():
                os.system("kubectl create -f " + yaml_file_path)

            # Button
            app_cancle_btn = Button(app, text="cancle")
            app_cancle_btn.config(command=app_cancle_button)
            app_cancle_btn.place(x=150, y=595, width=150, height=50)

            app_summit_btn = Button(app, text=" Job Create")
            app_summit_btn.config(command=app_summit_button)
            app_summit_btn.place(x=400, y=595, width=150, height=50)
    
    







#####################################
# UI

win = Tk()
win.geometry("1100x600")
win.title("MW OST - K8s")
win.option_add("*Font", "Arial 15")
win.resizable(False, False)



# 로고
lab_img = Label(win)
img = PhotoImage(file = "./image/miruware_logo.png", master=win)
img = img.subsample(2)
lab_img.config(image=img)
lab_img.place(x=800, y=20)




# 라벨
lab1 = Label(win)
lab1.place(x=20, y=10, width=490, height=30)
lab1.config(text="Docker images")


# 리스트박스
lb1 = Listbox(win, font=("Arial", 12))
docker_preprocessing()
lb1.place(x=20, y=50, width=550, height=360)

xscrollbar = Scrollbar(win, orient="horizontal")
xscrollbar.config(command=lb1.xview)
xscrollbar.place(x=20, y=410, width=530, height=20)

yscrollbar = Scrollbar(win, orient="vertical")
yscrollbar.config(command=lb1.yview)
yscrollbar.place(x=550, y=50, width=20, height=360)


# Button
up_btn = Button(win, text="Undo")
up_btn.config(command=undo_select_image)
up_btn.place(x=120, y=470, width=160, height=30)

down_btn = Button(win, text="Select")
down_btn.config(command=select_image)
down_btn.place(x=330, y=470, width=160, height=30)


# 선택된 이미지 이름
ent1 = Entry(win)
ent1.place(x=20, y=530, width=550, height=30)
#ent1.config(text="test")


# 새로고침 버튼
refresh_button = Button(win, text="Reload")
refresh_button.config(command=refresh_image)
refresh_button.place(x=400, y=20, width=160, height=25)


# Right (Selector)
#---------------------------------------------------------------


# GPU
r_lab_gpu = Label(win)
r_lab_gpu.place(x=600, y=130, width=230, height=30)
r_lab_gpu.config(text="GPU Count ")

#gpu_num_list = [1,2,3,4,5,6,7,8]
gpu_num_list=[]
gpu_check()
r_combo_gpu = ttk.Combobox(win)
r_combo_gpu.config(value = gpu_num_list)
r_combo_gpu.set("0")
r_combo_gpu.place(x=600, y=160, width=180, height=30)






# Container Name
container_name = container_name_check()

r_lab_name = Label(win)
r_lab_name.place(x=600, y=230, width=470, height=30)
r_lab_name.config(text="New Pod Name(Do not use space)")

r_ent_name = Entry(win)
r_ent_name.insert(0, str(container_name))
r_ent_name.place(x=600, y=260, width=470, height=30)






# command
r_lab_command = Label(win)
r_lab_command.place(x=600, y=330, width=470, height=30)
r_lab_command.config(text="Command")

r_ent_command = Entry(win)
r_ent_command.insert(0,"bash")
r_ent_command.place(x=600, y=360, width=470, height=30)





# Button
cancle_btn = Button(win, text="Reset")
cancle_btn.config(command=cancle_button)
cancle_btn.place(x=850, y=510, width=100, height=50)


summit_btn = Button(win, text="Summit")
summit_btn.config(command=summit_button)
summit_btn.place(x=970, y=510, width=100, height=50)



#--------------------------------------------
# Copyright
copyright = Label(
    win,
    font=("Helvetica", 9))
copyright.config(text="Made By Suseong,Yang      Email : tntjd5596@miruware.com      2021.08.27")
copyright.place(x=630, y=570, width=500, height=30)



win.mainloop()

