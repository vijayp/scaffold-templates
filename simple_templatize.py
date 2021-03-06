#!/usr/bin/env python3
import re
import shutil
import sys
import os
import tempfile

import git
# ensure that anything we substitute is only composed of 
# letters, numbers, or _
VALID_EXPRESSION = re.compile('^[0-9A-Za-z_]+$')
REQUIRED_PARAMS = {'____PROGRAM'}
OPTIONAL_PARAMS = {'____AUTHOR', '____YEAR', '____GENERATOR_STRING'}
FILENAME_PARAMS = set(REQUIRED_PARAMS)

# make filenames don't rely on any non specified params
assert (not (FILENAME_PARAMS - (OPTIONAL_PARAMS | REQUIRED_PARAMS)))

is_valid_expression = lambda e: (VALID_EXPRESSION.match(e) is not None)

def copytree_with_substitutions(from_dir, to_dir, template_dict):
    ''' fills out a new directory tree inside to_dir, copying files from our template from_dir,
        and substituting template params within the files and in filenames '''

    # make sure we're not substituting anything strange
    for v in template_dict.values():
        if not is_valid_expression(v):
            raise TypeError('%s is not a valid expression for substitution' % v)

    # make sure we're not missing any required parameters
    missing_required = REQUIRED_PARAMS - set(template_dict.keys())
    if missing_required:
        raise TypeError('missing required params: %s' % (','.join(missing_required)))
    
    # copy optional params
    for param in OPTIONAL_PARAMS:
        if param not in template_dict:
            template_dict[param] = param
    # copy over filename params
    filename_substitutions = {k: template_dict[k] for k in FILENAME_PARAMS}

    def substitute_in_string(s, mapping=None):
        # this can be buggy
        # TODO: use a real templating framework
        if mapping is None: 
            mapping = template_dict
        for old, new in mapping.items():
            s = s.replace(old, new)
        return s

    def copy2_substitute(oldfname, newfname, *args, **kwargs):
        ''' this function is a replacement for copy2() in shutil.copytree.
        We use this to rename files while copying which is kind of a hack. '''

        # TODO we should restrict substitutions to basename to be careful
        modified_fname = substitute_in_string(os.fspath(newfname), mapping=filename_substitutions)
        return shutil.copy2(oldfname, modified_fname, *args, **kwargs)

    # 1. recursively copy all files from from_dir to to_dir,
    #    renaming files as we go
    shutil.copytree(src=from_dir, dst=to_dir, copy_function=copy2_substitute, dirs_exist_ok=True)

    # 2. for each file in the new directory, in-place replace the contents of the file
    for subdir, dirs, files in os.walk(to_dir):
        for basename in files:
            # TODO: large files might break this 
            # TODO: this is O(n^m) for file size n and with m substitutions. Super inefficient
            fn = os.path.join(subdir, basename)
            with open(fn, 'r') as fd:
                try:
                    data = fd.read()
                except UnicodeDecodeError: 
                    # this is probably a binary file.
                    continue

            with open(fn, 'w') as fd:
                fd.write(substitute_in_string(data))

def make_git_repo(location, program_name):
    assert is_valid_expression(program_name)
    repo = git.Repo.init(location)
    repo.git.add(all=True)
    repo.git.commit('-m', 'Initial commit for program %s, made by kickstart' % program_name, author='Kickstart Bot <bot@kickstartbio.com>')

    # clean up unnecessary files
    repo.git.clean('-xdf')

def make_zip_file(tree, zipfile_name):
    ''' this creates a NEW zipfile called zipfile_name, with the contents of tree in it. '''
    shutil.make_archive(zipfile_name, 'zip', tree)

if __name__ == '__main__':
    program_name = sys.argv[1]
    olddir = sys.argv[2]
    with tempfile.TemporaryDirectory() as working_dir:
        substitutions = {'____PROGRAM' : program_name}
        assert is_valid_expression(program_name)
        newdir = os.path.join(working_dir, program_name)
        copytree_with_substitutions(olddir, newdir, substitutions)
        make_git_repo(newdir, program_name)
        tmpdirname = sys.argv[3]
        zipfile_name = os.path.join(tmpdirname, program_name)
        make_zip_file(working_dir, zipfile_name)
        print('wrote %s.zip' % zipfile_name)