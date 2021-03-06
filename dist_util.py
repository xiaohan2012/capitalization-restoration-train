import os, sys, logging
from alnsim.best_ukko_servers import best_n
from glob import glob

logging.basicConfig(format='%(levelname)s-%(asctime)s: %(message)s',
                    level = logging.INFO)

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

def gen_cv_scripts(task_name, servers, group, feature_groups, data_dir, tmp_dir):
    """
    task_name: screen name also
    group: uppercase or monocase
    """
    script_paths = "deploy_scripts/%s/%s" %(group, "+".join(group.split()))
    
    if not os.path.exists(script_paths):
        os.makedirs(script_paths)
        
    for p in glob("%s/*.sh" %(script_paths)):
        sys.stderr.write("removing %s\n" %(p))
        os.remove(p)
        
    data_paths = set(glob(data_dir))
    assert len(servers) == len(data_paths) * len(feature_groups), "%d != %d" %(len(servers),
                                                                               len(data_paths)  * len(feature_groups))

    servers_file = open("%s/servers.txt" %(script_paths), "w")
    
    data_paths = set(glob(data_dir))
    for feature_group in feature_groups:
        sys.stderr.write("Feature group: %s\n" %("+".join(feature_group.split())))
        for server, test_data_path in zip(servers, data_paths):
            train_data_path = data_paths - set([test_data_path])

            train_path_string = " ".join(train_data_path)
            test_path_string = test_data_path
            feature_group_dir = "+".join(feature_group.split())
            feature_ids = feature_group
            test_data_id = test_data_path.rsplit('-', 1)[1]
            
            with open("%s/%s.sh" %(script_paths, server), "w") as f:
                f.write("screen -dmS {task_name} bash\n".format(**locals()))
                f.write("screen -S  {task_name} -p 0 -X stuff \"\n".format(**locals()))
                f.write("cd ~/code/capitalization-restoring/\n")
                f.write("cat {train_path_string} | python crfsuite-0.12/example/chunking.py {feature_ids} > {tmp_dir}/{group}/{feature_group_dir}/train-{test_data_id}.crfsuite.txt\n".format(**locals()))
                f.write("cat {test_path_string} | python crfsuite-0.12/example/chunking.py {feature_ids} > {tmp_dir}/{group}/{feature_group_dir}/test-{test_data_id}.crfsuite.txt\n".format(**locals()))

                f.write("./crfsuite-0.12/bin/crfsuite learn -m {tmp_dir}/{group}/{feature_group_dir}/cap-{test_data_id}.model {tmp_dir}/{group}/{feature_group_dir}/train-{test_data_id}.crfsuite.txt\n".format(**locals()))
                f.write("rm {tmp_dir}/{group}/{feature_group_dir}/train-{test_data_id}.crfsuite.txt\n".format(**locals())) # remove train data to save space
                
                f.write("./crfsuite-0.12/bin/crfsuite tag -qt -m {tmp_dir}/{group}/{feature_group_dir}/cap-{test_data_id}.model {tmp_dir}/{group}/{feature_group_dir}/test-{test_data_id}.crfsuite.txt > {tmp_dir}/{group}/{feature_group_dir}/result-{test_data_id}.txt\n".format(**locals()))
                # clean it up

                # f.write("rm {tmp_dir}/{group}/{feature_group_dir}/test-{test_data_id}.crfsuite.txt\n".format(**locals())) # remove test data
                # f.write("rm {tmp_dir}/{group}/{feature_group_dir}/cap-{test_data_id}.model\n".format(**locals())) # remove model 
                f.write("\"\n")
                
            servers_file.write("%s\n", server)
            
    servers_file.close()
    
if __name__ == "__main__":
    
    from datetime import datetime
    
    exclude_table = {0: (1, 48),
                     1: (49, 96),
                     2: (97, 144),
                     3: (145, 192),
                     4: (193, 240)}
    which_day = datetime.today().weekday()
    logging.info("Excluding %s",  exclude_table.get(which_day, None))
    
    servers = [s for s, _ in best_n(10,
                                    exclude_number_range = exclude_table.get(which_day, None),
                                    exclude_numbers = [125, 146])]
    
    # print servers
    # gen_preprocessing_script(servers,
    #                          data_file_path = "data/reuters/titles-and-paths",
    #                          target_file_path = "data/reuters-upper/trainable"
    # )

    # gen_cv_scripts("cv",
    #                servers, "uppercase",
    #                ["1 2 3"], 
    #                "/cs/taatto/home/hxiao/capitalization-recovery/data/uppercase/trainable/*",
    #                "/cs/taatto/home/hxiao/capitalization-recovery/tmp")
    
    # feature_groups = ("1", "2", "3", "1 2", "1 3", "2 3")
    
    task_name = sys.argv[1]

    data_group = sys.argv[2]
    assert data_group in ("uppercase", "monocase")
    
    assert len(sys.argv[2:]) >= 1, "Select at least some feature group"
    feature_group = " ".join(sys.argv[3:])
    
    logging.info("Task Name: %s", task_name)
    logging.info("Data Group: %s", data_group)
    logging.info("Feature group: %s", feature_group)
    
    gen_cv_scripts(task_name, servers, data_group,
                   [feature_group],
                   "/cs/taatto/home/hxiao/capitalization-recovery/data/{data_group}/trainable/*".format(**locals()),
                   "/cs/taatto/home/hxiao/capitalization-recovery/tmp")
    
    print "\n".join(servers)
