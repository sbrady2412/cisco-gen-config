#   Author: Niladri Datta (niladridatta@att.net)
#
#   This code is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.
#
#   The author provides no warranties regarding the software, which is
#   provided "AS-IS" and your use of this software is entirely at your
#   own risk.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR DAMAGES OF ANY
#   KIND RELATING TO USE OF THE SOFTWARE, INCLUDING WITHOUT LIMITATION
#   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#   DAMAGES; ANY PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE), EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import csv
import os
import jinja2

CSV_FILE = 'switch-datafile.csv'
SW_TEMPLATE_FILE = 'cat3850-switch-template.j2'


def make_vlan_dict(row):
      
      vdb = dict([(row['voice_vlan_id'], 'VOICE')])
      for i in range(2,9):
            vid = 'vlan_id_' + str(i)
            vname = 'vlan_name_' + str(i)
            vlan_id = row[vid]
            vlan_name = row[vname]
            if vlan_id != "0" or vlan_name != "0":
                  vdb[vlan_id] = vlan_name

      row.update({"vlans": vdb})

# Prompt for file directory
scriptdir = raw_input("Enter script directory: ")
if not scriptdir.endswith('/'):
      scriptdir = scriptdir + '/'

# Check to see if Template and Jinja2 files exist
csvfile = str(scriptdir) + CSV_FILE
j2file = str(scriptdir) + SW_TEMPLATE_FILE

if not os.path.isfile(csvfile):
      sys.exit("CSV file missing, exiting")
elif not os.path.isfile(j2file):
      sys.exit("Jinja2 template file missing, exiting")

# Create subdirectory for output if one doesn't exist
cfgdir = str(scriptdir) + 'configs'

if not os.path.isdir(cfgdir):
      os.mkdir(cfgdir)

objFile = open(csvfile)

print "CSV Filename used: %r" % CSV_FILE

FileDict = csv.DictReader(objFile)

env = jinja2.Environment(
     loader=jinja2.FileSystemLoader(scriptdir),
     trim_blocks=True,
     lstrip_blocks=True)

sw_template = env.get_template(SW_TEMPLATE_FILE)

# Change to the CONFIGS directory
os.chdir(cfgdir)

for row in FileDict:
      make_vlan_dict(row)
      with open(row['hostname'] + '.txt', mode='w') as dev:
            dev.write(sw_template.render(row))
        
print "Done"
print "Config files created in %r directory" % cfgdir