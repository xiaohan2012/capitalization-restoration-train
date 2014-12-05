import os, sys
from alnsim.best_ukko_servers import best_n
from glob import glob

def gen_preprocessing_script(servers, data_file_path,
                             target_file_path = "data/reuters/trainable"):

    for p in glob("deploy_scripts/*.sh"):
        sys.stderr.write("removing %s\n" %(p))
        os.remove(p)
        
    paths = glob(data_file_path + "/*")
    assert len(servers) == len(paths), "#Server should equal segment number"

    for server, path in zip(servers, paths):
        sys.stderr.write("Prepareing script for %s at %s\n" %(server, path))
        content = """
screen -dmS {file_name} bash
screen -S  {file_name} -p 0 -X stuff "
cd ~/code/capitalization-restoring/
python data.py {raw_data_path} > {target_file_path}/{file_name}
"
        """.format(raw_data_path = path,
                   file_name = os.path.basename(path),
                   target_file_path = target_file_path)
        with open("deploy_scripts/%s.sh" %(server), "w") as f:
            f.write(content)

def gen_cv_script(servers, data_dir = "data/reuters/trainable/*"):
    for p in glob("cv_scripts/*.sh"):
        sys.stderr.write("removing %s\n" %(p))
        os.remove(p)
        
    data_paths = set(glob(data_dir))
    assert len(servers) == len(data_paths), "%d != %d" %(len(servers), len(data_paths))
    
    for server, test_data_path in zip(servers, data_paths):
        test_data_id = test_data_path.split('-')[1]
        train_data_path = data_paths - set([test_data_path])
        
        with open("cv_scripts/%s.sh" %server, "w") as f:
            f.write("screen -dmS cv bash\n")
            f.write("screen -S  cv -p 0 -X stuff \"\n")
            f.write("cd ~/code/capitalization-restoring/\n")
            f.write("cat %s | python crfsuite-0.12/example/chunking.py > tmp/train-%s.crfsuite.txt\n" %(" ".join(train_data_path), test_data_id))
            f.write("cat %s | python crfsuite-0.12/example/chunking.py > tmp/test-%s.crfsuite.txt\n" %(test_data_path, test_data_id))

            f.write("./crfsuite-0.12/bin/crfsuite learn -m tmp/cap-{id}.model tmp/train-{id}.crfsuite.txt\n".format(id = test_data_id))
            f.write("./crfsuite-0.12/bin/crfsuite tag -qt -m tmp/cap-{id}.model tmp/test-{id}.crfsuite.txt > tmp/result-{id}.txt\n".format(id = test_data_id))
            f.write("\"\n")

if __name__ == "__main__":
    from datetime import datetime
    
    exclude_table = {0: (1, 48),
                     1: (49, 96),
                     2: (97, 144),
                     3: (145, 192),
                     4: (193, 240)}
    which_day = datetime.today().weekday()
    servers = [s for s, _ in best_n(10,
                                    exclude_number_range = exclude_table.get(which_day, None))]
    
    # print servers
    gen_preprocessing_script(servers,
                             data_file_path = "data/reuters/titles-and-paths",
                             target_file_path = "data/reuters-upper/trainable")
    # gen_cv_script(servers)
    
    print "\n".join(servers)                
