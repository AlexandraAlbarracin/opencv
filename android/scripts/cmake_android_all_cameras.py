#!/usr/bin/python

import os
import sys
import shutil

ScriptHome = os.path.split(sys.argv[0])[0]
ConfFile = open(os.path.join(ScriptHome, "camera_build.conf"), "rt")
HomeDir = os.getcwd()
for s in ConfFile.readlines():
    keys = s.split(";")
    if (len(keys) < 4):
	print("Error: invalid config line: \"%s\"" % s)
	continue
    MakeTarget = keys[0]
    Arch = keys[1]
    NativeApiLevel = keys[2]
    AndroidTreeRoot = keys[3]
    AndroidTreeRoot = str.strip(AndroidTreeRoot, "\n")
    print("Building %s for %s" % (MakeTarget, Arch))
    BuildDir = os.path.join(HomeDir, MakeTarget + "_" + Arch)
    if (os.path.exists(BuildDir)):
	shutil.rmtree(BuildDir)
    try:
	os.mkdir(BuildDir)
    except:
	print("Error: cannot create direcotry \"%s\"" % BuildDir)
	continue
    shutil.rmtree(os.path.join(AndroidTreeRoot, "out", "target", "product", "generic", "system"), ignore_errors=True)
    if (Arch == "x86"):
	shutil.copytree(os.path.join(AndroidTreeRoot, "bin_x86", "system"), os.path.join(AndroidTreeRoot, "out", "target", "product", "generic", "system"))
    else:
	shutil.copytree(os.path.join(AndroidTreeRoot, "bin_arm", "system"), os.path.join(AndroidTreeRoot, "out", "target", "product", "generic", "system"))
    os.chdir(BuildDir)
    BuildLog = os.path.join(BuildDir, "build.log")
    CmakeCmdLine = "cmake -DCMAKE_TOOLCHAIN_FILE=../android.toolchain.cmake -DANDROID_SOURCE_TREE=\"%s\" -DANDROID_NATIVE_API_LEVEL=\"%s\" -DANDROID_ABI=\"%s\" -DANDROID_USE_STLPORT=ON ../../ > \"%s\" 2>&1" % (AndroidTreeRoot, NativeApiLevel, Arch, BuildLog)
    MakeCmdLine = "make %s >> \"%s\" 2>&1" % (MakeTarget, BuildLog);
    #print(CmakeCmdLine)
    os.system(CmakeCmdLine)
    #print(MakeCmdLine)
    os.system(MakeCmdLine)
    os.chdir(HomeDir)
    CameraLib = os.path.join(BuildDir, "lib", Arch, "lib" + MakeTarget + ".so")
    if (os.path.exists(CameraLib)):
	try:
	    shutil.copyfile(CameraLib, os.path.join("..", "3rdparty", "lib", Arch, "lib" + MakeTarget + ".so"))
	    print("Building %s for %s\t[OK]" % (MakeTarget, Arch));
	except:
	    print("Building %s for %s\t[FAILED]" % (MakeTarget, Arch));
ConfFile.close()

