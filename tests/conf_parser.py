import os
os.chdir(os.path.dirname( __file__))
conf_file_path = os.path.join(os.path.pardir, "scc.conf")
conf_file = open(conf_file_path, "r")
build_chain = []

for line in conf_file.readlines():
    line = line.split("#")[0]  # strip out comments
    line = line.strip()
    if line:
        build_chain.append(line)
