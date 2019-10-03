#!/usr/bin/env python
#
# This class calls configuration wizard and executes scripts on it
# --------------------------------------------------------------
# Author: Luis Carrillo
# Updated: Jikai Tang - change run_validation logic
# Date: 11/2/2016
# Updated for LinuxMstrBak : Martin Bonica
# --------------------------------------------------------------
# sample calling:
#        executor = Executor(args[1], isWin)
#        output = executor.run_cfgwiz(script)

import os
import time
import json

SCP_FILE = 'cmd_mgr_executor.scp'
OUTPUT_FILE = 'cmd_mgr_executor_output.txt'
SUCCESS_TASK = 'task(s) execution completed successfully'


class Executor:
    def __init__(self, mstr_install, server_name, user_name, user_pwd):
        self.mstr_install = mstr_install
        self.server_name = server_name
        self.user_name = user_name
        self.user_pwd = user_pwd

    # Method that runs a command manager 'script'
    # returns True/False if the execution succed and an output array
    def run_cmd_mgr(self, script):
        # print self.mstr_install
        scp_full_path = os.path.join(self.mstr_install, SCP_FILE)
        # print scp_full_path
        output_full_path = os.path.join(self.mstr_install, OUTPUT_FILE)
        # print output_full_path

        if os.name == 'posix':  # Linux
            cmd_mgr = os.path.join(self.mstr_install, 'bin/mstrcmdmgr')
        else:  # Windows
            cmd_mgr = os.path.join(self.mstr_install, 'cmdmgr')
        # Create script file
        with open(scp_full_path, 'w') as f:
            f.write(script)
        # Create command to execute
        if os.name == 'posix':
            command = cmd_mgr + " -n '" + self.server_name + \
                      "' -u '" + self.user_name + "'"
            if len(self.user_pwd) > 0:
                command += " -p '" + self.user_pwd + "'"
            command += " -f " + scp_full_path + " -o " + output_full_path
        else:
            command = "cmdmgr -n \"" + self.server_name + \
                      "\" -u \"" + self.user_name + "\""
            if len(self.user_pwd) > 0:
                command += " -p '" + self.user_pwd + "'"
            command += " -f \"" + scp_full_path + "\" -o \"" + output_full_path + "\""
        print command
        # Execute command
        os.popen(command)
        # Open output file
        output = []
        with open(output_full_path, 'r') as f:
            for line in f:
                output.append(line.lower())
        found = str(output).find(SUCCESS_TASK)
        success = found > -1
        # Delete generated files
        os.remove(scp_full_path)
        os.remove(output_full_path)
        return [success, output, command]

    # Private method that returns True if the 'source' block starting at 'line' corresponds to the 'validation',
    # False otherwise
    # Make sure that the the first line of the source is checked before iterating through the rest of the
    # block to avoid index out of range error (in case the source only has one line)
    def is_valid_block(self, source, line, validation):
        i = 0
        while i < len(validation):
            src = source[line + i]
            val = validation[i]
            found = src.find(val)
            if found == -1:
                return False
            i += 1
        return True

    # Method that runs a command manager 'script' and checks if it is valid
    # returns True if the execution succeed and it passes the 'validation',
    # False otherwise
    def run_validation(self, script, validation, ignore_execution_res=True):
        cmd_mgr = self.run_cmd_mgr(script)
        print cmd_mgr
        output = cmd_mgr[1]

        # "LIST" command ignore execution result is False
        if ignore_execution_res and cmd_mgr[0] == False:
            output.insert(0, 'Error: Command Manager execution failed.')
            return [False, output]

        val_lower = []
        for v in validation:
            val_lower.append(v.lower())
        val = val_lower[0]

        for src in output:
            if val in src:
                return [True, output]

        return [False, ['Error: Validation failed.']]

    # Method that runs a command manager 'script' and
    # returns a list of values corresponding to the given 'tag'
    def run_iterator(self, script, tag):
        cmd_mgr = self.run_cmd_mgr(script)
        output = cmd_mgr[1]
        if cmd_mgr[0] == False:
            output.insert(0, 'Error: Command Manager execution failed.')
            return [False, output]
        tag_lower = tag.lower()
        tag_len = len(tag)
        values = []
        i = 0
        while i < len(output):
            src = output[i]
            found = src.find(tag_lower)
            if found > -1:
                value = src[tag_len:]
                values.append(value)
            i += 1
        return [True, values]

    def list_all_loaded_projects(self, projects=[]):

        # update_iserver_paths may try and pass in the list of projects
        # If id doesn't
        if projects == []:

            execution = self.run_validation('LIST ALL PROJECTS;', ["Task(s) execution completed successfully."])
            execution_list = execution[1]
            print execution_list

            for exe_str in execution_list:
                if 'name' in exe_str:
                    project_name = exe_str.split('= ')[1][:-1]

                # It contains 'true' if the project loaded
                # 'name = rally analytics\n', 'load on startup = true\n', 'active = loaded\n'
                if 'true' in exe_str:
                    projects.append(project_name)

        return projects

    def run_command(self, command, validation_str):
        num_try = 0
        while num_try < 10:
            print("num_try=" + str(num_try))
            execution = self.run_validation(command, validation_str)

            if execution[1]:
                break
            time.sleep(5)
            num_try += 1

        if num_try == 10:
            raise Exception("Run command failed after 10 times: " + command)

        return execution