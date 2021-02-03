#!/usr/bin/env python

import os
import subprocess

RESPONSE_FILE = 'cfgwiz_response.ini'
SUCCESS_TASK = 'configuration procedure has been run successfully'

class Executor:

    def __init__(self, mstr_install, is_win):
        self.mstr_install = mstr_install
        executable = 'mstrcfgwiz-editor'
        if is_win:
            executable = 'macfgwiz'
        self.cfgwiz = os.path.join(self.mstr_install, executable)

    # Method that runs a configuration wizard response file
    # returns True if the execution succeeds, False if the execution fails
    def run_cfgwiz(self, script):
        response_path = os.path.join(self.mstr_install, RESPONSE_FILE)

        # Create response file
        with open(response_path, 'w') as f:
            for line in script:
                f.write(line)

        # Execute command
        command = [self.cfgwiz, '-response', response_path]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = []
        success = False
        line_count =0

        while(line_count < 1800):  # FUTURE ENHANCEMENT : Check for case when there is an infinite loop
            line = p.stdout.readline()
            print line
            output.append(line)
            found = line.find(SUCCESS_TASK)
            if found > -1:
                success = True
                # DE97468 - wait until process is done, then check return code
                p.wait()
                #break 
            retcode = p.poll()  # returns None while subprocess is running
            if retcode is not None:
                print "return code:{}".format(retcode)
                break
            line_count += 1
        else: 
            print "Error: I-Server takes too long time to configure."

        # Delete response file
        os.remove(response_path)

        return [success, output]
