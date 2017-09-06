##############################################################################################
#
# This script will recursively read all files in the directory
#   whose path you pass as the first argument (or else the current directory),
# determine whether each file contains a React component,
# and if it does, list all of that component's
#   - props
#   - state variables
#   - rendered components
# along with the line numbers where they appear.
#
# You don't have to use PropTypes or Flow to run this; it's just a simple regex search for
# props.whatever, state.whatever, and <whatever {...}>.
#
# The goal is to help you quickly get a high-level understanding of a React or RN project
# by helping you infer the "inputs" and "outputs" of each component.
#
# Author: Charlie McGeorge @chrmcg
#
# Pull requests and issues are welcomed at github.com/chrmcg/react-analyze
#
##############################################################################################

import os
import sys
import re

rootDir = sys.argv[1] if len(sys.argv) > 1 else '.'

propsRegex = re.compile("props\.(\w+)")
stateRegex = re.compile("state\.(\w+)")
renderRegex = re.compile("render\s*\(.*\)")
tagRegex = re.compile("<(\w+)")

results = {}

for root, dirs, files in os.walk(rootDir):
    for filename in files:
        result = ''
        path = os.path.join(root, filename)
        relativePath = os.path.relpath(path, rootDir)
        relativeDir = os.path.split(relativePath)[0]
        if filename.endswith('.js') or filename.endswith('.jsx'):

            props = {}
            state = {}
            tags = {}
            hasRenderFunction = False

            for i, line in enumerate(open(path)):

                for match in re.finditer(propsRegex, line):
                    prop = match.groups()[0]
                    if prop not in props:
                        props[prop] = []
                    props[prop].append(i+1)

                for match in re.finditer(stateRegex, line):
                    stat = match.groups()[0]
                    if stat not in state:
                        state[stat] = []
                    state[stat].append(i+1)

                for match in re.finditer(renderRegex, line):
                    hasRenderFunction = True

                for match in re.finditer(tagRegex, line):
                    tag = match.groups()[0]
                    if tag not in tags:
                        tags[tag] = []
                    tags[tag].append(i+1)
                    

            if hasRenderFunction:
                result = filename + ' (/' + relativeDir + ')\n'
                for prop, lst in sorted(props.items()):
                    result += '    ' + prop + ': ' + str(lst) + '\n'

                if len(state) > 0:
                    result += '\n'

                for stat, lst in sorted(state.items()):
                    result += '    state.' + stat + ': ' + str(lst) + '\n'

                if len(tags) > 0:
                    result += '\n'

                for tag, lst in sorted(tags.items()):
                    result += '    <' + tag + '>: ' + str(lst) + '\n'

                result += '\n'
                results[path] = result

# TODO topological sort instead of alphabetical sort!
for (path, result) in sorted(results.items(), key=lambda s: s[0].lower()):
    print result
