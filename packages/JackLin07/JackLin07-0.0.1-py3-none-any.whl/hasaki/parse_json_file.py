import json
import os
import sys




class parse_json_action_field:
    def __init__(self,action_entity,index):
        # action field
        self.__action_name = ""
        self.__action_type = ""
        self.__cc_name = ""
        self.__ld_name = ""
        self.__ar_name = ""
        self.__suffix_filter = []
        self.__src_file_path = []
        self.__src_args = ""
        self.__inc_file_path = []
        self.__obj_file_suffix = ""
        self.__output_dir = ""
        self.__user_ld_flag = ""
        # tmp var 
        self.__action_entity = action_entity
        self.__index = index

        self.__check_action_all_right()


    def __check_action_all_right(self):
        # check action is all right 
        if "name" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s name".format(self.__index))
            sys.exit()
        if "type" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s type".format(self.__index))
            sys.exit()
        if "cc" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s cc".format(self.__index))
            sys.exit()
        if "ar" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s ar".format(self.__index))
            sys.exit()
        if "ld" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s ld".format(self.__index))
            sys.exit()
        if "src_file_filter_suffix" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s src_file_filter_suffix".format(self.__index))
            sys.exit()
        if "src_path" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s src_path".format(self.__index))
            sys.exit()
        if "src_args" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s src_args".format(self.__index))
            sys.exit()
        if "inc_path" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s inc_path".format(self.__index))
            sys.exit()
        if "obj_file_suffix" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s obj_file_suffix".format(self.__index))
            sys.exit()
        if "output_dir" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s output_dir".format(self.__index))
            sys.exit()
        if "use_ld_flag" not in self.__action_entity:
            print("parse config file error.happend in parse action{}'s use_ld_flag".format(self.__index))
            sys.exit()


    def start_parse_action(self):
        self.__action_name = self.__action_entity["name"].split(" ")[0]
        if self.__action_entity["type"] == "exe":
            self.__action_type = self.__action_entity["type"]
        else:
            print("parse action{} error. now only support type [exe].".format(self.__index))
            sys.exit()
        self.__cc_name = self.__action_entity["cc"] 
        self.__ld_name = self.__action_entity["ld"] 
        self.__ar_name = self.__action_entity["ar"] 
        self.__suffix_filter = self.__action_entity["src_file_filter_suffix"] 


        # check src path is all right
        # Deduplication
        self.__src_file_path = list(set(self.__action_entity["src_path"]))
        for i in self.__src_file_path:
            if os.path.exists(i):
                continue
            print("parse action{} error.can't find src path:{}".format(self.__index,i))
            sys.exit()
        
        self.__src_args = self.__action_entity["src_args"] 

        # check inc path is all right
        # Deduplication
        self.__inc_file_path = list(set(self.__action_entity["inc_path"]))
        for i in self.__inc_file_path:
            if os.path.exists(i):
                continue
            print("parse action{} error.can't find inc path:{}".format(self.__index,i))
            sys.exit()

        self.__obj_file_suffix = self.__action_entity["obj_file_suffix"] 
        self.__output_dir = self.__action_entity["output_dir"] 
        self.__user_ld_flag = self.__action_entity["use_ld_flag"] 



    



    def get_action_name(self):
        return self.__action_name
    
    def get_action_type(self):
        return self.__action_type

    def get_action_cc(self):
        return self.__cc_name

    def get_action_ld(self):
        return self.__ld_name

    def get_action_ar(self):
        return self.__ar_name

    def get_action_suffix_filter(self):
        return self.__suffix_filter

    def get_action_src_path(self):
        return self.__src_file_path

    def get_action_src_args(self):
        return self.__src_args

    def get_action_inc_path(self):
        return self.__inc_file_path

    def get_action_obj_file_suffix(self):
        return self.__obj_file_suffix

    def get_action_output_dir(self):
        return self.__output_dir

    def get_action_ld_flag(self):
        return self.__user_ld_flag
        
        











