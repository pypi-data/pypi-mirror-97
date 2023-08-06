import argparse
import parse_json_file
import ninja_syntax
import os
import copy

"""
cc CC_ARGS
ld LD_ARGS
ar AR_ARGS
"""



class generate_ninja:
    def __init__(self,config_file_handle):
        self.__config_file_handle = config_file_handle
        # only generate action 0
        self.__output_dir = config_file_handle.get_config_file_action_output_dir(0)
        if os.path.exists(self.__output_dir) == False:
            os.mkdir(self.__output_dir)
        # gen build.ninja
        f = open(os.path.join(self.__output_dir,"build.ninja"),"w")
        self.__ninja_handle = ninja_syntax.Writer(f)

    

    def run(self):
        self.generate_header_comment()
        self.generate_compiler_rule()
        self.generate_user_task_rule_and_build()

        self.generate_build_action()
        self.generate_last_context()


        # close file
        self.__ninja_handle.close()


    def generate_header_comment(self):
        self.__ninja_handle.comment("this build.ninja is generate by probuild.don't edit.")
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()

    def generate_compiler_rule(self):
        self.__ninja_handle.comment("this compile rule -- begin")
        self.__ninja_handle.rule(name = "cc",command = "{} $ccfront -c $in -o $out $ccrear".format(self.__config_file_handle.get_config_file_action_cc(0))
                                ,description = "build $out")
        self.__ninja_handle.newline()
        self.__ninja_handle.rule(name = "ar",command = "{} $AR_ARGS $out $in".format(self.__config_file_handle.get_config_file_action_ar(0)))
        self.__ninja_handle.newline()
        self.__ninja_handle.rule(name = "ld",command = "{} $ldfront -o $out $in $ldrear".format(self.__config_file_handle.get_config_file_action_ld(0)))
        self.__ninja_handle.newline()
        self.__ninja_handle.rule(name = "cc_ld",command = "{} $ccfront -o $out $in $ccrear".format(self.__config_file_handle.get_config_file_action_cc(0)))
        self.__ninja_handle.newline()
        self.__ninja_handle.comment("this compile rule -- end")
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()


    def generate_user_task_rule_and_build(self):
        self.__ninja_handle.comment("this user task rule and build -- begin")
        # self.__ninja_handle.rule(name = "user_task",command = "$in ")
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()

        # generate prebuild rule
        self.__ninja_handle.rule(name = "pre0",command = "echo ",description = "exec user prebuild task")
        self.__ninja_handle.newline()
        counter = 1
        for i in self.__config_file_handle.get_config_file_prebuild_cmd():
            if i == "":
                continue
            self.__ninja_handle.rule(name = "pre{}".format(counter),command = i,description = "exec user prebuild task {}".format(counter))
            self.__ninja_handle.newline()
            counter += 1

        # generate postbuild rule
        self.__ninja_handle.rule(name = "post0",command = "echo ",description = "exec user postbuild task")
        self.__ninja_handle.newline()
        counter = 1
        for i in self.__config_file_handle.get_config_file_postbuild_cmd():
            if i == "":
                continue
            self.__ninja_handle.rule(name = "post{}".format(counter),command = i,description = "exec user prebuild task {}".format(counter))
            self.__ninja_handle.newline()

        # generate pretask build
        self.__ninja_handle._line("build a0:pre0")
        self.__ninja_handle.newline()
        counter = 1
        for i in self.__config_file_handle.get_config_file_prebuild_cmd():
            if i == "":
                continue
            self.__ninja_handle._line("build a{}:pre{}".format(counter,counter))
            self.__ninja_handle.newline()
            counter += 1


        # generate posttask build
        self.__ninja_handle._line("build b0:post0")
        self.__ninja_handle.newline()
        counter = 1
        for i in self.__config_file_handle.get_config_file_postbuild_cmd():
            if i == "":
                continue
            self.__ninja_handle._line("build b{}:post{}".format(counter,counter))
            self.__ninja_handle.newline()
            counter += 1


        
        
        self.__ninja_handle.comment("this user task rule and build -- end")
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        

    def generate_build_action(self):
        obj_array = []
        self.__ninja_handle.comment("this build action  -- begin")
        # generate build action -- obj generate 
        for i in self.__config_file_handle.get_config_file_action_src_path(0):
            file_array = parse_json_file.list_src_file(self.__config_file_handle.get_config_file_action_suffix_filter(0),i)
            # print(i,file_array)
            for j in file_array:
                out = parse_json_file.get_output_file_name(self.__config_file_handle.get_config_file_action_file_suffix(0),j)
                xin = "../" + i + "/" + j
                xout = i + "/" + out

                cflag = copy.deepcopy(self.__config_file_handle.get_config_file_global_cflag())
                cflag["ccfront"].extend(self.__config_file_handle.get_config_file_action_src_args(0))
                cflag["ccfront"].extend(parse_json_file.intergration_inc(self.__config_file_handle.get_config_file_action_inc_path(0)))

                self.__ninja_handle.build(xout,"cc",xin,variables = cflag)
                obj_array.append(xout)
                self.__ninja_handle.newline()
        
        # generate build action -- exe generate
        if self.__config_file_handle.get_config_file_action_type(0) == "exe":
            if self.__config_file_handle.get_config_file_action_ld_flag(0) == "True":
                # use ld
                self.__ninja_handle.build(self.__config_file_handle.get_config_file_action_name(0),"ld",obj_array,
                                            variables = self.__config_file_handle.get_config_file_link_flag())
            else:
                
                cflag = copy.deepcopy(self.__config_file_handle.get_config_file_global_cflag())
                cflag["ccfront"].extend(self.__config_file_handle.get_config_file_action_src_args(0))
                # user cc
                self.__ninja_handle.build(self.__config_file_handle.get_config_file_action_name(0),"cc_ld",obj_array,
                                            variables=cflag)
            
        elif self.__config_file_handle.get_config_file_action_type == "static_lib":
            pass
        else:
            # dyn lib
            pass

        self.__ninja_handle.comment("this build action  -- end")
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()



    def generate_last_context(self):
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        self.__ninja_handle.newline()
        
        pre_task_input = "a0 "
        counter = 1
        for i in self.__config_file_handle.get_config_file_prebuild_cmd():
            if i == "":
                continue
            pre_task_input += "a{} ".format(counter)
            counter += 1
        counter = 1
        post_task_input = "b0 "
        for i in self.__config_file_handle.get_config_file_postbuild_cmd():
            if i == "":
                continue
            post_task_input += "b{} ".format(counter)
            counter += 1
        
        # self.__ninja_handle.build(outputs="pretask_all",command = "phony",inputs=pre_task_input)

        
        self.__ninja_handle.phony("pretask_all",pre_task_input)
        self.__ninja_handle.newline()
        self.__ninja_handle.phony("posttask_all",post_task_input)
        self.__ninja_handle.newline()
        self.__ninja_handle.phony("all",self.__config_file_handle.get_config_file_action_name(0))
        self.__ninja_handle.default("all")
        self.__ninja_handle.newline()



def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('config_file', nargs='?', default=None)

def run(options: argparse.Namespace) -> int:
    file_handle = parse_json_file.parse_config_json_file(options.config_file)
    file_handle.start_parse()
    generate_ninja(file_handle).run()
    return 0




