# -*- coding: utf-8 -*-
import sys
from . import iboot, pack_model, onboarding


def iboot_command():
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1]

    if cmd == 'start':
        iboot.start()
        return

    if cmd == 'pack_model':
        pack_model.pack_model()
        return

    if cmd == 'build_docker':
        pack_model.build_docker()
        return

    if cmd == 'onboarding':
        onboarding.onboarding()
        return

    print_usage()


def print_usage():
    print('iboot命令格式：')
    print('  iboot start        # 启动iBoot服务，监听端口：3330')
    print('  iboot pack_model   # 打包基于iBoot服务引擎的AI模型，在out目录下生成模型压缩文件')
    print('  iboot build_docker # 构建基于iBoot服务引擎的AI模型微服务docker镜像')
    print('  iboot onboarding [URL] # 将out目录下的模型压缩包共享至由[URL]所指定的CubeAI智立方算能服务平台')