class parse_config_json_file:
    def __init__(self,config_file_path=None):
        # config file option
        self.__global_cflag = ""
        self.__global_linkflag = ""
        self.__prebuild_cmd = []
        self.__postbuild_cmd = []
        # tmp var
        self.__config_path = ""
        self.__config_json_entity = ""
        self.__action_class_array = []
        self.__action_class_array_len = 0
        

        if config_file_path == None:
            self.__config_path = "config.json"
        else:
            self.__config_path = config_file_path

        self.__check_config_file_right(self.__config_path)
        

    def __check_config_file_right(self,config_file_path):
        if os.path.exists(config_file_path) == False:
            print("config file:{} is not exist.".format(self.__config_path))
            sys.exit()
        with open(self.__config_path,"r") as f:
            try:
                self.__config_json_entity = json.loads(f.read(1000000))
            except:
                print("{} config file is not standard json file.please check it.".format(config_file_path))
                sys.exit()
        # check config is all right
        if "global_cflag" not in self.__config_json_entity:
            print("parse config file error.happend in parse global_cflag")
            sys.exit()
        if "global_link_flag" not in self.__config_json_entity:
            print("parse config file error.happend in parse front_link_flag")
            sys.exit()
        if "prebuild_action" not in self.__config_json_entity:
            print("parse config file error.happend in parse global_cflag")
            sys.exit()
        if "postbuild_action" not in self.__config_json_entity:
            print("parse config file error.happend in parse global_cflag")
            sys.exit()
        # only check action 0
        self.__action_class_array.append(parse_json_action_field(self.__config_json_entity["action"][0],0))
        self.__action_class_array_len = len(self.__config_json_entity["action"])


    def __show_all_parse_option(self):
        print("field:{}.valud:{}".format("global_cflag",self.get_config_file_global_cflag()))
        print("field:{}.valud:{}".format("link_flag",self.get_config_file_link_flag()))
        print("field:{}.valud:{}".format("prebuild_action",self.get_config_file_prebuild_cmd()))
        print("field:{}.valud:{}".format("postbuild_action",self.get_config_file_postbuild_cmd()))

        index = 0
        for i in self.__action_class_array:
            print("action{} field:{}.valud:{}".format(index,"name",i.get_action_name()))
            print("action{} field:{}.valud:{}".format(index,"type",i.get_action_type()))
            print("action{} field:{}.valud:{}".format(index,"cc",i.get_action_cc()))
            print("action{} field:{}.valud:{}".format(index,"ld",i.get_action_ld()))
            print("action{} field:{}.valud:{}".format(index,"ar",i.get_action_ar()))
            print("action{} field:{}.valud:{}".format(index,"suffix_filter",i.get_action_suffix_filter()))
            print("action{} field:{}.valud:{}".format(index,"src_path",i.get_action_src_path()))
            print("action{} field:{}.valud:{}".format(index,"src_args",i.get_action_src_args()))
            print("action{} field:{}.valud:{}".format(index,"inc_path",i.get_action_inc_path()))
            print("action{} field:{}.valud:{}".format(index,"obj_file_suffix",i.get_action_obj_file_suffix()))
            print("action{} field:{}.valud:{}".format(index,"outout_dir",i.get_action_output_dir()))
            print("action{} field:{}.valud:{}".format(index,"ld_flag",i.get_action_ld_flag()))
            index += 1

        print("============================================================================================")
        print()
        print()
        print()
        print()




    def start_parse(self):
        # parse config file
        self.__global_cflag = self.__config_json_entity["global_cflag"]
        self.__global_linkflag = self.__config_json_entity["global_link_flag"]
        self.__prebuild_cmd = self.__config_json_entity["prebuild_action"]
        self.__postbuild_cmd = self.__config_json_entity["postbuild_action"]
        # parse action - only parse action 0
        self.__action_class_array[0].start_parse_action()
        self.__show_all_parse_option()


    def gen_action_length(self):
        return self.__action_class_array_len

    def get_config_file_global_cflag(self):
        return self.__global_cflag

    def get_config_file_link_flag(self):
        return self.__global_linkflag

    def get_config_file_prebuild_cmd(self):
        return self.__prebuild_cmd

    def get_config_file_postbuild_cmd(self):
        return self.__postbuild_cmd

    def get_config_file_action_name(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_name()

    def get_config_file_action_type(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_type()

    def get_config_file_action_cc(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_cc()


    def get_config_file_action_ld(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_ld()

    def get_config_file_action_ar(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_ar()


    def get_config_file_action_suffix_filter(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_suffix_filter()


    def get_config_file_action_src_path(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_src_path()


    def get_config_file_action_src_args(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_src_args()
        
    def get_config_file_action_inc_path(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_inc_path()


    def get_config_file_action_file_suffix(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_obj_file_suffix()

    def get_config_file_action_output_dir(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_output_dir()

    def get_config_file_action_ld_flag(self,index):
        if index >= self.__action_class_array_len:
            return ""
        else:
            return self.__action_class_array[index].get_action_ld_flag()







def list_src_file(filter,path):
    file_array = os.listdir(path)
    ret_data = []
    for i in file_array:
        if i[-2:] in filter:
            ret_data.append(i)
    return ret_data


def get_output_file_name(suffix,file_name):
    return file_name[0:-2] + suffix




def integration_cflag(glboal_flag,sub_flag):
    ret_data = ""
    for i in glboal_flag:
        if i == "":
            continue
        ret_data += i + " "
    for i in sub_flag:
        if i == "":
            continue
        ret_data += i + " "
    return ret_data


def intergration_inc(inc_path):
    ret_data = []
    for i in inc_path:
        if i == "":
            continue
        ret_data.append("-I{} ".format("../" + i))
    return ret_data


