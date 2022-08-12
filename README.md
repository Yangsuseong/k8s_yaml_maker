# K8s Yaml Maker

* 2022/08/21 기준 Ubuntu 환경에서 사용 가능

## 코드 실행
```bash
$ python3 ./auto_yaml_maker.py
>>> passwd 입력
Password : *************
Certification Success!

>>> 이미지 선택
0 : mw.local:5000/cuda-test:20210201
1 : nvidia/cuda:11.3.0-base-ubuntu20.04

몇번 이미지를 사용 하시겠습니까? : 1

>>> GPU 개수 입력
몇개의 GPU를 사용 하시겠습니까? : 1

>>> 명령어 입력
명령어 : tail -f /dev/null

yaml file create complete. please check ./k8s_create.yaml
```

## 생성된 yaml 파일 확인
```bash
$ cat ./k8s_create.yaml
#################################
apiVersion: v1
kind: Pod
metadata:
  name: root
spec:
  restartPolicy: OnFailure

  volumes:
  - name: shmdir
    emptyDir:
      medium: Memory
  - name: pvc-volume
    persistentVolumeClaim:
       claimName: root-pvc

  containers:
  - name: gpu-container
    image: mw.local:5000/cuda-test:20210201
    volumeMounts:
    - mountPath: /dev/shm
      name: shmdir
    - mountPath: /home/root
      name: pvc-volume
    command:
      - "/bin/sh"
      - "-c"
    args:
      - tail -f /dev/null
    securityContext:
      allowPrivilegeEscalation: false

    resources:
      requests:
        nvidia.com/gpu: 1
      limits:
        nvidia.com/gpu: 1
#################################
```
