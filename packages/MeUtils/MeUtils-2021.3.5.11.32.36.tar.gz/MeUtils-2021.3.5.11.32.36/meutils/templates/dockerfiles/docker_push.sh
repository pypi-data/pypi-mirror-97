#!/usr/bin/env bash
# @Project      : AppZoo
# @Time         : 2021/2/23 8:31 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

ContainerID=1bc238971d22b48f0854a1cbd67748c37be9976e008cb970948553f0182c6828
ImageName=app:latest
docker commit  -a 'yuanjie' -m 'ann' $ContainerID cr.d.xiaomi.net/yuanjie/$ImageName
docker push cr.d.xiaomi.net/yuanjie/$ImageName