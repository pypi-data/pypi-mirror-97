#TODO(fernando): marchs supported by: apple-clang 10.0 and greater
#                                     clang7, clang8 and clang9
#                                     gcc8, gcc9

# from cpt.packager import ConanMultiPackager
import os
import copy
import re
import platform
import importlib
import subprocess
import sys
import difflib
import tempfile
from conans import ConanFile, CMake
from conans.errors import ConanException
from conans.model.version import Version
from conans import __version__ as conan_version

from subprocess import Popen, PIPE, STDOUT
import inspect
from collections import deque


base94_charset = ''.join(map(chr, range(33,127)))
base58_charset = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

def base58_flex_encode(val, chrset=base58_charset):
    """\
    Returns a value encoded using 'chrset' regardless of length and 
    composition... well, needs 2 printable asccii chars minimum...

    :param val: base-10 integer value to encode as base*
    :param chrset: the characters to use for encoding

    Note: While this could encrypt some value, it is an insecure toy. 

    """
    basect = len(chrset)
    assert basect > 1
    encode = deque()

    while val > 0:
        val, mod = divmod(val, basect)
        encode.appendleft(chrset[mod])

    return ''.join(encode)

def base58_flex_decode(enc, chrset=base58_charset):
    """\
    Returns the 'chrset'-decoded value of 'enc'. Of course this needs to use 
    the exact same charset as when to encoding the value.

    :param enc: base-* encoded value to decode
    :param chrset: the character-set used for original encoding of 'enc' value

    Note: Did you read the 'encode' note above? Splendid, now have 
             some fun... somewhere...

    """
    basect = len(chrset)
    decoded = 0

    for e, c in enumerate(enc[::-1]):
        decoded += ((basect**e) * chrset.index(c))

    return decoded

DEFAULT_ORGANIZATION_NAME = 'k-nuth'
DEFAULT_LOGIN_USERNAME = 'fpelliccioni'
DEFAULT_USERNAME = 'kth'
DEFAULT_REPOSITORY = 'kth'


def get_base_microarchitectures():
    return ['haswell']

def get_base_march_ids():
    return ['4fZKi37a595hP']        # haswell

def get_tempfile_name():
    return os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))

def get_compilation_symbols_gcc_string_program(filename, default=None):
    ofile = filename + '.o'
    afile = filename + '.a'
    try:

        # print("get_compilation_symbols_gcc_string_program - 1")

        # g++ -D_GLIBCXX_USE_CXX11_ABI=1 -c test.cxx -o test-v2.o
        # ar cr test-v1.a test-v1.o
        # nm test-v1.a

        # g++ -D_GLIBCXX_USE_CXX11_ABI=1 -c -o ofile.o -x c++ -
        # ar cr ofile.a ofile.o
        # nm ofile.a

        p = Popen(['g++', '-D_GLIBCXX_USE_CXX11_ABI=1', '-c', '-o', ofile, '-x', 'c++', '-'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
        # print("get_compilation_symbols_gcc_string_program - 2")

        output, _ = p.communicate(input=b'#include <string>\nstd::string foo __attribute__ ((visibility ("default")));\nstd::string bar __attribute__ ((visibility ("default")));\n')
        # print("get_compilation_symbols_gcc_string_program - 3")

        if p.returncode != 0:
            # print("get_compilation_symbols_gcc_string_program - 4")
            return default

        # print("get_compilation_symbols_gcc_string_program - 5")

        p = Popen(['ar', 'cr', afile, ofile], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    

        # print("get_compilation_symbols_gcc_string_program - 6")
        output, _ = p.communicate()
        # print("get_compilation_symbols_gcc_string_program - 7")

        if p.returncode != 0:
            # print("get_compilation_symbols_gcc_string_program - 8")
            return default

        # print("get_compilation_symbols_gcc_string_program - 9")

        p = Popen(['nm', afile], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
        # print("get_compilation_symbols_gcc_string_program - 10")
        output, _ = p.communicate()
        # print("get_compilation_symbols_gcc_string_program - 11")

        if p.returncode == 0:
            # print("get_compilation_symbols_gcc_string_program - 12")
            if output:
                # print("get_compilation_symbols_gcc_string_program - 13")
                return output.decode("utf-8")

        # print("get_compilation_symbols_gcc_string_program - 14")

        return default
    except OSError as e:
        # print("get_compilation_symbols_gcc_string_program - 15")
        print(e)
        return default
    except:
        # print("get_compilation_symbols_gcc_string_program - 16")
        return default

def glibcxx_supports_cxx11_abi():
    name = get_tempfile_name()
    # print(name)
    flags = get_compilation_symbols_gcc_string_program(name)
    # print(flags)
    if flags is None:
        return False
    return "__cxx11" in flags


def get_conan_packager():
    pkg = importlib.import_module('cpt.packager')
    return pkg
    # try:
    #     pkg = importlib.import_module('cpt.packager')
    #     return pkg
    # except ImportError:
    #     # print("*** cpuid could not be imported")
    #     return None

def get_git_branch(default=None):
    try:
        res = subprocess.Popen(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        # print('fer 0')

        if output:
            # print('fer 0.1')
            if res.returncode == 0:
                # print('fer 0.2')
                # print(output)
                # print(output.decode("utf-8"))
                # print(output.decode("utf-8").replace('\n', ''))
                ret = output.decode("utf-8").replace('\n', '').replace('\r', '')
                # print(ret)
                return ret
        return default
    except OSError: # as e:
        # print('fer 1')
        return default
    except:
        # print('fer 2')
        return default

def get_git_describe(default=None):
    try:
        res = subprocess.Popen(["git", "describe", "master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                return output.decode("utf-8").replace('\n', '').replace('\r', '')
                # return output.replace('\n', '').replace('\r', '')
        return default
    except OSError: # as e:
        return default
    except:
        return default

        

def get_version_from_git_describe_no_releases(default=None, is_dev_branch=False):
    describe = get_git_describe()
    
    # print('describe')
    # print(describe)

    if describe is None:
        return None
    version = describe.split('-')[0][1:]

    if is_dev_branch:
        version_arr = version.split('.')
        if len(version_arr) != 3:
            # print('version has to be of the following format: xx.xx.xx')
            return None
        # version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), version_arr[2])
        version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), 0)

    return version

def get_version_from_git_describe(default=None, is_dev_branch=False):
    describe = get_git_describe()
    
    # print('describe')
    # print(describe)

    # if describe is None:
    #     return None

    if describe is None:
        describe = "v0.0.0-"

    version = describe.split('-')[0][1:]

    if is_dev_branch:
        # print(version)
        # print(release_branch_version_to_int(version))
        
        # print(max_release_branch())

        max_release_i, max_release_s = max_release_branch()
        
        if max_release_i is not None and max_release_i > release_branch_version_to_int(version):
            version = max_release_s

        version_arr = version.split('.')
        if len(version_arr) != 3:
            # print('version has to be of the following format: xx.xx.xx')
            return None
        # version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), version_arr[2])
        version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), 0)

    return version

def get_git_branches(default=None):
    try:
        # res = subprocess.Popen(["git", "branch", "-r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # res = subprocess.Popen(["git", "branch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # git ls-remote --heads origin
        # res = subprocess.Popen(["git", "ls-remote", "--heads"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = subprocess.Popen(["git", "ls-remote", "--heads", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                # return output.decode("utf-8").replace('\n', '').replace('\r', '')
                return output.decode("utf-8")
        return default
    except OSError: # as e:
        return default
    except:
        return default

def release_branch_version_to_int(version):
    verarr = version.split('.')
    if len(verarr) != 3:
        return None
    verstr = verarr[0].zfill(5) + verarr[1].zfill(5) + verarr[2].zfill(5)
    return int(verstr)

def release_branch_version(branch):
    version = branch.split('-')[-1]
    return (release_branch_version_to_int(version), version)

def max_release_branch(default=None):
    branches = get_git_branches()
    # print(branches)
    if branches is None:
        return False

    max = None
    max_str = None

    for line in branches.splitlines():
        line = line.strip()
        # print(line)
        # if line.startswith("origin/release-"):
        if "release-" in line: 
            veri, vers = release_branch_version(line)
            if veri is not None:
                if max is None or veri > max:
                    max = veri
                    max_str = vers

    return (max, max_str)

# def get_version_from_git_describe_clean(default=None, increment_minor=False):
#     describe = get_git_describe()
#     if describe is None:
#         return None
#     version = describe.split('-')[0][1:]
#     if increment_minor:
#         version_arr = version.split('.')
#         if len(version_arr) != 3:
#             # print('version has to be of the following format: xx.xx.xx')
#             return None
#         version = "%s.%s.%s" % (version_arr[0], str(int(version_arr[1]) + 1), version_arr[2])
#     return version

def copy_env_vars(env_vars):
    env_vars["KTH_BRANCH"] = os.getenv('KTH_BRANCH', '-')
    env_vars["KTH_CONAN_CHANNEL"] = os.getenv('KTH_CONAN_CHANNEL', '-')
    env_vars["KTH_FULL_BUILD"] = os.getenv('KTH_FULL_BUILD', '-')
    env_vars["KTH_CONAN_VERSION"] = os.getenv('KTH_CONAN_VERSION', '-')

def is_development_branch_internal(branch = None):
    if branch is None: 
        branch = get_branch()
        
    if branch is None: 
        return False

    # return branch == 'dev' or branch.startswith('feature')    

    if branch == 'master':
        return False
    if branch.startswith('release'):
        return False
    if branch.startswith('hotfix'):
        return False

    return True


def is_development_branch():
    branch = get_branch()
    if branch is None: 
        return False

    # return branch == 'dev' or branch.startswith('feature')    

    if branch == 'master':
        return False
    if branch.startswith('release'):
        return False
    if branch.startswith('hotfix'):
        return False

    return True


# if ($Env:APPVEYOR_REPO_BRANCH -ceq "dev") {
# +        $Env:KTH_CONAN_CHANNEL = "testing"
# +        $Env:KTH_FULL_BUILD = 0
# +      }
# +      elseif ($Env:APPVEYOR_REPO_BRANCH.StartsWith("release")) {
# +        $Env:KTH_CONAN_CHANNEL = "stable"
# +        $Env:KTH_FULL_BUILD = 1
# +      }
# +      elseif ($Env:APPVEYOR_REPO_BRANCH.StartsWith("hotfix")) {
# +        $Env:KTH_CONAN_CHANNEL = "stable"
# +        $Env:KTH_FULL_BUILD = 1
# +      }
# +      elseif ($Env:APPVEYOR_REPO_BRANCH.StartsWith("feature")) {
# +        $Env:KTH_CONAN_CHANNEL = $Env:APPVEYOR_REPO_BRANCH
# +        $Env:KTH_FULL_BUILD = 0
# +      }
# +      else {
# +        $Env:KTH_CONAN_CHANNEL = "stable"
# +        $Env:KTH_FULL_BUILD = 1
# +      }


def get_branch():
    branch = os.getenv("KTH_BRANCH", None)
    
    # print("branch: %s" % (branch,))

    if branch is None: 
        branch = get_git_branch()

    # print("branch: %s" % (branch,))

    return branch

# def get_branch_clean():
#     branch = os.getenv("KTH_BRANCH", None)
#     if branch is None: 
#         branch = get_git_branch()
#     return branch

def get_version_from_branch_name():
    branch = get_branch()
    # print("get_version_from_branch_name - branch: %s" % (branch,))
    if branch is None: 
        return None
    if branch.startswith("release-") or branch.startswith("hotfix-"):
        return branch.split('-', 1)[1]
    if branch.startswith("release_") or branch.startswith("hotfix_"):
        return branch.split('_', 1)[1]
    return None

# def get_version_from_branch_name_clean():
#     branch = get_branch_clean()
#     if branch is None: 
#         return None
#     if branch.startswith("release-") or branch.startswith("hotfix-"):
#         return branch.split('-', 1)[1]
#     if branch.startswith("release_") or branch.startswith("hotfix_"):
#         return branch.split('_', 1)[1]
#     return None

def option_on_off(option):
    return "ON" if option else "OFF"

def access_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().replace('\n', '').replace('\r', '')

def get_content(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_name)
    return access_file(file_path)

def get_content_default(file_name, default=None):
    try:
        return get_content(file_name)
    except IOError as e:
        return default

def get_version_from_file(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_version')

def get_version_from_file_no_recipe_dir():
    return get_content_default('conan_version')

def get_version_no_recipe_dir():
    # print("get_version()----------------------------------------------------------")
    # print("KTH_BRANCH:        %s" % (os.getenv("KTH_BRANCH", None),))
    # print("KTH_CONAN_CHANNEL: %s" % (os.getenv("KTH_CONAN_CHANNEL", None),))
    # print("KTH_FULL_BUILD:    %s" % (os.getenv("KTH_FULL_BUILD", None),))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    version = get_version_from_file_no_recipe_dir()

    # print('------------------------------------------------------')
    # print("version 1: %s" % (version,))

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)

    # print("version 2: %s" % (version,))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    if version is None:
        version = get_version_from_branch_name()

    # print("version 3: %s" % (version,))

    if version is None:
        version = get_version_from_git_describe(None, is_development_branch())

    # print("version 4: %s" % (version,))
    # print('------------------------------------------------------')

    return version

def get_version(recipe_dir):
    # print("get_version()----------------------------------------------------------")
    # print("KTH_BRANCH:        %s" % (os.getenv("KTH_BRANCH", None),))
    # print("KTH_CONAN_CHANNEL: %s" % (os.getenv("KTH_CONAN_CHANNEL", None),))
    # print("KTH_FULL_BUILD:    %s" % (os.getenv("KTH_FULL_BUILD", None),))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    version = get_version_from_file(recipe_dir)

    # print('------------------------------------------------------')
    # print("version 1: %s" % (version,))

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)

    # print("version 2: %s" % (version,))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    if version is None:
        version = get_version_from_branch_name()

    # print("version 3: %s" % (version,))

    if version is None:
        version = get_version_from_git_describe(None, is_development_branch())

    # print("version 4: %s" % (version,))
    # print('------------------------------------------------------')

    return version

def get_version_no_releases(recipe_dir, default=None):
    # print("get_version()----------------------------------------------------------")
    # print("KTH_BRANCH:        %s" % (os.getenv("KTH_BRANCH", None),))
    # print("KTH_CONAN_CHANNEL: %s" % (os.getenv("KTH_CONAN_CHANNEL", None),))
    # print("KTH_FULL_BUILD:    %s" % (os.getenv("KTH_FULL_BUILD", None),))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    version = get_version_from_file(recipe_dir)

    # print('------------------------------------------------------')
    # print("version 1: %s" % (version,))

    if version is None:
        version = os.getenv("KTH_CONAN_VERSION", None)

    # print("version 2: %s" % (version,))
    # print("KTH_CONAN_VERSION: %s" % (os.getenv("KTH_CONAN_VERSION", None),))

    if version is None:
        version = get_version_from_branch_name()

    # print("version 3: %s" % (version,))

    if version is None:
        version = get_version_from_git_describe_no_releases(None, is_development_branch())

    # print("version 4: %s" % (version,))
    # print('------------------------------------------------------')

    if version is None:
        version = default


    return version


# def get_version_clean():
#     version = get_version_from_file()

#     if version is None:
#         version = os.getenv("KTH_CONAN_VERSION", None)

#     if version is None:
#         version = get_version_from_branch_name_clean()

#     if version is None:
#         version = get_version_from_git_describe_clean(None, is_development_branch_clean())

#     return version


def get_channel_from_file_no_recipe_dir():
    return get_content_default('conan_channel')

def get_channel_from_file(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_channel')

def branch_to_channel(branch):
    if branch is None:
        return "staging"
    if branch == 'dev':
        return "testing"
    if branch.startswith('release'):
        return "staging"
    if branch.startswith('hotfix'):
        return "staging"
    if branch.startswith('feature'):
        return branch

    return "staging"

def get_channel_from_branch():
    return branch_to_channel(get_branch())
    
    

def get_channel_no_recipe_dir():
    channel = get_channel_from_file_no_recipe_dir()

    if channel is None:
        channel = os.getenv("KTH_CONAN_CHANNEL", None)

    if channel is None:
        # channel = get_git_branch()
        channel = get_channel_from_branch()

    if channel is None:
        channel = 'staging'

    return channel

def get_channel(recipe_dir):
    channel = get_channel_from_file(recipe_dir)

    if channel is None:
        channel = os.getenv("KTH_CONAN_CHANNEL", None)

    if channel is None:
        channel = get_channel_from_branch()

    if channel is None:
        channel = 'staging'

    return channel

def get_user(recipe_dir):
    return get_content_default_with_dir(recipe_dir, 'conan_user', DEFAULT_USERNAME)

def get_user_no_recipe_dir():
    return get_content_default('conan_user', DEFAULT_USERNAME)

def get_repository():
    return os.getenv("KTH_BINTRAY_REPOSITORY", DEFAULT_REPOSITORY)


def get_content_with_dir(dir, file_name):
    # print(__file__)
    # print(os.path.abspath(__file__))

    # print('sys.argv[0] =', sys.argv[0])             
    # pathname = os.path.dirname(sys.argv[0])        
    # print('path =', pathname)
    # print('full path =', os.path.abspath(pathname)) 

    # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_name)
    file_path = os.path.join(dir, file_name)
    return access_file(file_path)

def get_content_default_with_dir(dir, file_name, default=None):
    try:
        return get_content_with_dir(dir, file_name)
    except IOError as e:
        # print(file_name)
        # print(e)
        return default





def get_conan_req_version(recipe_dir):
    # return get_content_default('conan_req_version', None)
    return get_content_default_with_dir(recipe_dir, 'conan_req_version', None)

def get_conan_vars(recipe_dir):
    org_name = os.getenv("CONAN_ORGANIZATION_NAME", DEFAULT_ORGANIZATION_NAME)
    login_username = os.getenv("CONAN_LOGIN_USERNAME", DEFAULT_LOGIN_USERNAME)
    username = os.getenv("CONAN_USERNAME", get_user(recipe_dir))
    channel = os.getenv("CONAN_CHANNEL", get_channel(recipe_dir))
    version = os.getenv("CONAN_VERSION", get_version(recipe_dir))
    return org_name, login_username, username, channel, version

def get_value_from_recipe(recipe_dir, search_string, recipe_name="conanfile.py"):
    # recipe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', recipe_name)
    recipe_path = os.path.join(recipe_dir, recipe_name)
    with open(recipe_path, "r") as conanfile:
        contents = conanfile.read()
        result = re.search(search_string, contents)
    return result

def get_name_from_recipe(recipe_dir):
    return get_value_from_recipe(recipe_dir, r'''name\s*=\s*["'](\S*)["']''').groups()[0]

def get_user_repository(org_name, repository_name):
    # https://api.bintray.com/conan/k-nuth/kth
    return "https://api.bintray.com/conan/{0}/{1}".format(org_name.lower(), repository_name)


def is_pull_request_appveyor():
    return os.getenv("APPVEYOR_PULL_REQUEST_NUMBER", None) is not None

def is_pull_request_travis():
    # return os.getenv("TRAVIS_PULL_REQUEST", "false") != "false"
    return os.getenv("TRAVIS_PULL_REQUEST", None) is not None

def is_pull_request():
    return is_pull_request_travis() or is_pull_request_appveyor()

def get_conan_upload(org_name):
    # if is_pull_request(): return ''
    repository_name = get_repository()
    return os.getenv("CONAN_UPLOAD", get_user_repository(org_name, repository_name))

def get_conan_upload_for_remote(org_name):
    repository_name = get_repository()
    return get_user_repository(org_name, repository_name)

def get_conan_remotes(org_name):
    # While redundant, this moves upload remote to position 0.
    # remotes = [get_conan_upload_for_remote(org_name),
    #           'https://api.bintray.com/conan/k-nuth/kth',
    #           'https://api.bintray.com/conan/bitprim/bitprim']

    remotes = [get_conan_upload_for_remote(org_name),
              'https://api.bintray.com/conan/tao-cpp/tao']

    # # Add bincrafters repository for other users, e.g. if the package would
    # # require other packages from the bincrafters repo.
    # bincrafters_user = "bincrafters"
    # if username != bincrafters_user:
    #     remotes.append(get_conan_upload(bincrafters_user))
    return remotes

def get_os():
    return platform.system().replace("Darwin", "Macos")

def get_archs():
    return ["x86_64"]
    # archs = os.getenv("CONAN_ARCHS", None)
    # if get_os() == "Macos" and archs is None:
    #     return ["x86_64"]
    # return split_colon_env("CONAN_ARCHS") if archs else None


def get_builder(recipe_dir, args=None):
    name = get_name_from_recipe(recipe_dir)
    org_name, login_username, username, channel, version = get_conan_vars(recipe_dir)
    reference = "{0}/{1}".format(name, version)
    upload = get_conan_upload(org_name)
    remotes = os.getenv("CONAN_REMOTES", get_conan_remotes(org_name))

    #TODO(fernando): check why when a remote is set before get_builder() call we get the following error:
            #  >> Verifying credentials...
            # Traceback (most recent call last):
            #   File "C:\Python37\lib\site-packages\conans\client\cache\remote_registry.py", line 219, in __getitem__
            #     remote = self._remotes[remote_name]
            # KeyError: 'upload_repo'
            # During handling of the above exception, another exception occurred:
            # Traceback (most recent call last):
            #   File "build.py", line 38, in <module>
            #     builder.run()
            #   File "C:\Python37\lib\site-packages\cpt\packager.py", line 505, in run
            #     self.auth_manager.login(self.remotes_manager.upload_remote_name)
            #   File "C:\Python37\lib\site-packages\cpt\auth.py", line 106, in login
            #     self._conan_api.authenticate(user, password, remote_name)
            #   File "C:\Python37\lib\site-packages\conans\client\conan_api.py", line 81, in wrapper
            #     return f(api, *args, **kwargs)
            #   File "C:\Python37\lib\site-packages\conans\client\conan_api.py", line 794, in authenticate
            #     remote = self.get_remote_by_name(remote_name)
            #   File "C:\Python37\lib\site-packages\conans\client\conan_api.py", line 81, in wrapper
            #     return f(api, *args, **kwargs)
            #   File "C:\Python37\lib\site-packages\conans\client\conan_api.py", line 1079, in get_remote_by_name
            #     return self.app.cache.registry.load_remotes()[remote_name]
            #   File "C:\Python37\lib\site-packages\conans\client\cache\remote_registry.py", line 225, in __getitem__
            #     raise NoRemoteAvailable("No remote '%s' defined in remotes" % (remote_name))
            # conans.errors.NoRemoteAvailable: No remote 'upload_repo' defined in remotes
            # Build success    

    print(org_name)
    print(remotes)
    print(upload)
    


    # upload_when_stable = get_upload_when_stable()
    # stable_branch_pattern = os.getenv("CONAN_STABLE_BRANCH_PATTERN", "stable/*")

    archs = get_archs()

    # print((login_username, username, channel, version, archs))

    builder = get_conan_packager().ConanMultiPackager(
        # args=args,    # Removed on https://github.com/conan-io/conan-package-tools/pull/269
        # pip_install=["kthbuild==0.17.0", "conan-promote==0.1.2"]
        # pip_install=["--install-option='--no-remotes=True' kthbuild"],
        pip_install=["kthbuild"],
        username=username,
        login_username=login_username,
        channel=channel,
        reference=reference,
        upload=upload,
        remotes=remotes,
        archs=archs,
        # upload_only_when_stable=upload_when_stable,
        # stable_branch_pattern=stable_branch_pattern
        )

    return builder, name

def handle_microarchs(opt_name, microarchs, filtered_builds, settings, options, env_vars, build_requires):
    microarchs = list(set(microarchs))

    for ma in microarchs:
        opts_copy = copy.deepcopy(options)
        opts_copy[opt_name] = ma
        filtered_builds.append([settings, opts_copy, env_vars, build_requires])

def filter_marchs_tests(name, builds, test_options, march_opt=None):
    if march_opt is None:
        # march_opt = "%s:microarchitecture" % name
        march_opt = "%s:march_id" % name

    for b in builds:
        options = b[1]
        if options[march_opt] != "x86-64":
            for to in test_options:
                options[to] = "False"



# --------------------------------------------

# https://gcc.gnu.org/onlinedocs/gcc-4.8.0/gcc/i386-and-x86_002d64-Options.html
# https://gcc.gnu.org/onlinedocs/gcc-7.4.0/gcc/x86-Options.html#x86-Options
# https://gcc.gnu.org/onlinedocs/gcc-8.3.0/gcc/x86-Options.html#x86-Options
# https://gcc.gnu.org/onlinedocs/gcc-9.1.0/gcc/x86-Options.html#x86-Options



def get_cpuid():
    try:
        # print("*** cpuid OK")
        cpuid = importlib.import_module('cpuid')
        return cpuid
    except ImportError:
        # print("*** cpuid could not be imported")
        return None

def get_cpu_microarchitecture_or_default(default):
    cpuid = get_cpuid()
    if cpuid != None:
        # return '%s%s' % cpuid.cpu_microarchitecture()
        return '%s' % (''.join(cpuid.cpu_microarchitecture()))
    else:
        self.output.warn("cpuid module not installed")
        return default

# microarchitecture_default = 'x86_64'
# def get_cpu_microarchitecture():
#     return get_cpu_microarchitecture_or_default(microarchitecture_default)


def get_cpu_microarchitecture():
    return get_cpu_microarchitecture_or_default(None)




marchs_extensions = {
    'x86-64':         ['64-bit extensions'],

# Intel Core
    #tock
    'core2':          ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3'],
    #tick
    # 'penryn':         ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1'],
    #tock
    'nehalem':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT'],
    #tick
    'westmere':       ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL'],
    #tock
    'sandybridge':    ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX'],
    #tick
    'ivybridge':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C'],
    #tock
    'haswell':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2'],
    #tick/process
    'broadwell':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW'],  #TXT, TSX, 
                                 

    'skylake':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES'],
    'skylake-avx512': ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES', 'AVX512F', 'AVX512CD', 'AVX512VL', 'AVX512BW', 'AVX512DQ', 'PKU', 'CLWB'],
    # Kaby Lake
    # Coffee Lake
    # Whiskey Lake
    # Cascade Lake
    'cascadelake':    ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES', 'AVX512F', 'AVX512CD', 'AVX512VL', 'AVX512BW', 'AVX512DQ', 'PKU', 'CLWB', 'AVX512VNNI'],

    'cannonlake':     ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES', 'AVX512F', 'AVX512CD', 'AVX512VL', 'AVX512BW', 'AVX512DQ', 'PKU', '????', 'AVX512VBMI', 'AVX512IFMA', 'SHA', 'UMIP'],
    'icelake-client': ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES', 'AVX512F', 'AVX512CD', 'AVX512VL', 'AVX512BW', 'AVX512DQ', 'PKU', 'CLWB', 'AVX512VBMI', 'AVX512IFMA', 'SHA', 'UMIP', 'RDPID', 'GFNI', 'AVX512VBMI2', 'AVX512VPOPCNTDQ', 'AVX512BITALG', 'AVX512VNNI', 'VPCLMULQDQ', 'VAES'],
    'icelake-server': ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW', 'CLFLUSHOPT', 'XSAVEC', 'XSAVES', 'AVX512F', 'AVX512CD', 'AVX512VL', 'AVX512BW', 'AVX512DQ', 'PKU', 'CLWB', 'AVX512VBMI', 'AVX512IFMA', 'SHA', 'UMIP', 'RDPID', 'GFNI', 'AVX512VBMI2', 'AVX512VPOPCNTDQ', 'AVX512BITALG', 'AVX512VNNI', 'VPCLMULQDQ', 'VAES', 'PCONFIG', 'WBNOINVD'],
    # Tiger Lake
    # Sapphire Rapids

# Intel Atom
    'bonnell':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'MOVBE'],
    'silvermont':     ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'MOVBE', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'RDRND'],
    'goldmont':       ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'MOVBE', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'RDRND', 'XSAVE', 'XSAVEOPT', 'FSGSBASE'],
    'goldmont-plus':  ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'MOVBE', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'RDRND', 'XSAVE', 'XSAVEOPT', 'FSGSBASE', 'PTWRITE', 'RDPID', 'SGX', 'UMIP'],
    'tremont':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'MOVBE', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'RDRND', 'XSAVE', 'XSAVEOPT', 'FSGSBASE', 'PTWRITE', 'RDPID', 'SGX', 'UMIP', 'GFNI-SSE', 'CLWB', 'ENCLV'],

# Intel High-end
    'knl':            ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW',                                   'AVX512F', 'AVX512CD', 'AVX512PF', 'AVX512ER'],
    'knm':            ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4', 'SSE4.1', 'SSE4.2', 'POPCNT', 'AES', 'PCLMUL', 'AVX', 'FSGSBASE', 'RDRND', 'F16C', 'FMA', 'BMI', 'BMI2', 'MOVBE', 'AVX2', 'RDSEED', 'ADCX', 'PREFETCHW',                                   'AVX512F', 'AVX512CD', 'AVX512PF', 'AVX512ER', 'AVX5124VNNIW', 'AVX5124FMAPS', 'AVX512VPOPCNTDQ'],



# AMD       https://en.wikipedia.org/wiki/List_of_AMD_CPU_microarchitectures
#           AMD K8 Hammer: k8, opteron, athlon64, athlon-fx
#           https://en.wikipedia.org/wiki/AMD_K8
    'k8':            ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!'],
    'opteron':       ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!'],
    'athlon64':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!'],
    'athlon-fx':     ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!'],

#           AMD K8 Hammer with SSE3: k8-sse3, opteron-sse3, athlon64-sse3
    'k8-sse3':       ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3'],
    'opteron-sse3':  ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3'],
    'athlon64-sse3': ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3'],

#           AMD Family 10h, or K10: amdfam10, barcelona            
#           https://en.wikipedia.org/wiki/AMD_10h
    'amdfam10':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM'],
    'barcelona':     ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM'],

#           AMD Bobcat Family 14h (low-power/low-cost market)   https://en.wikipedia.org/wiki/Bobcat_(microarchitecture)
    'btver1':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'CX16'],
#           AMD Jaguar Family 16h (low-power/low-cost market)   https://en.wikipedia.org/wiki/Jaguar_(microarchitecture)
    'btver2':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'CX16', 'MOVBE', 'F16C', 'BMI', 'AVX', 'PCL_MUL', 'AES', 'SSE4.2', 'SSE4.1'],
#           AMD Puma Family 16h (2nd-gen) (low-power/low-cost market)   https://en.wikipedia.org/wiki/Puma_(microarchitecture)
#           ????

#           AMD Bulldozer Family 15h (1st-gen)      https://en.wikipedia.org/wiki/Bulldozer_(microarchitecture)
    'bdver1':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16'],
#           AMD Piledriver Family 15h (2nd-gen)     https://en.wikipedia.org/wiki/Piledriver_(microarchitecture)
    'bdver2':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16', 'BMI', 'TBM', 'F16C', 'FMA'],
#           AMD Steamroller Family 15h (3rd-gen)    https://en.wikipedia.org/wiki/Steamroller_(microarchitecture)
    'bdver3':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16', 'BMI', 'TBM', 'F16C', 'FMA', 'FSGSBASE'],
#           AMD Excavator Family 15h (4th-gen)      https://en.wikipedia.org/wiki/Excavator_(microarchitecture)
    'bdver4':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16', 'BMI', 'TBM', 'F16C', 'FMA', 'FSGSBASE', 'AVX2', 'BMI2', 'MOVBE'],
#           AMD Zen                                 https://en.wikipedia.org/wiki/Zen_(microarchitecture)
    'znver1':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16', 'BMI', 'TBM', 'F16C', 'FMA', 'FSGSBASE', 'AVX2', 'BMI2', 'MOVBE', 'ADCX', 'RDSEED', 'MWAITX', 'SHA', 'CLZERO', 'XSAVEC', 'XSAVES', 'CLFLUSHOPT', 'POPCNT'],
#           AMD Zen 2                               https://en.wikipedia.org/wiki/Zen_2
    'znver2':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', '3DNow!', 'enhanced 3DNow!', 'SSE3', 'SSE4A', 'ABM', 'SSSE3', 'SSE4.1', 'SSE4.2', 'FMA4', 'AVX', 'XOP', 'LWP', 'AES', 'PCL_MUL', 'CX16', 'BMI', 'TBM', 'F16C', 'FMA', 'FSGSBASE', 'AVX2', 'BMI2', 'MOVBE', 'ADCX', 'RDSEED', 'MWAITX', 'SHA', 'CLZERO', 'XSAVEC', 'XSAVES', 'CLFLUSHOPT', 'POPCNT', 'CLWB'],

# VIA
    'eden-x2':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3'],
    'eden-x4':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4.1', 'SSE4.2', 'AVX', 'AVX2'],

    'nano':           ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3'],
    'nano-1000':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3'], 
    'nano-2000':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3'], 
    'nano-3000':      ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4.1'], 
    'nano-x2':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4.1'], 
    'nano-x4':        ['64-bit extensions', 'MMX', 'SSE', 'SSE2', 'SSE3', 'SSSE3', 'SSE4.1'], 
}


marchs_aliases = {
    'k8':            'k8',
    'opteron':       'k8',
    'athlon64':      'k8',
    'athlon-fx':     'k8',
    'k8-sse3':       'k8-sse3',
    'opteron-sse3':  'k8-sse3',
    'athlon64-sse3': 'k8-sse3',
    'k10':           'amdfam10',
    'amdfam10':      'amdfam10',
    'barcelona':     'amdfam10',
    'bobcat':        'btver1',
    'jaguar':        'btver2',
    # 'puma':          'btver2',
    # 'leopard':       'btver3',
    # 'margay':        'btver4',
    'bulldozer':      'bdver1',
    'piledriver':     'bdver2',
    'steamroller':    'bdver3',
    'excavator':      'bdver4',

    'knightslanding': 'knl',
    'atom':           'bonnell',
    'kabylake':       'skylake',
}

def remove_ext(data, ext):
    for _, value in data.items():
        if ext in value:
            value.remove(ext)


marchs_families = {}
marchs_families['gcc']= {}
marchs_families['apple-clang']= {}
marchs_families['clang']= {}
marchs_families['msvc']= {}
marchs_families['mingw']= {}

# msvc 2019
    # (x86)
        # /arch:[IA32|SSE|SSE2|AVX|AVX2]  
    # (x64)
        # /arch:[AVX|AVX2]  
    # (ARM)
        # /arch:[ARMv7VE|VFPv4]  

# msvc 2017
    # (x86)
        # /arch:[IA32|SSE|SSE2|AVX|AVX2]  
    # (x64)
        # /arch:[AVX|AVX2]  
    # (ARM)
        # /arch:[ARMv7VE|VFPv4]  

marchs_families['msvc'][14] = {
    'amd_high':   ['x86-64', 'bdver1', 'bdver4'],
    'amd_low':    ['x86-64', 'btver2'],
    'intel_core': ['x86-64', 'sandybridge', 'haswell'],
    'via_eden':   ['x86-64', 'eden-x4'],
}

marchs_families['msvc'][15] = copy.deepcopy(marchs_families['msvc'][14])
marchs_families['msvc'][16] = copy.deepcopy(marchs_families['msvc'][15])


msvc_to_extensions = {
    'x86-64':        None,
    'bdver1':       'AVX',
    'bdver4':       'AVX2',
    'btver2':       'AVX',
    'sandybridge':  'AVX',
    'haswell':      'AVX2',
    'eden-x4':      'AVX2',
}

def msvc_to_ext(march):
    march_str = str(march)
    # print(march_str)
    if march_str in msvc_to_extensions:
        return msvc_to_extensions[march_str]
    return None

marchs_families_base = {
    'amd_high':   ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'bdver1', 'bdver2', 'bdver3', 'bdver4'],
    'amd_low':    ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'btver1', 'btver2'],
    # 'intel_core': ['x86-64', 'core2', 'penryn', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell'],
    'intel_core': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell'],
    'intel_atom': ['x86-64', 'core2', 'bonnell', 'silvermont'],
}

marchs_families_clang_base = copy.deepcopy(marchs_families_base)
marchs_families_clang_base['intel_high'] = copy.deepcopy(marchs_families_clang_base['intel_core'])
marchs_families_clang_base['intel_core'].extend(['skylake', 'skylake-avx512', 'cannonlake'])
marchs_families_clang_base['intel_high'].extend(['knl'])

marchs_families['clang'][4.0] = copy.deepcopy(marchs_families_clang_base)
marchs_families['clang'][4.0]['amd_high'].extend(['znver1'])

marchs_families['apple-clang'][9.1] = copy.deepcopy(marchs_families['clang'][4.0])
marchs_families['apple-clang'][9.1]['intel_atom'].extend(['goldmont'])

marchs_families['gcc'][4] = copy.deepcopy(marchs_families_base)

marchs_families['gcc'][5] = copy.deepcopy(marchs_families['gcc'][4])
marchs_families['gcc'][5]['intel_high'] = copy.deepcopy(marchs_families['gcc'][5]['intel_core'])
marchs_families['gcc'][5]['intel_high'].extend(['knl'])

marchs_families['mingw'][7] = copy.deepcopy(marchs_families['gcc'][5])
marchs_families['mingw'][7]['intel_core'].extend(['skylake'])
marchs_families['mingw'][7]['amd_high'].extend(['znver1'])

marchs_families['gcc'][6] = copy.deepcopy(marchs_families['mingw'][7])
marchs_families['gcc'][6]['intel_core'].extend(['skylake-avx512'])
marchs_families['gcc'][6]['amd_high'].extend(['znver1'])

marchs_families['mingw'][6] = copy.deepcopy(marchs_families['gcc'][6])
remove_ext(marchs_families['mingw'][6], "skylake-avx512")

marchs_families['mingw'][5] = copy.deepcopy(marchs_families['gcc'][5])

marchs_families['gcc'][7] = copy.deepcopy(marchs_families['gcc'][6])
marchs_families['gcc'][7]['via_eden'] = ['x86-64', 'eden-x2', 'eden-x4']
marchs_families['gcc'][7]['via_nano'] = ['x86-64', 'nano', 'nano-1000', 'nano-2000', 'nano-3000', 'nano-x2', 'nano-x4']

marchs_families['gcc'][8] = copy.deepcopy(marchs_families['gcc'][7])
marchs_families['gcc'][8]['intel_high'].extend(['knm'])
marchs_families['gcc'][8]['intel_core'].extend(['cannonlake', 'icelake-client', 'icelake-server'])

marchs_families['gcc'][9] = copy.deepcopy(marchs_families['gcc'][8])
marchs_families['gcc'][9]['intel_atom'].extend(['goldmont', 'goldmont-plus', 'tremont'])
marchs_families['gcc'][9]['intel_core'].extend(['cascadelake'])



marchs_families['mingw'][8] = copy.deepcopy(marchs_families['gcc'][7])
marchs_families['mingw'][8]['intel_high'].extend(['knm'])
remove_ext(marchs_families['mingw'][8], "skylake-avx512")

#TODO(fernando): Check MinGW9
marchs_families['mingw'][9] = copy.deepcopy(marchs_families['gcc'][8])


# marchs_families['clang'][4.0] = copy.deepcopy(marchs_families['apple-clang'][9.1])
marchs_families['clang'][5.0] = copy.deepcopy(marchs_families['apple-clang'][9.1])
marchs_families['clang'][6.0] = copy.deepcopy(marchs_families['clang'][5.0])
marchs_families['clang'][7.0] = copy.deepcopy(marchs_families['clang'][6.0])
marchs_families['clang'][8] = copy.deepcopy(marchs_families['clang'][7.0])
marchs_families['clang'][9] = copy.deepcopy(marchs_families['clang'][8])

marchs_families['apple-clang'][11.0] = copy.deepcopy(marchs_families['apple-clang'][9.1])
marchs_families['apple-clang'][10.0] = copy.deepcopy(marchs_families['apple-clang'][9.1])
marchs_families['apple-clang'][9.0] = copy.deepcopy(marchs_families['apple-clang'][9.1])
marchs_families['apple-clang'][8.3] = copy.deepcopy(marchs_families_clang_base)
marchs_families['apple-clang'][8.1] = copy.deepcopy(marchs_families_clang_base)
marchs_families['apple-clang'][7.3] = copy.deepcopy(marchs_families_clang_base)
remove_ext(marchs_families['apple-clang'][7.3], "skylake")
remove_ext(marchs_families['apple-clang'][7.3], "cannonlake")
remove_ext(marchs_families['apple-clang'][7.3], "skylake-avx512")



def get_supported_architectures():
    return ['x86_64']

def get_available_microarchitectures():
    return ['haswell']

def is_supported_architecture(x):
    return x in get_supported_architectures()

def get_supported_compilers():
    res = []
    for x in marchs_families:
        res.append(x)
    res.sort()
    return res

def is_supported_compiler(os, x):
    x = adjust_compiler_name(os, x)
    return x in get_supported_compilers()

def get_supported_compiler_versions(os, compiler):
    compiler = adjust_compiler_name(os, compiler)
    res = []
    for x in marchs_families[compiler]:
        res.append(x)
    res.sort()
    return res

def is_supported_compiler_version(os, compiler, x):
    return x in get_supported_compiler_versions(os, compiler)

def is_compiler_version_newer(os, compiler, x):
    latest_supported_version = get_supported_compiler_versions(os, compiler)[-1]
    return x > latest_supported_version    

def is_known_microarchitecture(x):
    full = get_full_family()

    for key, value in full.items():
        if x in value:
            return True

    return False






def get_full_family():
    return marchs_families['gcc'][9]

def translate_alias(alias):
    alias_str = str(alias)
    if alias_str in marchs_aliases:
        return marchs_aliases[alias_str]
    else:
        return alias

def adjust_compiler_name(os, compiler):
    if os == "Windows" and compiler == "gcc":
        return "mingw"
    if compiler == "Visual Studio":
        return "msvc"
        
    return compiler
        
def get_march_basis(march_detected, os, compiler, compiler_version, full, default):
    compiler = adjust_compiler_name(os, compiler)

    if compiler not in marchs_families:
        return default

    if compiler_version not in marchs_families[compiler]:
        return default

    data = marchs_families[compiler][compiler_version]
    march_detected = translate_alias(march_detected)

    for key, value in data.items():
        if march_detected in value:
            return march_detected
        else:
            if march_detected in full[key]:
                idx = full[key].index(march_detected)
                idx = min(idx, len(value) - 1)
                return value[idx]

    return default

def get_march(march_detected, os, compiler, compiler_version):
    full = get_full_family()
    default = 'x86-64'
    return get_march_basis(march_detected, os, compiler, compiler_version, full, default)

def march_exists_in(march_detected, os, compiler, compiler_version):
    compiler = adjust_compiler_name(os, compiler)

    if compiler not in marchs_families:
        return False

    if compiler_version not in marchs_families[compiler]:
        return False

    data = marchs_families[compiler][compiler_version]
    march_detected = translate_alias(march_detected)

    for _, value in data.items():
        if march_detected in value:
            return True

    return False

def march_exists_full(march_detected):
    data = get_full_family()
    march_detected = translate_alias(march_detected)

    for _, value in data.items():
        if march_detected in value:
            return True

    return False

def marchs_full_list_basis(data):
    ret = []
    for _, value in data.items():
        ret.extend(value)
    return list(set(ret))

def marchs_full_list():
    full = get_full_family()
    return marchs_full_list_basis(full)

def marchs_compiler_list(os, compiler, compiler_version):
    compiler = adjust_compiler_name(os, compiler)

    if compiler not in marchs_families:
        return []

    if compiler_version not in marchs_families[compiler]:
        return []

    data = marchs_families[compiler][compiler_version]
    return marchs_full_list_basis(data)

def filter_valid_exts(os, compiler, compiler_version, exts):
    data = marchs_compiler_list(os, compiler, compiler_version)

    ret = []
    for x in exts:
        if x in data:
            ret.append(x)

    return list(set(ret))

def march_close_name(march_incorrect): #, compiler, compiler_version):
    # full = get_full_family()
    return difflib.get_close_matches(march_incorrect, marchs_full_list())
    



# def march_conan_manip(conanobj):
#     if conanobj.settings.arch != "x86_64":
#         return

#     if conanobj.options.microarchitecture == "_DUMMY_":
#         conanobj.options.microarchitecture = get_cpu_microarchitecture().replace('_', '-')
#         if get_cpuid() == None:
#             march_from = 'default'
#         else:
#             march_from = 'taken from cpuid'
#     else:
#         march_from = 'user defined'

#         # conanobj.output.error("%s" % (marchs_full_list(),))

#         if not march_exists_full(conanobj.options.microarchitecture):
#             close = march_close_name(str(conanobj.options.microarchitecture))
#             if not conanobj.options.fix_march:
#                 # conanobj.output.error("fixed_march: %s" % (fixed_march,))

#                 if len(close) > 0:
#                     raise Exception ("Microarchitecture '%s' is not recognized. Did you mean '%s'?." % (conanobj.options.microarchitecture, close[0]))
#                     # conanobj.output.error("Microarchitecture '%s' is not recognized. Did you mean '%s'?." % (conanobj.options.microarchitecture, close[0]))
#                     # sys.exit
#                 else:
#                     raise Exception ("Microarchitecture '%s' is not recognized." % (conanobj.options.microarchitecture,))
#                     # conanobj.output.error("Microarchitecture '%s' is not recognized." % (conanobj.options.microarchitecture,))
#                     # sys.exit
#             else:
#                 if len(close) > 0:
#                     fixed_march = get_march(close[0], str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version)))
#                 else:
#                     fixed_march = get_march(conanobj.options.microarchitecture, str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version)))

#                 conanobj.output.warn("Microarchitecture '%s' is not recognized, but it will be automatically fixed to '%s'." % (conanobj.options.microarchitecture, fixed_march))
#                 conanobj.options.microarchitecture = fixed_march


#         if not march_exists_in(conanobj.options.microarchitecture, str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version))):
#             # TODO(fernando): print possible options for the platform (os, compiler, ...)
        
#             fixed_march = get_march(conanobj.options.microarchitecture, str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version)))

#             if not conanobj.options.fix_march:
#                 raise Exception ("Microarchitecture '%s' is not supported by your compiler, you could use '%s'. Compiler information: %s -- %s -- %s" % (conanobj.options.microarchitecture,fixed_march), str(conanobj.settings.os), str(conanobj.settings.compiler), str(float(str(conanobj.settings.compiler.version))))

#                 # conanobj.output.error("Microarchitecture '%s' is not supported by your compiler, you could use '%s'." % (conanobj.options.microarchitecture,fixed_march))
#                 # sys.exit
#             else:
#                 conanobj.output.warn("Microarchitecture '%s' is not supported by your compiler, but it will be automatically fixed to '%s'." % (conanobj.options.microarchitecture, fixed_march))


#     fixed_march = get_march(conanobj.options.microarchitecture, str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version)))

#     if march_from == 'user defined':
#         conanobj.output.info("User selected microarchitecture (%s): %s" % (march_from, conanobj.options.microarchitecture))
#     else:
#         conanobj.output.info("Detected microarchitecture (%s): %s" % (march_from, conanobj.options.microarchitecture))

#     if conanobj.options.microarchitecture != fixed_march:
#         conanobj.options.microarchitecture = fixed_march
#         conanobj.output.info("Corrected microarchitecture for compiler: %s" % (conanobj.options.microarchitecture,))


def march_conan_manip(conanobj):
    if conanobj.settings.arch != "x86_64":
        return (None, None)

    march_from = 'taken from cpuid'
    march_id = get_architecture_id()
    microarchitecture = get_cpu_microarchitecture().replace('_', '-')

    if conanobj.options.get_safe("march_id") is not None:
        if conanobj.options.march_id == "_DUMMY_":
            conanobj.options.march_id = march_id
        else:
            march_id = conanobj.options.march_id
            march_from = 'user defined'
            #TODO(fernando): check for march_id errors

    microarchitecture = get_march(microarchitecture, str(conanobj.settings.os), str(conanobj.settings.compiler), float(str(conanobj.settings.compiler.version)))
    conanobj.output.info("Detected microarchitecture (%s): %s" % ("taken from cpuid", microarchitecture))
    conanobj.output.info("Detected microarchitecture ID (%s): %s" % (march_from, march_id))

    return (march_id, microarchitecture)


def pass_march_to_compiler(conanobj, cmake):

    if conanobj.options.get_safe("march_id") is not None:
        march_id = str(conanobj.options.march_id)
        flags = get_compiler_flags_arch_id(march_id, 
                                str(conanobj.settings.os), 
                                str(conanobj.settings.compiler), 
                                float(str(conanobj.settings.compiler.version)))

        conanobj.output.info("Compiler flags: %s" % flags)

        cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " " + flags
        cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " " + flags

    # if conanobj.settings.compiler != "Visual Studio":
    #     gcc_march = str(conanobj.options.microarchitecture)
    #     cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " -march=" + gcc_march
    #     cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " -march=" + gcc_march
    # else:
    #     ext = msvc_to_ext(str(conanobj.options.microarchitecture))

    #     if ext is not None:
    #         cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " /arch:" + ext
    #         cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " /arch:" + ext



def get_conan_get(package, remote=None, default=None):
    try:
        if remote is None:
            params = ["conan", "get", package]
        else:
            params = ["conan", "get", package, "-r", remote]

        res = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = res.communicate()
        if output:
            if res.returncode == 0:
                return output.decode("utf-8")
        return default
    except OSError: # as e:
        return default
    except:
        return default

def get_alias_version(package, remote=None, default=None):
    conan_alias = get_conan_get(package, remote, default)
    conan_alias = conan_alias.split('\n')[4:][0]
    return conan_alias[12:].replace('"', '')


def get_recipe_dir():
    recipe_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.normpath(recipe_dir + os.sep + os.pardir)

def get_conan_requirements_path():
    return os.path.normpath(get_recipe_dir() + os.sep + 'conan_requirements')

def get_requirements_from_file():
    conan_requirements = get_conan_requirements_path()
    if os.path.exists(conan_requirements):
        # print("conan_requirements exists")
        with open(conan_requirements, 'r') as f:
            return [line.rstrip('\n') for line in f]
    # else:
    #     # print("-----------------------------------------------")
    #     # print("conan_requirements DOESNT exists")
    #     # print(os.getcwd())

    #     recipe_dir = get_recipe_dir()
    #     # print(recipe_dir)
    #     # print(get_conan_requirements_path())

    #     # files = [f for f in os.listdir('.') if os.path.isfile(f)]
    #     files = [f for f in recipe_dir if os.path.isfile(f)]
    #     for f in files:
    #         print(f)

    return []


def try_remove_glibcxx_supports_cxx11_abi(obj):
    if obj.options.get_safe("glibcxx_supports_cxx11_abi") is None:
        return
    del obj.options.glibcxx_supports_cxx11_abi

class KnuthCxx11ABIFixer(ConanFile):

    def configure(self, pure_c=False):
        ConanFile.configure(self)

        # self.output.info("configure() - glibcxx_supports_cxx11_abi: %s" % (self.options.get_safe("glibcxx_supports_cxx11_abi"),))

        if pure_c:
            del self.settings.compiler.libcxx               #Pure-C Library
            try_remove_glibcxx_supports_cxx11_abi(self)
            return

        if self.options.get_safe("glibcxx_supports_cxx11_abi") is None:
            return

        if not (self.settings.compiler == "gcc" or self.settings.compiler == "clang"):
            # self.output.info("glibcxx_supports_cxx11_abi option is only valid for 'gcc' or 'clang' compilers, deleting it. Your compiler is: '%s'." % (str(self.settings.compiler),))
            del self.options.glibcxx_supports_cxx11_abi
            return

        if self.settings.compiler == "gcc" and self.settings.os == "Windows":
            # self.output.info("glibcxx_supports_cxx11_abi option is not valid for 'MinGW' compiler, deleting it. Your compiler is: '%s, %s'." % (str(self.settings.compiler),str(self.settings.os)))
            del self.options.glibcxx_supports_cxx11_abi
            return

        if self.settings.get_safe("compiler.libcxx") is None:
            # self.output.info("glibcxx_supports_cxx11_abi option is only useful for 'libstdc++' or 'libstdc++11', deleting it. Your compiler.libcxx is: '%s'." % (str(self.settings.compiler.libcxx),))
            del self.options.glibcxx_supports_cxx11_abi
            return

        if not (str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11"):
            # self.output.info("glibcxx_supports_cxx11_abi option is only useful for 'libstdc++' or 'libstdc++11', deleting it. Your compiler.libcxx is: '%s'." % (str(self.settings.compiler.libcxx),))
            del self.options.glibcxx_supports_cxx11_abi
            return

        if self.options.get_safe("glibcxx_supports_cxx11_abi") != "_DUMMY_":
            return

        abi_support = glibcxx_supports_cxx11_abi()
        # self.output.info("glibcxx_supports_cxx11_abi(): %s" % (abi_support,))
        
        self.options.glibcxx_supports_cxx11_abi = abi_support
        self.options["*"].glibcxx_supports_cxx11_abi = self.options.glibcxx_supports_cxx11_abi
        # self.output.info("configure() - 2 - glibcxx_supports_cxx11_abi: %s" % (self.options.get_safe("glibcxx_supports_cxx11_abi"),))
        self.libcxx_changed = True

        # libcxx_old = str(self.settings.compiler.libcxx)
        # if str(self.settings.compiler.libcxx) == "libstdc++" and abi_support:
        #     self.settings.compiler.libcxx = "libstdc++11"
        #     # self.settings["*"].compiler.libcxx = self.settings.compiler.libcxx
        #     self.output.info("compiler.libcxx changed from %s to %s" % (libcxx_old, str(self.settings.compiler.libcxx),))

        # if str(self.settings.compiler.libcxx) == "libstdc++11" and not abi_support:
        #     self.settings.compiler.libcxx = "libstdc++"
        #     # self.settings["*"].compiler.libcxx = self.settings.compiler.libcxx
        #     self.output.info("compiler.libcxx changed from %s to %s" % (libcxx_old, str(self.settings.compiler.libcxx),))


    def package_id(self):
        ConanFile.package_id(self)
        # self.output.info("package_id() - glibcxx_supports_cxx11_abi: %s" % (self.options.get_safe("glibcxx_supports_cxx11_abi"),))
        # self.info.settings.compiler.libcxx = "libstdc++11"

        #For Knuth Packages libstdc++ and libstdc++11 are the same
        if self.settings.compiler == "gcc" or self.settings.compiler == "clang":
            if self.settings.get_safe("compiler.libcxx") is not None:
                if str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11":
                    # self.info.settings.compiler.libcxx = "ANY"
                    self.info.settings.compiler.libcxx = "libstdc++"

class KnuthConanFile(KnuthCxx11ABIFixer):
    @property
    def conan_req_version(self):
        return get_conan_req_version(self.recipe_dir())

    def config_options(self):
        KnuthCxx11ABIFixer.config_options(self)

        if self.settings.arch != "x86_64":
            self.output.info("microarchitecture is disabled for architectures other than x86_64, your architecture: %s" % (self.settings.arch,))
            self.options.remove("microarchitecture")
            self.options.remove("fix_march")

        if self.settings.compiler == "Visual Studio":
            self.options.remove("fPIC")
            if self.is_shared:
                self.options.remove("shared")

    def _warn_missing_options(self):
        if self.settings.arch == "x86_64" and self.options.get_safe("march_id") is None:
            self.output.warn("**** The recipe does not implement the march_id option. ****")

    def configure(self, pure_c=False):
        if self.conan_req_version != None and Version(conan_version) < Version(self.conan_req_version):
            raise Exception ("Conan version should be greater or equal than %s. Detected: %s." % (self.conan_req_version, conan_version))

        # self.output.info("libcxx: %s" % (str(self.settings.compiler.libcxx),))
        KnuthCxx11ABIFixer.configure(self, pure_c)

        if self.options.get_safe("currency") is not None:
            self.options["*"].currency = self.options.currency
            self.output.info("Compiling for currency: %s" % (self.options.currency,))

        if self.options.get_safe("db") is not None:
            self.options["*"].db = self.options.db
            self.output.info("Compiling for DB: %s" % (self.options.db,))
        
        self._warn_missing_options()

        if self.settings.arch == "x86_64":
            # if self.options.get_safe("microarchitecture") is not None and self.options.microarchitecture == "_DUMMY_":
            #     del self.options.fix_march

            march_id, microarchitecture = march_conan_manip(self)
            self.options["*"].march_id = march_id
            self.options["*"].microarchitecture = microarchitecture

            if self.options.get_safe("march_id") is not None:
                self.options.march_id = march_id

            if self.options.get_safe("microarchitecture") is not None:
                self.options.microarchitecture = microarchitecture

            # self.output.info("Vendor ID: %s" % vendorID())
            # self.output.info("Brand name: %s" % brandName())
            # self.output.info("Cache line: %s" % cacheLine())
            # self.output.info("Family model: %s, %s" % familyModel())
            # self.output.info("Threads per core: %s" % threadsPerCore())
            # self.output.info("Logical cores: %s" % logicalCores())
            # self.output.info("Physical cores: %s" % physicalCores())
            # self.output.info("Logical CPU: %s" % LogicalCPU())
            # self.output.info("VM: %s" % VM())
            # self.output.info("Hyperthreading: %s" % Hyperthreading())
            # # self.output.info("This computer microarchitecture: %s%s" % cpuid.cpu_microarchitecture())
            # # self.output.info("This computer microarchitecture ID: %s" % get_architecture_id())
            # # self.output.info("This computer extensions -------------------------")
            # exts = get_available_extensions()
            # exts_names = extensions_to_names(exts)
            # self.output.info(", ".join(exts_names))
            #TODO(fernando): print build march_id and extensions

            if self.options.get_safe("march_id") is not None:
                self.output.info("Building microarchitecture ID: %s" % march_id)
                exts = decode_extensions(march_id)
                exts_names = extensions_to_names(exts)
                self.output.info(", ".join(exts_names))


    def package_id(self):
        KnuthCxx11ABIFixer.package_id(self)

        # self.info.options.verbose = "ANY"
        # self.info.options.fix_march = "ANY"
        # self.info.options.cxxflags = "ANY"
        # self.info.options.cflags = "ANY"
        # self.info.options.microarchitecture = "ANY"
        # self.info.options.tests = "ANY"
        # self.info.options.examples = "ANY"
        # self.info.options.cmake_export_compile_commands = "ANY"

        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")

        # self.output.warn(self.info.options)
        # self.output.warn(self.options.get_safe("verbose"))
        # self.output.warn(self.options.get_safe("fix_march"))
        # self.output.warn(self.options.get_safe("cxxflags"))
        # self.output.warn(self.options.get_safe("cflags"))
        # self.output.warn(self.options.get_safe("microarchitecture"))
        # self.output.warn(self.options.get_safe("tests"))
        # self.output.warn(self.options.get_safe("tools"))
        # self.output.warn(self.options.get_safe("examples"))
        # self.output.warn(self.options.get_safe("cmake_export_compile_commands"))

        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")

        if self.options.get_safe("verbose") is not None:
            self.info.options.verbose = "ANY"

        if self.options.get_safe("fix_march") is not None:
            self.info.options.fix_march = "ANY"

        if self.options.get_safe("cxxflags") is not None:
            self.info.options.cxxflags = "ANY"

        if self.options.get_safe("cflags") is not None:
            self.info.options.cflags = "ANY"

        if self.options.get_safe("microarchitecture") is not None:
            self.info.options.microarchitecture = "ANY"

        if self.options.get_safe("tests") is not None:
            self.info.options.tests = "ANY"

        if self.options.get_safe("tools") is not None:
            self.info.options.tools = "ANY"

        if self.options.get_safe("examples") is not None:
            self.info.options.examples = "ANY"

        if self.options.get_safe("cmake_export_compile_commands") is not None:
            self.info.options.cmake_export_compile_commands = "ANY"


        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")
        # self.output.warn("-----------------------------------------------------------------")

        # self.output.warn(self.info.options)

    def _cmake_database(self, cmake):
        if self.options.get_safe("db") is None:
            return

        if self.options.db == "legacy":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "legacy_full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(True)
            cmake.definitions["DB_SPENDS"] = option_on_off(True)
            cmake.definitions["DB_HISTORY"] = option_on_off(True)
            cmake.definitions["DB_STEALTH"] = option_on_off(True)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_LEGACY"] = option_on_off(True)
            cmake.definitions["DB_NEW"] = option_on_off(False)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "pruned":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "default":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(True)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(False)
        elif self.options.db == "full":
            cmake.definitions["DB_TRANSACTION_UNCONFIRMED"] = option_on_off(False)
            cmake.definitions["DB_SPENDS"] = option_on_off(False)
            cmake.definitions["DB_HISTORY"] = option_on_off(False)
            cmake.definitions["DB_STEALTH"] = option_on_off(False)
            cmake.definitions["DB_UNSPENT_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_LEGACY"] = option_on_off(False)
            cmake.definitions["DB_NEW"] = option_on_off(True)
            cmake.definitions["DB_NEW_BLOCKS"] = option_on_off(False)
            cmake.definitions["DB_NEW_FULL"] = option_on_off(True)

    def cmake_basis(self, pure_c=False):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = option_on_off(True)
        cmake.definitions["NO_CONAN_AT_ALL"] = option_on_off(False)
        cmake.verbose = self.options.verbose
        cmake.definitions["ENABLE_SHARED"] = option_on_off(self.is_shared)
        cmake.definitions["ENABLE_POSITION_INDEPENDENT_CODE"] = option_on_off(self.fPIC_enabled)

        if self.options.get_safe("tests") is not None:
            cmake.definitions["WITH_TESTS"] = option_on_off(self.options.tests)
            cmake.definitions["WITH_TESTS_NEW"] = option_on_off(self.options.tests)

        if self.options.get_safe("examples") is not None:
            cmake.definitions["WITH_EXAMPLES"] = option_on_off(self.options.examples)

        if self.options.get_safe("tools") is not None:
            cmake.definitions["WITH_TOOLS"] = option_on_off(self.options.tools)

        if self.options.get_safe("cxxflags") is not None and self.options.cxxflags != "_DUMMY_":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " " + str(self.options.cxxflags)
        if self.options.get_safe("cflags") is not None and self.options.cflags != "_DUMMY_":
            cmake.definitions["CONAN_C_FLAGS"] = cmake.definitions.get("CONAN_C_FLAGS", "") + " " + str(self.options.cflags)

        if self.settings.compiler != "Visual Studio":
            # cmake.definitions["CONAN_CXX_FLAGS"] += " -Wno-deprecated-declarations"
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " -Wno-deprecated-declarations"
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CONAN_CXX_FLAGS"] = cmake.definitions.get("CONAN_CXX_FLAGS", "") + " /DBOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"

        if self.options.get_safe("microarchitecture") is not None:
            cmake.definitions["MICROARCHITECTURE"] = self.options.microarchitecture

        if self.options.get_safe("march_id") is not None:
            cmake.definitions["MARCH_ID"] = self.options.march_id

        cmake.definitions["KTH_PROJECT_VERSION"] = self.version

        if self.options.get_safe("currency") is not None:
            cmake.definitions["CURRENCY"] = self.options.currency

        self._cmake_database(cmake)

        if self.options.get_safe("cmake_export_compile_commands") is not None and self.options.cmake_export_compile_commands:
            cmake.definitions["CMAKE_EXPORT_COMPILE_COMMANDS"] = option_on_off(self.options.cmake_export_compile_commands)

        if not pure_c:
            if self.settings.compiler == "gcc":
                if float(str(self.settings.compiler.version)) >= 5:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)
                else:
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(True)
            elif self.settings.compiler == "clang":
                if str(self.settings.compiler.libcxx) == "libstdc++" or str(self.settings.compiler.libcxx) == "libstdc++11":
                    cmake.definitions["NOT_USE_CPP11_ABI"] = option_on_off(False)

        pass_march_to_compiler(self, cmake)
        # self.output.info("CONAN_CXX_FLAGS: %s" % (cmake.definitions["CONAN_CXX_FLAGS"], ))
        # self.output.info("cmake.command_line: %s" % (cmake.command_line, ))
        return cmake


# --------------










    def add_reqs(self, reqs):
        for r in reqs:
            self.requires(r % (self.user, self.channel))

    def knuth_requires(self, default_reqs):
        file_reqs = get_requirements_from_file()
        # print(file_reqs)

        if len(file_reqs) != 0:
            self.add_reqs(file_reqs)
        else:
            self.add_reqs(default_reqs)

    @property
    def msvc_mt_build(self):
        # return "MT" in str(self.settings.compiler.runtime)
        return "MT" in str(self.settings.get_safe("compiler.runtime"))

    @property
    def fPIC_enabled(self):
        if self.options.get_safe("fPIC") is None: 
            return False

        if self.settings.compiler == "Visual Studio":
            return False

        return self.options.fPIC

    # Version Node-Cint
    # @property
    # def is_shared(self):
    #     # if self.settings.compiler == "Visual Studio" and self.msvc_mt_build:
    #     #     return False
    #     # else:
    #     #     return self.options.shared
    #     return self.options.shared

    @property
    def is_shared(self):
        if self.options.get_safe("shared") is None: 
            return False

        if self.options.shared and self.msvc_mt_build:
            return False
        else:
            return self.options.shared



    # @property
    # def channel(self):
    #     if not self._channel:
    #         if not self._channel:
    #             self._channel = get_channel()
    #         if not self._channel:
    #             raise ConanException("CONAN_CHANNEL environment variable not defined, "
    #                                  "but self.channel is used in conanfile")
    #     return self._channel

    # @property
    # def user(self):
    #     if not self._user:
    #         self._user = os.getenv("CONAN_USERNAME")
    #         if not self._user:
    #             self._user = get_user()
    #         if not self._user:
    #             raise ConanException("CONAN_USERNAME environment variable not defined, "
    #                                  "but self.user is used in conanfile")
    #     return self._user

    @property
    def channel(self):
        try:
            return super(KnuthConanFile, self).channel
        except ConanException:
            return get_channel(self.recipe_dir())

    @property
    def user(self):
        try:
            return super(KnuthConanFile, self).user
        except ConanException:
            return get_user(self.recipe_dir())



# marchs = filter_valid_exts('Windows', 'Visual Studio', 15, ['x86-64', 'sandybridge', 'ivybridge', 'haswell', 'skylake', 'skylake-avx512'])
# print(marchs)


# >>> difflib.get_close_matches('anlmal', ['car', 'animal', 'house', 'animation'])

# --------------------------------------------------------------------------------

# def print_extensions():
#     ma = get_cpu_microarchitecture()
#     print(ma)
#     print(marchs_extensions[ma])

# print_extensions()
# print( get_march('broadwell', 'gcc', 4) )
# print( get_march('skylake', 'gcc', 4) )
# print( get_march('skylake-avx512', 'gcc', 4) )

# print( get_march('broadwell', 'gcc', 5) )
# print( get_march('skylake', 'gcc', 5) )
# print( get_march('skylake-avx512', 'gcc', 5) )

# print( get_march('broadwell', 'gcc', 6) )
# print( get_march('skylake', 'gcc', 6) )
# print( get_march('skylake-avx512', 'gcc', 6) )

# print( get_march('broadwell', 'gcc', 7) )
# print( get_march('skylake', 'gcc', 7) )
# print( get_march('skylake-avx512', 'gcc', 7) )

# print( get_march('broadwell', 'gcc', 8) )
# print( get_march('skylake', 'gcc', 8) )
# print( get_march('skylake-avx512', 'gcc', 8) )

# print( get_march('knightslanding', 'gcc', 8) )
# print( get_march('excavator', 'gcc', 8) )
# print( get_march('bdver4', 'gcc', 8) )



# --------------------------------------------------------------------------------

# marchs_families_apple91_temp = {
#     'amd_high':   ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'bdver1', 'bdver2', 'bdver3', 'bdver4', 'znver1'],
#     'amd_low':    ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'btver1', 'btver2'],

#     'intel_core': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell', 'skylake', 'skylake-avx512', 'cannonlake'],
#     'intel_atom': ['x86-64', 'core2', 'bonnell', 'silvermont', 'goldmont'],
#     'intel_high': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell', 'knl'],
# }

# marchs_families_gcc4_temp = {
#     'amd_high':   ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'bdver1', 'bdver2', 'bdver3', 'bdver4'],
#     'amd_low':    ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'btver1', 'btver2'],

#     'intel_core': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell'],
#     'intel_atom': ['x86-64', 'core2', 'bonnell', 'silvermont'],
#     # 'intel_high': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell'],
# }


# marchs_families_gcc8_temp = {
#     'amd_high':   ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'bdver1', 'bdver2', 'bdver3', 'bdver4', 'znver1'],
#     'amd_low':    ['x86-64', 'k8', 'k8-sse3', 'amdfam10', 'btver1', 'btver2'],

#     'intel_core': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell', 'skylake', 'skylake-avx512', 'cannonlake', 'icelake-client', 'icelake-server'],
#     'intel_atom': ['x86-64', 'core2', 'bonnell', 'silvermont'],
#     'intel_high': ['x86-64', 'core2', 'nehalem', 'westmere', 'sandybridge', 'ivybridge', 'haswell', 'broadwell', 'knl', 'knm'],

#     'via_eden':   ['x86-64', 'eden-x2', 'eden-x4'],
#     'via_nano':   ['x86-64', 'nano', 'nano-1000', 'nano-2000', 'nano-3000', 'nano-x2', 'nano-x4'],
# }


# print(marchs_families['gcc'][4])
# print()
# print(marchs_families['gcc'][5])
# print()
# print(marchs_families['gcc'][6])
# print()
# print(marchs_families['gcc'][7])
# print()
# print(marchs_families['gcc'][8])

# print(marchs_families['gcc'][4] == marchs_families_gcc4_temp)
# print(marchs_families['gcc'][8] == marchs_families_gcc8_temp)
# print(marchs_families['apple-clang'][9.1] == marchs_families_apple91_temp)


# --------------------------------------------------------------------------------


# GCC7 no tiene: knm, cannonlake, icelake-client, icelake-server
# GCC6 no tiene: ninguno de los VIA que tenemos
# GCC5 no tiene: skylake, skylake-avx512, znver1
# GCC4 no tiene: knl

# Apple LLVM version 9.1.0 (clang-902.0.39.1)
    # icelake-client
    # icelake-server
    # goldmont-plus
    # tremont
    # knm
    # eden-x2
    # eden-x4
    # nano
    # nano-1000
    # nano-2000
    # nano-3000
    # nano-x2
    # nano-x4



# https://gcc.gnu.org/onlinedocs/

    # https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html
    # echo "" | gcc -fsyntax-only -march=pepe -xc -
    # nocona core2 nehalem corei7 westmere sandybridge corei7-avx ivybridge core-avx-i haswell core-avx2 broadwell skylake skylake-avx512 bonnell atom silvermont slm knl x86-64 eden-x2 nano nano-1000 nano-2000 nano-3000 nano-x2 eden-x4 nano-x4 k8 k8-sse3 opteron opteron-sse3 athlon64 athlon64-sse3 athlon-fx amdfam10 barcelona bdver1 bdver2 bdver3 bdver4 znver1 btver1 btver2


# g++ --version
# g++ (Ubuntu 7.3.0-16ubuntu3~16.04.1) 7.3.0
# Copyright (C) 2017 Free Software Foundation, Inc.
# This is free software; see the source for copying conditions.  There is NO
# warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 
# echo "" | gcc -fsyntax-only -march=pepe -xc -
# cc1: note: valid arguments to '-march=' switch are: nocona core2 nehalem corei7 westmere sandybridge corei7-avx ivybridge core-avx-i haswell core-avx2 broadwell skylake skylake-avx512 bonnell atom silvermont slm knl x86-64 eden-x2 nano nano-1000 nano-2000 nano-3000 nano-x2 eden-x4 nano-x4 k8 k8-sse3 opteron opteron-sse3 athlon64 athlon64-sse3 athlon-fx amdfam10 barcelona bdver1 bdver2 bdver3 bdver4 znver1 btver1 btver2


# echo "" | clang -fsyntax-only -march=x86-64 -xc -




# clang --version
# Apple LLVM version 9.1.0 (clang-902.0.39.1)
# Target: x86_64-apple-darwin17.6.0
# Thread model: posix
# InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin



# Kaby Lake
#     Successor	
#         Desktop: Coffee Lake (2nd Optimization)
#                  Whiskey Lake (3rd Optimization)
#         Mobile:  Cannon Lake (Process)
#         Servers and Desktop: Cascade Lake (3rd Optimization)[4][5]

# Coffee Lake
#     Successor	
#         Desktop:    Whiskey Lake (3rd Optimization)
#         Mobile:     Cannon Lake (Process)
#         Ice Lake (Architecture)

# Whiskey Lake
#     Successor
# 	    Cannon Lake (Process)
#         Ice Lake (Architecture)

# Cannon Lake (Skymont)
#     Successor
#         Ice Lake (Architecture)

# Cascade Lake
#     Successor
#         Ice Lake (Architecture)

# Ice Lake
#     Successor
#     	Tiger Lake (Optimization)

# Tiger Lake
#     Successor	
#         Sapphire Rapids (unknown)

# Sapphire Rapids
#     Successor	

# Linea Knights
#     Polaris | Larrabee (LRB) | Rock Creek
#     Knights Ferry (KNF) 
#     Knights Corner (KNC) 
#     Knights Landing (KNL) | Knights Mill (KNM)
#     Knights Hill (KNH)
#     Knights Peak (KNP)

# Linea Atom
#     Bonnell         x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3
#     Saltwell        x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3
#     Silvermont      x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AES, PCLMUL, RDRND
#     Airmont         x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AES, PCLMUL, RDRND
#     Goldmont        x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AES, PCLMUL, RDRND, SHA
#     Goldmont Plus   x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AES, PCLMUL, RDRND, SHA
#     Tremont         x86-64, MOVBE, MMX, SSE, SSE2, SSE3, SSSE3, SSE4.1, SSE4.2, POPCNT, AES, PCLMUL, RDRND, SHA




# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


# 64-bit	
# MOVBE	                            https://www.felixcloutier.com/x86/movbe
# MMX	
# SSE	
# SSE2	
# SSE3	
# SSSE3	
# SSE4.1	
# SSE4.2
# SSE4a (AMD)	
# POPCNT (AMD's ABM)	
# LZCNT (AMD's ABM)
# PKU	
# AVX	
# AVX2	
# AES	
# PCLMUL	
# FSGSBASE
# RDRND
# FMA3
# FMA4
# "ABM (AMD)"	
# BMI	
# BMI2	
# "TBM (AMD)"	
# F16C
# RDSEED
# ADCX
# PREFETCHW
# CLFLUSHOPT
# XSAVE?
# XSAVEOPT?
# XSAVEC
# XSAVES

# AVX512F
# AVX512PF?
# AVX512ER?
# AVX512VL
# AVX512BW
# AVX512DQ
# AVX512CD
# AVX5124VNNIW?
# AVX5124FMAPS?
# AVX512VBMI
# AVX512IFMA
# AVX512VBMI2
# AVX512VPOPCNTDQ
# AVX512BITALG
# AVX512VNNI
# AVX512BF16
# AVX512VP2INTERSECT

# SHA
# CLWB
# ENCLV?
# UMIP
# PTWRITE?
# RDPID
# SGX?
# GFNI
# GFNI-SSE?
# VPCLMULQDQ
# VAES
# PCONFIG
# WBNOINVD
# MOVDIRI
# MOVDIR64B
# BFLOAT16
# 3DNow!
# enhanced 3DNow!
# "SSE prefetch??? Parece que es una version previa, no Full de SSE"	
# "XOP (AMD) ???"	
# "LWP (AMD) ???"	
# "CX16 (AMD) ???"	
# "MWAITX (AMD) ???"	
# "CLZERO (AMD) ???"
# "Extended MMX (AMD) https://en.wikipedia.org/wiki/Extended_MMX"
# PREFETCHWT1               #TODO(fernando): ver en que marchs se usa...


# ------------------------------------------------------------------------------------
#TODO(fernando): chequear las siguientes instrucciones a ver si las soportamos
	# CMOV:               "CMOV",               // i686 CMOV
	# NX:                 "NX",                 // NX (No-Execute) bit
	# AMD3DNOW:           "AMD3DNOW",           // AMD 3DNOW
	# AMD3DNOWEXT:        "AMD3DNOWEXT",        // AMD 3DNowExt
	# MMX:                "MMX",                // Standard MMX
	# MMXEXT:             "MMXEXT",             // SSE integer functions or AMD MMX ext
	# SSE:                "SSE",                // SSE functions
	# SSE2:               "SSE2",               // P4 SSE2 functions
	# SSE3:               "SSE3",               // Prescott SSE3 functions
	# SSSE3:              "SSSE3",              // Conroe SSSE3 functions
	# SSE4:               "SSE4.1",             // Penryn SSE4.1 functions
	# SSE4A:              "SSE4A",              // AMD Barcelona microarchitecture SSE4a instructions
	# SSE42:              "SSE4.2",             // Nehalem SSE4.2 functions
	# AVX:                "AVX",                // AVX functions
	# AVX2:               "AVX2",               // AVX functions
	# FMA3:               "FMA3",               // Intel FMA 3
	# FMA4:               "FMA4",               // Bulldozer FMA4 functions
	# XOP:                "XOP",                // Bulldozer XOP functions
	# F16C:               "F16C",               // Half-precision floating-point conversion
	# BMI1:               "BMI1",               // Bit Manipulation Instruction Set 1
	# BMI2:               "BMI2",               // Bit Manipulation Instruction Set 2
	# TBM:                "TBM",                // AMD Trailing Bit Manipulation
	# LZCNT:              "LZCNT",              // LZCNT instruction
	# POPCNT:             "POPCNT",             // POPCNT instruction
	# AESNI:              "AESNI",              // Advanced Encryption Standard New Instructions
	# CLMUL:              "CLMUL",              // Carry-less Multiplication
	# HTT:                "HTT",                // Hyperthreading (enabled)
	# HLE:                "HLE",                // Hardware Lock Elision
	# RTM:                "RTM",                // Restricted Transactional Memory
	# RDRAND:             "RDRAND",             // RDRAND instruction is available
	# RDSEED:             "RDSEED",             // RDSEED instruction is available
	# ADX:                "ADX",                // Intel ADX (Multi-Precision Add-Carry Instruction Extensions)
	# SHA:                "SHA",                // Intel SHA Extensions
	# AVX512F:            "AVX512F",            // AVX-512 Foundation
	# AVX512DQ:           "AVX512DQ",           // AVX-512 Doubleword and Quadword Instructions
	# AVX512IFMA:         "AVX512IFMA",         // AVX-512 Integer Fused Multiply-Add Instructions
	# AVX512PF:           "AVX512PF",           // AVX-512 Prefetch Instructions
	# AVX512ER:           "AVX512ER",           // AVX-512 Exponential and Reciprocal Instructions
	# AVX512CD:           "AVX512CD",           // AVX-512 Conflict Detection Instructions
	# AVX512BW:           "AVX512BW",           // AVX-512 Byte and Word Instructions
	# AVX512VL:           "AVX512VL",           // AVX-512 Vector Length Extensions
	# AVX512VBMI:         "AVX512VBMI",         // AVX-512 Vector Bit Manipulation Instructions
	# AVX512VBMI2:        "AVX512VBMI2",        // AVX-512 Vector Bit Manipulation Instructions, Version 2
	# AVX512VNNI:         "AVX512VNNI",         // AVX-512 Vector Neural Network Instructions
	# AVX512VPOPCNTDQ:    "AVX512VPOPCNTDQ",    // AVX-512 Vector Population Count Doubleword and Quadword
	# GFNI:               "GFNI",               // Galois Field New Instructions
	# VAES:               "VAES",               // Vector AES
	# AVX512BITALG:       "AVX512BITALG",       // AVX-512 Bit Algorithms
	# VPCLMULQDQ:         "VPCLMULQDQ",         // Carry-Less Multiplication Quadword
	# AVX512BF16:         "AVX512BF16",         // AVX-512 BFLOAT16 Instruction
	# AVX512VP2INTERSECT: "AVX512VP2INTERSECT", // AVX-512 Intersect for D/Q
	# MPX:                "MPX",                // Intel MPX (Memory Protection Extensions)
	# ERMS:               "ERMS",               // Enhanced REP MOVSB/STOSB
	# RDTSCP:             "RDTSCP",             // RDTSCP Instruction
	# CX16:               "CX16",               // CMPXCHG16B Instruction
	# SGX:                "SGX",                // Software Guard Extensions
	# SGXLC:              "SGXLC",              // Software Guard Extensions Launch Control
	# IBPB:               "IBPB",               // Indirect Branch Restricted Speculation and Indirect Branch Predictor Barrier
	# STIBP:              "STIBP",              // Single Thread Indirect Branch Predictors
	# VMX:                "VMX",                // Virtual Machine Extensions

	# // Performance indicators
	# SSE2SLOW: "SSE2SLOW", // SSE2 supported, but usually not faster
	# SSE3SLOW: "SSE3SLOW", // SSE3 supported, but usually not faster
	# ATOM:     "ATOM",     // Atom processor, some SSSE3 instructions are slower
# ------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------
#TODO(fernando): Faltan implementar
# Provienen de GCC: https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html

# -mprfchw
# -mfxsr
# -mrtm
# -mhle
# -mwaitpkg
# -menqcmd
# -mcldemote
# -mcld
# -mvzeroupper
# -msahf
# -mshstk
# -mcrc32
# -mrecip
 
# ------------------------------------------------------------------------------------
#TODO(fernando): ver todas las instrucciones que se usan en el proyecto QEMU

# ------------------------------------------------------------------------------------

#TODO(fernando): chequear el soporte de AVX512 en VS2019, VS2017 y VS2015
# https://docs.microsoft.com/en-us/cpp/build/reference/arch-x64?view=vs-2019


# ------------------------------------------------------------------------------------
#TODO(fernando): ver todas las instrucciones que se usan en el proyecto Clang/LLVM
# https://clang.llvm.org/docs/ClangCommandLineReference.html

# X86
# -m3dnow, -mno-3dnow
# -m3dnowa, -mno-3dnowa
# -madx, -mno-adx
# -maes, -mno-aes
# -mavx, -mno-avx
# -mavx2, -mno-avx2
# -mavx512bf16, -mno-avx512bf16
# -mavx512bitalg, -mno-avx512bitalg
# -mavx512bw, -mno-avx512bw
# -mavx512cd, -mno-avx512cd
# -mavx512dq, -mno-avx512dq
# -mavx512er, -mno-avx512er
# -mavx512f, -mno-avx512f
# -mavx512ifma, -mno-avx512ifma
# -mavx512pf, -mno-avx512pf
# -mavx512vbmi, -mno-avx512vbmi
# -mavx512vbmi2, -mno-avx512vbmi2
# -mavx512vl, -mno-avx512vl
# -mavx512vnni, -mno-avx512vnni
# -mavx512vp2intersect, -mno-avx512vp2intersect
# -mavx512vpopcntdq, -mno-avx512vpopcntdq
# -mbmi, -mno-bmi
# -mbmi2, -mno-bmi2
# -mcldemote, -mno-cldemote
# -mclflushopt, -mno-clflushopt
# -mclwb, -mno-clwb
# -mclzero, -mno-clzero
# -mcx16, -mno-cx16
# -menqcmd, -mno-enqcmd
# -mf16c, -mno-f16c
# -mfma, -mno-fma
# -mfma4, -mno-fma4
# -mfsgsbase, -mno-fsgsbase
# -mfxsr, -mno-fxsr
# -mgfni, -mno-gfni
# -minvpcid, -mno-invpcid
# -mlwp, -mno-lwp
# -mlzcnt, -mno-lzcnt
# -mmmx, -mno-mmx
# -mmovbe, -mno-movbe
# -mmovdir64b, -mno-movdir64b
# -mmovdiri, -mno-movdiri
# -mmwaitx, -mno-mwaitx
# -mpclmul, -mno-pclmul
# -mpconfig, -mno-pconfig
# -mpku, -mno-pku
# -mpopcnt, -mno-popcnt
# -mprefetchwt1, -mno-prefetchwt1
# -mprfchw, -mno-prfchw
# -mptwrite, -mno-ptwrite
# -mrdpid, -mno-rdpid
# -mrdrnd, -mno-rdrnd
# -mrdseed, -mno-rdseed
# -mretpoline-external-thunk, -mno-retpoline-external-thunk
# -mrtm, -mno-rtm
# -msahf, -mno-sahf
# -msgx, -mno-sgx
# -msha, -mno-sha
# -mshstk, -mno-shstk
# -msse, -mno-sse
# -msse2, -mno-sse2
# -msse3, -mno-sse3
# -msse4.1, -mno-sse4.1
# -msse4.2, -mno-sse4.2, -msse4
# -msse4a, -mno-sse4a
# -mssse3, -mno-ssse3
# -mtbm, -mno-tbm
# -mvaes, -mno-vaes
# -mvpclmulqdq, -mno-vpclmulqdq
# -mvzeroupper, -mno-vzeroupper
# -mwaitpkg, -mno-waitpkg
# -mwbnoinvd, -mno-wbnoinvd
# -mx87, -m80387, -mno-x87
# -mxop, -mno-xop
# -mxsave, -mno-xsave
# -mxsavec, -mno-xsavec
# -mxsaveopt, -mno-xsaveopt
# -mxsaves, -mno-xsaves

# ------------------------------------------------------------------------------------





#TODO(fernando) ---------------------------
# VMX               https://github.com/klauspost/cpuid/blob/master/cpuid.go#L866
# AESNI             https://github.com/klauspost/cpuid/blob/master/cpuid.go#L878
# PREFETCHWT1       ver en que marchs se usa...



# http://instlatx64.atw.hu/
# https://github.com/klauspost/cpuid/blob/master/cpuid.go
# https://www.agner.org/optimize/#vectorclass
# https://github.com/vectorclass/version2/blob/master/instrset_detect.cpp
# https://hjlebbink.github.io/x86doc/
# https://software.intel.com/sites/default/files/managed/c5/15/architecture-instruction-set-extensions-programming-reference.pdf

import cpuid
import base64
import string
# import base58
from enum import Enum




# print(cpuid._is_long_mode_cpuid())
# ----------------------------------------------------------------------
#TODO(fernando): ponemos el Vendor o no en el entero?
# a, b, c, d = cpuid.cpuid(0)
# print(a)
# print(b)
# print(c)
# print(d)# 
# ----------------------------------------------------------------------


    # int info[4];
    # cpuid(info, 0);
    # int nIds = info[0];

    # cpuid(info, 0x80000000);
    # uint32_t nExIds = info[0];

    # //  Detect Features
    # if (nIds >= 0x00000001){
    #     cpuid(info, 0x00000001);
    #     HW_MMX    = (info[3] & ((int)1 << 23)) != 0;
    #     HW_SSE    = (info[3] & ((int)1 << 25)) != 0;
    #     HW_SSE2   = (info[3] & ((int)1 << 26)) != 0;
    #     HW_SSE3   = (info[2] & ((int)1 <<  0)) != 0;

    #     HW_SSSE3  = (info[2] & ((int)1 <<  9)) != 0;
    #     HW_SSE41  = (info[2] & ((int)1 << 19)) != 0;
    #     HW_SSE42  = (info[2] & ((int)1 << 20)) != 0;
    #     HW_AES    = (info[2] & ((int)1 << 25)) != 0;

    #     HW_AVX    = (info[2] & ((int)1 << 28)) != 0;
    #     HW_FMA3   = (info[2] & ((int)1 << 12)) != 0;

    #     HW_RDRAND = (info[2] & ((int)1 << 30)) != 0;
    # }

def reserved():
    return False

def max_function_id():
	a, _, _, _ = cpuid.cpuid(0)
	return a

def max_extended_function():
	a, _, _, _ = cpuid.cpuid(0x80000000)
	return a

def max_function_id():
	a, _, _, _ = cpuid.cpuid(0)
	return a

def support_movbe():
    # CPUID.01H:ECX.MOVBE[bit 22]
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & (1 << 22) != 0

def support_mmx():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L851
    if max_function_id() < 0x00000001: return False
    _, _, _, d = cpuid.cpuid(0x00000001)
    return d & (1 << 23) != 0

#TODO(fernando): la implementacion de la libreria de Golang creo que tiene un error, revisar y PR.
# def support_mmxext():
#     # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L854
#     if max_function_id() < 0x00000001: return False
#     _, _, _, d = cpuid.cpuid(0x00000001)
#     return d & (1 << 25) != 0

def support_sse():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L857
    if max_function_id() < 0x00000001: return False
    _, _, _, d = cpuid.cpuid(0x00000001)
    return d & (1 << 25) != 0

def support_sse2():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L860
    if max_function_id() < 0x00000001: return False
    _, _, _, d = cpuid.cpuid(0x00000001)
    return d & (1 << 26) != 0

def support_sse3():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L863
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & (1 << 0) != 0

def support_ssse3():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L869
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & 0x00000200 != 0

def support_sse41():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L872
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & 0x00080000 != 0

def support_sse42():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L875
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & 0x00100000 != 0

def support_sse4a():
    # CPUID.80000001H:ECX.SSE4A[Bit 6]
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L1022
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return c & (1 << 6) != 0

def support_popcnt():
    # https://github.com/klauspost/cpuid/blob/master/cpuid.go#L884
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & (1 << 23) != 0 or support_abm()

def support_abm():                  #lzcnt and popcnt
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return (c & (1 << 5)) != 0

def support_pku():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    # return (c & 0x00000008) != 0
    return (c & (1 << 3)) != 0

def support_avx_cpu():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 28)) != 0

def support_avx2_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 5)) != 0

def support_aes():                          # AES Native instructions
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 25)) != 0

def support_pclmul():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 1)) != 0

def support_fsgsbase():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 0)) != 0

def support_rdrnd():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 30)) != 0

def support_fma3_cpu():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 12)) != 0

def support_fma4_cpu():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return (c & (1 << 16)) != 0

def support_bmi():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 3)) != 0

def support_bmi2():
    if not support_bmi(): return False
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 3)) != 0

#Note(fernando): check if CPU is AMD, I think it is not necessary
# static bool TBM(void) { return CPU_Rep.isAMD_ && CPU_Rep.f_81_ECX_[21]; }
def support_tbm():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return (c & (1 << 21)) != 0

def support_f16c():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 29)) != 0

def support_rdseed():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 18)) != 0

# https://en.wikipedia.org/wiki/Intel_ADX
def support_adx():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 19)) != 0

# https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf
# pag. 202
# https://superuser.com/questions/931742/windows-10-64-bit-requirements-does-my-cpu-support-cmpxchg16b-prefetchw-and-la
def support_prefetchw():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return (c & (1 << 8)) != 0

def support_prefetchwt1():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 0)) != 0

def support_clflushopt():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 23)) != 0

def support_xsave_cpu():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 26)) != 0

def support_osxsave():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return (c & (1 << 27)) != 0

def support_xsaveopt_cpu():
    if max_function_id() < 0x0000000D: return False
    a, _, _, _ = cpuid.cpuid_count(0x0000000D, 1)
    return (a & (1 << 0)) != 0

def support_xsavec_cpu():
    if max_function_id() < 0x0000000D: return False
    a, _, _, _ = cpuid.cpuid_count(0x0000000D, 1)
    return (a & (1 << 1)) != 0

def support_xsaves_cpu():
    if max_function_id() < 0x0000000D: return False
    a, _, _, _ = cpuid.cpuid_count(0x0000000D, 1)
    return (a & (1 << 3)) != 0

def support_avx512f_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 16)) != 0

def support_avx512pf_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 26)) != 0

def support_avx512er_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 27)) != 0

def support_avx512vl_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 31)) != 0

def support_avx512bw_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 30)) != 0

def support_avx512dq_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 17)) != 0

def support_avx512cd_cpu():
    if max_function_id() < 0x00000007: return False
    # _, b, _, _ = cpuid.cpuid(0x00000007)
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 28)) != 0

def support_avx5124vnniw_cpu():
    if max_function_id() < 0x00000007: return False
    # _, _, _, d = cpuid.cpuid(0x00000007)
    _, _, _, d = cpuid.cpuid_count(7, 0)
    return (d & (1 << 2)) != 0

def support_avx5124fmaps_cpu():
    if max_function_id() < 0x00000007: return False
    # _, _, _, d = cpuid.cpuid(0x00000007)
    _, _, _, d = cpuid.cpuid_count(7, 0)
    return (d & (1 << 3)) != 0

def support_avx512vbmi_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 1)) != 0

def support_avx512ifma_cpu():
    if max_function_id() < 0x00000007: return False
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 21)) != 0

def support_avx512vbmi2_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 6)) != 0

def support_avx512vpopcntdq_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 14)) != 0

def support_avx512bitalg_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 12)) != 0

def support_avx512vnni_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 11)) != 0

def support_avx512bf16_cpu():
    if max_function_id() < 0x00000007: return False
    a, _, _, _ = cpuid.cpuid_count(7, 1)
    return (a & (1 << 5)) != 0

def support_avx512vp2intersect_cpu():
    if max_function_id() < 0x00000007: return False
    _, _, _,d = cpuid.cpuid_count(7, 0)
    return (d & (1 << 8)) != 0

def support_sha():
    if max_function_id() < 0x00000007: return False
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 29)) != 0

def support_clwb():
    if max_function_id() < 0x00000007: return False
    _, b, _, _ = cpuid.cpuid_count(7, 0)
    return (b & (1 << 24)) != 0

# TODO(fernando): ver Enclave en Golang
def support_enclv():
    return False

def support_umip():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 2)) != 0

# https://hjlebbink.github.io/x86doc/html/PTWRITE.html
def support_ptwrite():
    # TODO(fernando): chequear que sea correcto
    # If CPUID.(EAX=14H, ECX=0):EBX.PTWRITE [Bit 4] = 0.
    # If LOCK prefix is used.
    # If 66H prefix is used.
    if max_function_id() < 0x00000014: return False
    _, b, _, _ = cpuid.cpuid_count(0x00000014, 0)
    return (b & (1 << 4)) != 0

def support_rdpid():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 22)) != 0

# TODO(fernando): SGX?           
# Ver SGX en Golang
def support_sgx():
    return False

def support_gfni():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 8)) != 0

# https://software.intel.com/en-us/forums/intel-isa-extensions/topic/810449
def support_gfni_sse():
    return support_gfni()

def support_vpclmulqdq():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 10)) != 0

def support_vaes():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 9)) != 0

def support_pconfig():
    if max_function_id() < 0x00000007: return False
    _, _, _, d = cpuid.cpuid_count(7, 0)
    return (d & (1 << 18)) != 0

def support_wbnoinvd():
    if max_extended_function() < 0x80000008: return False
    _, b, _, _ = cpuid.cpuid(0x80000008)
    return (b & (1 << 9)) != 0

#https://www.felixcloutier.com/x86/movdiri
def support_movdir():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 27)) != 0

def support_movdir64b():
    if max_function_id() < 0x00000007: return False
    _, _, c, _ = cpuid.cpuid_count(7, 0)
    return (c & (1 << 28)) != 0

# https://www.extremetech.com/computing/296246-intel-announces-cooper-lake-will-be-socketed-compatible-with-future-ice-lake-cpus
# TODO(fernando): ver si hay diferencia entre avx512bf16 y bfloat16  
# cooperlake y tigerlake       
def support_bfloat16():
    return support_avx512bf16_os()

def support_3dnow():
    if max_extended_function() < 0x80000001: return False
    _, _, _, d = cpuid.cpuid(0x80000001)
    return d & (1 << 31) != 0

# enhanced 3DNow!
def support_3dnowext():
    if max_extended_function() < 0x80000001: return False
    _, _, _, d = cpuid.cpuid(0x80000001)
    return d & (1 << 30) != 0

#TODO(fernando): GCC muestra como "SSE prefetch"
    # athlon-tbird
    # AMD Athlon CPU with MMX, 3dNOW!, enhanced 3DNow! and SSE prefetch instructions support.
# creo que se refiere a lo mismo
def support_3dnowprefetch():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return c & (1 << 8) != 0

def support_xop():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return c & (1 << 11) != 0

def support_lwp():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return c & (1 << 15) != 0

# CMPXCHG16B
def support_cx16():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)
    return c & (1 << 13) != 0

# def support_mwait():
#     if max_function_id() < 0x00000001: return False
#     _, _, c, _ = cpuid.cpuid(0x00000001)
#     return c & (1 << 3) != 0

# https://reviews.llvm.org/rL269911
def support_mwaitx():
    if max_extended_function() < 0x80000001: return False
    _, _, c, _ = cpuid.cpuid(0x80000001)
    return c & (1 << 29) != 0

# https://patchew.org/QEMU/20190925214948.22212-1-bigeasy@linutronix.de/
def support_clzero():
    if max_extended_function() < 0x80000008: return False
    _, b, _, _ = cpuid.cpuid(0x80000008)
    return (b & (1 << 0)) != 0

#TODO(fernando): por las dudas chequear a ver si la implementacion de Golang es correcta!
# "Extended MMX (AMD) https://en.wikipedia.org/wiki/Extended_MMX"
def support_mmxext():
    if max_extended_function() < 0x80000001: return False
    _, _, _, d = cpuid.cpuid(0x80000001)
    return d & (1 << 22) != 0



# -----------------------------------------------------------------
# OS support
# -----------------------------------------------------------------

# https://en.wikipedia.org/wiki/Advanced_Vector_Extensions#Operating_system_support
def support_avx_os():
    # Copied from: http://stackoverflow.com/a/22521619/922184

    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)

    XGETBV = (c & (1 << 26)) != 0
    osUsesXSAVE_XRSTORE = (c & (1 << 27)) != 0
    cpuAVXSuport = (c & (1 << 28)) != 0

    if not (XGETBV and osUsesXSAVE_XRSTORE and cpuAVXSuport):
        return False

    xcrFeatureMask = cpuid.xgetbv(0)
    return (xcrFeatureMask & 0x6) == 0x6

def support_avx2_os():
    return support_avx_os() and support_avx2_cpu()

def support_fma3_os():
    return support_avx_os() and support_fma3_cpu()

def support_fma4_os():
    return support_avx_os() and support_fma4_cpu()

def support_xsave_os():
    return support_xsave_cpu() and support_osxsave()

def support_xsaveopt_os():
    return support_xsaveopt_cpu() and support_xsave_os()

def support_xsavec_os():
    return support_xsavec_cpu() and support_xsave_os()

def support_xsaves_os():
    return support_xsaves_cpu() and support_xsave_os()

def support_avx512_os():
    if max_function_id() < 0x00000001: return False
    _, _, c, _ = cpuid.cpuid(0x00000001)

    # Only detect AVX-512 features if XGETBV is supported
    if c & ((1<<26)|(1<<27)) != (1<<26)|(1<<27): return False

    # Check for OS support
    eax = cpuid.xgetbv(0)

    # Verify that XCR0[7:5] = 111b (OPMASK state, upper 256-bit of ZMM0-ZMM15 and
    # ZMM16-ZMM31 state are enabled by OS)
    #  and that XCR0[2:1] = 11b (XMM state and YMM state are enabled by OS).
    return (eax>>5)&7 == 7 and (eax>>1)&3 == 3

def support_avx512f_os():
    return support_avx512_os() and support_avx512f_cpu()

def support_avx512pf_os():
    return support_avx512_os() and support_avx512pf_cpu()

def support_avx512er_os():
    return support_avx512_os() and support_avx512er_cpu()

def support_avx512vl_os():
    return support_avx512_os() and support_avx512vl_cpu()

def support_avx512bw_os():
    return support_avx512_os() and support_avx512bw_cpu()

def support_avx512dq_os():
    return support_avx512_os() and support_avx512dq_cpu()

def support_avx512cd_os():
    return support_avx512_os() and support_avx512cd_cpu()

def support_avx5124vnniw_os():
    return support_avx512_os() and support_avx5124vnniw_cpu()

def support_avx5124fmaps_os():
    return support_avx512_os() and support_avx5124fmaps_cpu()

def support_avx512vbmi_os():
    return support_avx512_os() and support_avx512vbmi_cpu()

def support_avx512ifma_os():
    return support_avx512_os() and support_avx512ifma_cpu()

def support_avx512vbmi2_os():
    return support_avx512_os() and support_avx512vbmi2_cpu()

def support_avx512vpopcntdq_os():
    return support_avx512_os() and support_avx512vpopcntdq_cpu()

def support_avx512bitalg_os():
    return support_avx512_os() and support_avx512bitalg_cpu()

def support_avx512vnni_os():
    return support_avx512_os() and support_avx512vnni_cpu()

def support_avx512bf16_os():
    return support_avx512_os() and support_avx512bf16_cpu()

def support_avx512vp2intersect_os():
    return support_avx512_os() and support_avx512vp2intersect_cpu()



# -----------------------------------------------------------------


extensions_map = {
    0:   cpuid._is_long_mode_cpuid,
    1:   support_movbe,
    2:   support_mmx,
    3:   support_sse,
    4:   support_sse2,
    5:   support_sse3,
    6:   support_ssse3,
    7:   support_sse41,
    8:   support_sse42,
    9:   support_sse4a,
    10:  support_popcnt,
    11:  support_abm,
    12:  support_pku,
    13:  support_avx_os,
    14:  support_avx2_os,
    15:  support_aes,
    16:  support_pclmul,
    17:  support_fsgsbase,
    18:  support_rdrnd,
    19:  support_fma3_os,
    20:  support_fma4_os,
    21:  support_abm,
    22:  support_bmi,
    23:  support_bmi2,
    24:  support_tbm,
    25:  support_f16c,
    26:  support_rdseed,
    27:  support_adx,
    28:  support_prefetchw,
    29:  support_clflushopt,
    30:  support_xsave_os,
    31:  support_xsaveopt_os,
    32:  support_xsavec_os,
    33:  support_xsaves_os,

    34:  support_avx512f_os,
    35:  support_avx512pf_os,
    36:  support_avx512er_os,
    37:  support_avx512vl_os,
    38:  support_avx512bw_os,
    39:  support_avx512dq_os,
    40:  support_avx512cd_os,
    41:  support_avx5124vnniw_os,
    42:  support_avx5124fmaps_os,
    43:  support_avx512vbmi_os,
    44:  support_avx512ifma_os,
    45:  support_avx512vbmi2_os,
    46:  support_avx512vpopcntdq_os,
    47:  support_avx512bitalg_os,
    48:  support_avx512vnni_os,
    49:  support_avx512bf16_os,
    50:  support_avx512vp2intersect_os,

    51:  support_sha,
    52:  support_clwb,
    53:  support_enclv,
    54:  support_umip,
    55:  support_ptwrite,
    56:  support_rdpid,
    57:  support_sgx,
    58:  support_gfni,
    59:  support_gfni_sse,
    60:  support_vpclmulqdq,
    61:  support_vaes,
    62:  support_pconfig,
    63:  support_wbnoinvd,
    64:  support_movdir,
    65:  support_movdir64b,
    66:  support_bfloat16,
    67:  support_3dnow,
    68:  support_3dnowext,
    69:  support_3dnowprefetch,
    70:  support_xop,
    71:  support_lwp,
    72:  support_cx16,
    73:  support_mwaitx,
    74:  support_clzero,
    75:  support_mmxext,
    76:  support_prefetchwt1,

    77:  reserved,
    78:  reserved,
    79:  reserved,
    80:  reserved,
    81:  reserved,
    82:  reserved,
    83:  reserved,
    84:  reserved,
    85:  reserved,
    86:  reserved,
    87:  reserved,
    88:  reserved,
    89:  reserved,
    90:  reserved,
    91:  reserved,
    92:  reserved,
    93:  reserved,
    94:  reserved,
    95:  reserved,
    96:  reserved,
    97:  reserved,
    98:  reserved,
    99:  reserved,
    100: reserved,
    101: reserved,
    102: reserved,
    103: reserved,
    104: reserved,
    105: reserved,
    106: reserved,
    107: reserved,
    108: reserved,
    109: reserved,
    110: reserved,
    111: reserved,
    112: reserved,
    113: reserved,
    114: reserved,
    115: reserved,
    116: reserved,
    117: reserved,
    118: reserved,
    119: reserved,
    120: reserved,
    121: reserved,
    122: reserved,
    123: reserved,
    124: reserved,
    125: reserved,
    126: reserved,
    127: reserved,
    128: reserved,
    129: reserved,
    130: reserved,
    131: reserved,
    132: reserved,
    133: reserved,
    134: reserved,
    135: reserved,
    136: reserved,
    137: reserved,
    138: reserved,
    139: reserved,
    140: reserved,
    141: reserved,
    142: reserved,
    143: reserved,
    144: reserved,
    145: reserved,
    146: reserved,
    147: reserved,
    148: reserved,
    149: reserved,
    150: reserved,
    151: reserved,
    152: reserved,
    153: reserved,
    154: reserved,
    155: reserved,
    156: reserved,
    157: reserved,
    158: reserved,
    159: reserved,
    160: reserved,
    161: reserved,
    162: reserved,
    163: reserved,
    164: reserved,
    165: reserved,
    166: reserved,
    167: reserved,
    168: reserved,
    169: reserved,
    170: reserved,
    171: reserved,
    172: reserved,
    173: reserved,
    174: reserved,
    175: reserved,
    176: reserved,
    177: reserved,
    178: reserved,
    179: reserved,
    180: reserved,
    181: reserved,
    182: reserved,
    183: reserved,
    184: reserved,
    185: reserved,
    186: reserved,
    187: reserved,
    188: reserved,
    189: reserved,
    190: reserved,
    191: reserved,
    192: reserved,
    193: reserved,
    194: reserved,
    195: reserved,
    196: reserved,
    197: reserved,
    198: reserved,
    199: reserved,
    200: reserved,
    201: reserved,
    202: reserved,
    203: reserved,
    204: reserved,
    205: reserved,
    206: reserved,
    207: reserved,
    208: reserved,
    209: reserved,
    210: reserved,
    211: reserved,
    212: reserved,
    213: reserved,
    214: reserved,
    215: reserved,
    216: reserved,
    217: reserved,
    218: reserved,
    219: reserved,
    220: reserved,
    221: reserved,
    222: reserved,
    223: reserved,
    224: reserved,
    225: reserved,
    226: reserved,
    227: reserved,
    228: reserved,
    229: reserved,
    230: reserved,
    231: reserved,
    232: reserved,
    233: reserved,
    234: reserved,
    235: reserved,
    236: reserved,
    237: reserved,
    238: reserved,
    239: reserved,
    240: reserved,
    241: reserved,
    242: reserved,
    243: reserved,
    244: reserved,
    245: reserved,
    246: reserved,
    247: reserved,
    248: reserved,
    249: reserved,
    250: reserved,
    251: reserved,
    252: reserved,
    253: reserved,
    254: reserved,
    255: reserved,
}

extensions_names = {
    0:   "64 bits",
    1:   "movbe",
    2:   "mmx",
    3:   "sse",
    4:   "sse2",
    5:   "sse3",
    6:   "ssse3",
    7:   "sse41",
    8:   "sse42",
    9:   "sse4a",
    10:  "popcnt",
    11:  "lzcnt",
    12:  "pku",
    13:  "avx",
    14:  "avx2",
    15:  "aes",
    16:  "pclmul",
    17:  "fsgsbase",
    18:  "rdrnd",
    19:  "fma3",
    20:  "fma4",
    21:  "abm",
    22:  "bmi",
    23:  "bmi2",
    24:  "tbm",
    25:  "f16c",
    26:  "rdseed",
    27:  "adx",
    28:  "prefetchw",
    29:  "clflushopt",
    30:  "xsave",
    31:  "xsaveopt",
    32:  "xsavec",
    33:  "xsaves",

    34:  "avx512f",
    35:  "avx512pf",
    36:  "avx512er",
    37:  "avx512vl",
    38:  "avx512bw",
    39:  "avx512dq",
    40:  "avx512cd",
    41:  "avx5124vnniw",
    42:  "avx5124fmaps",
    43:  "avx512vbmi",
    44:  "avx512ifma",
    45:  "avx512vbmi2",
    46:  "avx512vpopcntdq",
    47:  "avx512bitalg",
    48:  "avx512vnni",
    49:  "avx512bf16",
    50:  "avx512vp2intersect",

    51:  "sha",
    52:  "clwb",
    53:  "enclv",
    54:  "umip",
    55:  "ptwrite",
    56:  "rdpid",
    57:  "sgx",
    58:  "gfni",
    59:  "gfni_sse",
    60:  "vpclmulqdq",
    61:  "vaes",
    62:  "pconfig",
    63:  "wbnoinvd",
    64:  "movdir",
    65:  "movdir64b",
    66:  "bfloat16",
    67:  "3dnow",
    68:  "3dnowext",
    69:  "3dnowprefetch",
    70:  "xop",
    71:  "lwp",
    72:  "cx16",
    73:  "mwaitx",
    74:  "clzero",
    75:  "mmxext",
    76:  "prefetchwt1",

    77:  "__reserved__",
    78:  "__reserved__",
    79:  "__reserved__",
    80:  "__reserved__",
    81:  "__reserved__",
    82:  "__reserved__",
    83:  "__reserved__",
    84:  "__reserved__",
    85:  "__reserved__",
    86:  "__reserved__",
    87:  "__reserved__",
    88:  "__reserved__",
    89:  "__reserved__",
    90:  "__reserved__",
    91:  "__reserved__",
    92:  "__reserved__",
    93:  "__reserved__",
    94:  "__reserved__",
    95:  "__reserved__",
    96:  "__reserved__",
    97:  "__reserved__",
    98:  "__reserved__",
    99:  "__reserved__",
    100: "__reserved__",
    101: "__reserved__",
    102: "__reserved__",
    103: "__reserved__",
    104: "__reserved__",
    105: "__reserved__",
    106: "__reserved__",
    107: "__reserved__",
    108: "__reserved__",
    109: "__reserved__",
    110: "__reserved__",
    111: "__reserved__",
    112: "__reserved__",
    113: "__reserved__",
    114: "__reserved__",
    115: "__reserved__",
    116: "__reserved__",
    117: "__reserved__",
    118: "__reserved__",
    119: "__reserved__",
    120: "__reserved__",
    121: "__reserved__",
    122: "__reserved__",
    123: "__reserved__",
    124: "__reserved__",
    125: "__reserved__",
    126: "__reserved__",
    127: "__reserved__",
    128: "__reserved__",
    129: "__reserved__",
    130: "__reserved__",
    131: "__reserved__",
    132: "__reserved__",
    133: "__reserved__",
    134: "__reserved__",
    135: "__reserved__",
    136: "__reserved__",
    137: "__reserved__",
    138: "__reserved__",
    139: "__reserved__",
    140: "__reserved__",
    141: "__reserved__",
    142: "__reserved__",
    143: "__reserved__",
    144: "__reserved__",
    145: "__reserved__",
    146: "__reserved__",
    147: "__reserved__",
    148: "__reserved__",
    149: "__reserved__",
    150: "__reserved__",
    151: "__reserved__",
    152: "__reserved__",
    153: "__reserved__",
    154: "__reserved__",
    155: "__reserved__",
    156: "__reserved__",
    157: "__reserved__",
    158: "__reserved__",
    159: "__reserved__",
    160: "__reserved__",
    161: "__reserved__",
    162: "__reserved__",
    163: "__reserved__",
    164: "__reserved__",
    165: "__reserved__",
    166: "__reserved__",
    167: "__reserved__",
    168: "__reserved__",
    169: "__reserved__",
    170: "__reserved__",
    171: "__reserved__",
    172: "__reserved__",
    173: "__reserved__",
    174: "__reserved__",
    175: "__reserved__",
    176: "__reserved__",
    177: "__reserved__",
    178: "__reserved__",
    179: "__reserved__",
    180: "__reserved__",
    181: "__reserved__",
    182: "__reserved__",
    183: "__reserved__",
    184: "__reserved__",
    185: "__reserved__",
    186: "__reserved__",
    187: "__reserved__",
    188: "__reserved__",
    189: "__reserved__",
    190: "__reserved__",
    191: "__reserved__",
    192: "__reserved__",
    193: "__reserved__",
    194: "__reserved__",
    195: "__reserved__",
    196: "__reserved__",
    197: "__reserved__",
    198: "__reserved__",
    199: "__reserved__",
    200: "__reserved__",
    201: "__reserved__",
    202: "__reserved__",
    203: "__reserved__",
    204: "__reserved__",
    205: "__reserved__",
    206: "__reserved__",
    207: "__reserved__",
    208: "__reserved__",
    209: "__reserved__",
    210: "__reserved__",
    211: "__reserved__",
    212: "__reserved__",
    213: "__reserved__",
    214: "__reserved__",
    215: "__reserved__",
    216: "__reserved__",
    217: "__reserved__",
    218: "__reserved__",
    219: "__reserved__",
    220: "__reserved__",
    221: "__reserved__",
    222: "__reserved__",
    223: "__reserved__",
    224: "__reserved__",
    225: "__reserved__",
    226: "__reserved__",
    227: "__reserved__",
    228: "__reserved__",
    229: "__reserved__",
    230: "__reserved__",
    231: "__reserved__",
    232: "__reserved__",
    233: "__reserved__",
    234: "__reserved__",
    235: "__reserved__",
    236: "__reserved__",
    237: "__reserved__",
    238: "__reserved__",
    239: "__reserved__",
    240: "__reserved__",
    241: "__reserved__",
    242: "__reserved__",
    243: "__reserved__",
    244: "__reserved__",
    245: "__reserved__",
    246: "__reserved__",
    247: "__reserved__",
    248: "__reserved__",
    249: "__reserved__",
    250: "__reserved__",
    251: "__reserved__",
    252: "__reserved__",
    253: "__reserved__",
    254: "__reserved__",
    255: "__reserved__",
}

extensions_flags = {
    'gcc':         None, 
    'apple-clang': None,
    'clang':       None,
    'msvc':        None,
    'mingw':       None
}

extensions_flags['gcc'] = {
    0:   ["-m32", "-m64"],
    1:   "-mmovbe",
    2:   "-mmmx",
    3:   "-msse",
    4:   "-msse2",
    5:   "-msse3",
    6:   "-mssse3",
    7:   "-msse4.1",
    8:   "-msse4.2",
    9:   "-msse4a",
    10:  "-mpopcnt",
    11:  "-mlzcnt",
    12:  "-mpku",
    13:  "-mavx",
    14:  "-mavx2",
    15:  "-maes",
    16:  "-mpclmul",
    17:  "-mfsgsbase",
    18:  "-mrdrnd",
    19:  "-mfma",
    20:  "-mfma4",
    21:  "-mabm",
    22:  "-mbmi",
    23:  "-mbmi2",
    24:  "-mtbm",
    25:  "-mf16c",
    26:  "-mrdseed",
    27:  "-madx",
    28:  "-mprfchw",
    29:  "-mclflushopt",
    30:  "-mxsave",
    31:  "-mxsaveopt",
    32:  "-mxsavec",
    33:  "-mxsaves",

    34:  "-mavx512f",
    35:  "-mavx512pf",
    36:  "-mavx512er",
    37:  "-mavx512vl",
    38:  "-mavx512bw",
    39:  "-mavx512dq",
    40:  "-mavx512cd",
    41:  "-mavx5124vnniw",
    42:  "-mavx5124fmaps",
    43:  "-mavx512vbmi",
    44:  "-mavx512ifma",
    45:  "-mavx512vbmi2",
    46:  "-mavx512vpopcntdq",
    47:  "-mavx512bitalg",
    48:  "-mavx512vnni",
    49:  "-mavx512bf16",
    50:  "-mavx512vp2intersect",

    51:  "-msha",
    52:  "-mclwb",
    53:  "-menclv",
    54:  "",                            # TODO(fernando) -mumip dice estar soportado por GCC en las marchs pero no parece ser una flag independiente
    55:  "-mptwrite",
    56:  "-mrdpid",
    57:  "-msgx",
    58:  "-mgfni",
    59:  "-mgfni",                      # gfni_sse
    60:  "-mvpclmulqdq",
    61:  "-mvaes",
    62:  "-mpconfig",
    63:  "-mwbnoinvd",
    64:  "-mmovdiri",                   # mmovdir
    65:  "-mmovdir64b",
    66:  "-mbfloat16",
    67:  "-m3dnow",
    68:  "-m3dnowa",                    # 3dnowext
    69:  "-mprfchw",                    # 3dnowprefetch
    70:  "-mxop",
    71:  "-mlwp",
    72:  "-mcx16",
    73:  "-mmwaitx",
    74:  "-mclzero",
    75:  "-mmmxext",
    76:  "-mprefetchwt1",
}

extensions_flags['apple-clang'] = {
    0:   ["-m32", "-m64"],
    1:   "-mmovbe",
    2:   "-mmmx",
    3:   "-msse",
    4:   "-msse2",
    5:   "-msse3",
    6:   "-mssse3",
    7:   "-msse4.1",
    8:   "-msse4.2",
    9:   "-msse4a",
    10:  "-mpopcnt",
    11:  "-mlzcnt",
    12:  "-mpku",
    13:  "-mavx",
    14:  "-mavx2",
    15:  "-maes",
    16:  "-mpclmul",
    17:  "-mfsgsbase",
    18:  "-mrdrnd",
    19:  "-mfma",
    20:  "-mfma4",
    21:  "-mlzcnt",                         # -mabm parece que no existe en Clang
    22:  "-mbmi",
    23:  "-mbmi2",
    24:  "-mtbm",
    25:  "-mf16c",
    26:  "-mrdseed",
    27:  "-madx",
    28:  "-mprfchw",
    29:  "-mclflushopt",
    30:  "-mxsave",
    31:  "-mxsaveopt",
    32:  "-mxsavec",
    33:  "-mxsaves",

    34:  "-mavx512f",
    35:  "-mavx512pf",
    36:  "-mavx512er",
    37:  "-mavx512vl",
    38:  "-mavx512bw",
    39:  "-mavx512dq",
    40:  "-mavx512cd",
    41:  "-mavx5124vnniw",
    42:  "-mavx5124fmaps",
    43:  "-mavx512vbmi",
    44:  "-mavx512ifma",
    45:  "-mavx512vbmi2",
    46:  "-mavx512vpopcntdq",
    47:  "-mavx512bitalg",
    48:  "-mavx512vnni",
    49:  "-mavx512bf16",
    50:  "-mavx512vp2intersect",

    51:  "-msha",
    52:  "-mclwb",
    53:  "-menclv",
    54:  "",                            # TODO(fernando) -mumip dice estar soportado por GCC en las marchs pero no parece ser una flag independiente
    55:  "-mptwrite",
    56:  "-mrdpid",
    57:  "-msgx",
    58:  "-mgfni",
    59:  "-mgfni",                      # gfni_sse
    60:  "-mvpclmulqdq",
    61:  "-mvaes",
    62:  "-mpconfig",
    63:  "-mwbnoinvd",
    64:  "-mmovdiri",                   # mmovdir
    65:  "-mmovdir64b",
    66:  "-mbfloat16",
    67:  "-m3dnow",
    68:  "-m3dnowa",                    # 3dnowext
    69:  "-mprfchw",                    # 3dnowprefetch
    70:  "-mxop",
    71:  "-mlwp",
    72:  "-mcx16",
    73:  "-mmwaitx",
    74:  "-mclzero",
    75:  "-mmmxext",
    76:  "-mprefetchwt1",
}

# Clang 9
# clang: error: unknown argument '-mabm'; did you mean '-marm'?
extensions_flags['clang'] = {
    0:   ["-m32", "-m64"],
    1:   "-mmovbe",
    2:   "-mmmx",
    3:   "-msse",
    4:   "-msse2",
    5:   "-msse3",
    6:   "-mssse3",
    7:   "-msse4.1",
    8:   "-msse4.2",
    9:   "-msse4a",
    10:  "-mpopcnt",
    11:  "-mlzcnt",
    12:  "-mpku",
    13:  "-mavx",
    14:  "-mavx2",
    15:  "-maes",
    16:  "-mpclmul",
    17:  "-mfsgsbase",
    18:  "-mrdrnd",
    19:  "-mfma",
    20:  "-mfma4",
    21:  "-mlzcnt",                         # -mabm parece que no existe en Clang
    22:  "-mbmi",
    23:  "-mbmi2",
    24:  "-mtbm",
    25:  "-mf16c",
    26:  "-mrdseed",
    27:  "-madx",
    28:  "-mprfchw",
    29:  "-mclflushopt",
    30:  "-mxsave",
    31:  "-mxsaveopt",
    32:  "-mxsavec",
    33:  "-mxsaves",

    34:  "-mavx512f",
    35:  "-mavx512pf",
    36:  "-mavx512er",
    37:  "-mavx512vl",
    38:  "-mavx512bw",
    39:  "-mavx512dq",
    40:  "-mavx512cd",
    41:  "-mavx5124vnniw",
    42:  "-mavx5124fmaps",
    43:  "-mavx512vbmi",
    44:  "-mavx512ifma",
    45:  "-mavx512vbmi2",
    46:  "-mavx512vpopcntdq",
    47:  "-mavx512bitalg",
    48:  "-mavx512vnni",
    49:  "-mavx512bf16",
    50:  "-mavx512vp2intersect",

    51:  "-msha",
    52:  "-mclwb",
    53:  "-menclv",
    54:  "",                            # TODO(fernando) -mumip dice estar soportado por GCC en las marchs pero no parece ser una flag independiente
    55:  "-mptwrite",
    56:  "-mrdpid",
    57:  "-msgx",
    58:  "-mgfni",
    59:  "-mgfni",                      # gfni_sse
    60:  "-mvpclmulqdq",
    61:  "-mvaes",
    62:  "-mpconfig",
    63:  "-mwbnoinvd",
    64:  "-mmovdiri",                   # mmovdir
    65:  "-mmovdir64b",
    66:  "-mbfloat16",
    67:  "-m3dnow",
    68:  "-m3dnowa",                    # 3dnowext
    69:  "-mprfchw",                    # 3dnowprefetch
    70:  "-mxop",
    71:  "-mlwp",
    72:  "-mcx16",
    73:  "-mmwaitx",
    74:  "-mclzero",
    75:  "-mmmxext",
    76:  "-mprefetchwt1",
}

extensions_flags['msvc'] = {
    0:   "",
    1:   "",
    2:   "",
    3:   "",
    4:   "",
    5:   "",
    6:   "",
    7:   "",
    8:   "",
    9:   "",
    10:  "",
    11:  "",
    12:  "",
    13:  "/arch:AVX",
    14:  "/arch:AVX2",
    15:  "",
    16:  "",
    17:  "",
    18:  "",
    19:  "",
    20:  "",
    21:  "",
    22:  "",
    23:  "",
    24:  "",
    25:  "",
    26:  "",
    27:  "",
    28:  "",
    29:  "",
    30:  "",
    31:  "",
    32:  "",
    33:  "",

    34:  "/arch:AVX512",
    35:  "/arch:AVX512",
    36:  "/arch:AVX512",
    37:  "/arch:AVX512",
    38:  "/arch:AVX512",
    39:  "/arch:AVX512",
    40:  "/arch:AVX512",
    41:  "/arch:AVX512",
    42:  "/arch:AVX512",
    43:  "/arch:AVX512",
    44:  "/arch:AVX512",
    45:  "/arch:AVX512",
    46:  "/arch:AVX512",
    47:  "/arch:AVX512",
    48:  "/arch:AVX512",
    49:  "/arch:AVX512",
    50:  "/arch:AVX512",

    51:  "",
    52:  "",
    53:  "",
    54:  "",
    55:  "",
    56:  "",
    57:  "",
    58:  "",
    59:  "",
    60:  "",
    61:  "",
    62:  "",
    63:  "",
    64:  "",
    65:  "",
    66:  "",
    67:  "",
    68:  "",
    69:  "",
    70:  "",
    71:  "",
    72:  "",
    73:  "",
    74:  "",
    75:  "",
    76:  "",
}

extensions_flags['mingw'] = {
    0:   ["-m32", "-m64"],
    1:   "-mmovbe",
    2:   "-mmmx",
    3:   "-msse",
    4:   "-msse2",
    5:   "-msse3",
    6:   "-mssse3",
    7:   "-msse4.1",
    8:   "-msse4.2",
    9:   "-msse4a",
    10:  "-mpopcnt",
    11:  "-mlzcnt",
    12:  "-mpku",
    13:  "-mavx",
    14:  "-mavx2",
    15:  "-maes",
    16:  "-mpclmul",
    17:  "-mfsgsbase",
    18:  "-mrdrnd",
    19:  "-mfma",
    20:  "-mfma4",
    21:  "-mabm",
    22:  "-mbmi",
    23:  "-mbmi2",
    24:  "-mtbm",
    25:  "-mf16c",
    26:  "-mrdseed",
    27:  "-madx",
    28:  "-mprfchw",
    29:  "-mclflushopt",
    30:  "-mxsave",
    31:  "-mxsaveopt",
    32:  "-mxsavec",
    33:  "-mxsaves",

    34:  "-mavx512f",
    35:  "-mavx512pf",
    36:  "-mavx512er",
    37:  "-mavx512vl",
    38:  "-mavx512bw",
    39:  "-mavx512dq",
    40:  "-mavx512cd",
    41:  "-mavx5124vnniw",
    42:  "-mavx5124fmaps",
    43:  "-mavx512vbmi",
    44:  "-mavx512ifma",
    45:  "-mavx512vbmi2",
    46:  "-mavx512vpopcntdq",
    47:  "-mavx512bitalg",
    48:  "-mavx512vnni",
    49:  "-mavx512bf16",
    50:  "-mavx512vp2intersect",

    51:  "-msha",
    52:  "-mclwb",
    53:  "-menclv",
    54:  "",                            # TODO(fernando) -mumip dice estar soportado por GCC en las marchs pero no parece ser una flag independiente
    55:  "-mptwrite",
    56:  "-mrdpid",
    57:  "-msgx",
    58:  "-mgfni",
    59:  "-mgfni",                      # gfni_sse
    60:  "-mvpclmulqdq",
    61:  "-mvaes",
    62:  "-mpconfig",
    63:  "-mwbnoinvd",
    64:  "-mmovdiri",                   # mmovdir
    65:  "-mmovdir64b",
    66:  "-mbfloat16",
    67:  "-m3dnow",
    68:  "-m3dnowa",                    # 3dnowext
    69:  "-mprfchw",                    # 3dnowprefetch
    70:  "-mxop",
    71:  "-mlwp",
    72:  "-mcx16",
    73:  "-mmwaitx",
    74:  "-mclzero",
    75:  "-mmmxext",
    76:  "-mprefetchwt1",
}


# GCC 10 and general
# # gcc: error: unrecognized command line option '-mumip'
# TODO(fernando) -mumip dice estar soportado por GCC en las marchs pero no parece ser una flag independiente

# GCC 9
# gcc: error: unrecognized command line option '-mavx512vp2intersect'

# GCC 7
# gcc: error: unrecognized command line option '-mavx512vbmi2'; did you mean '-mavx512vbmi'?
# gcc: error: unrecognized command line option '-mavx512bitalg'; did you mean '-mavx5124fmaps'?
# gcc: error: unrecognized command line option '-mavx512vnni'; did you mean '-mavx5124vnniw'?
# gcc: error: unrecognized command line option '-mgfni'
# gcc: error: unrecognized command line option '-mvpclmulqdq'; did you mean '-mpclmul'?
# gcc: error: unrecognized command line option '-mvaes'; did you mean '-maes'?
# gcc: error: unrecognized command line option '-mpconfig'; did you mean '-mpcommit'?
# gcc: error: unrecognized command line option '-mwbnoinvd'
# gcc: error: unrecognized command line option '-mmovdiri'; did you mean '-mmovbe'?
# gcc: error: unrecognized command line option '-mmovdir64b'

# GCC 5
# gcc: error: unrecognized command line option '-mpku'
# gcc: error: unrecognized command line option '-mavx512vpopcntdq'
# gcc: error: unrecognized command line option '-mrdpid'

# Clang 8
# clang: error: unknown argument: '-mavx512vp2intersect'

# Clang 6
# clang: error: unknown argument: '-mrdpid'
# clang: error: unknown argument: '-mpconfig'
# clang: error: unknown argument: '-mwbnoinvd'
# clang: error: unknown argument: '-mmovdiri'
# clang: error: unknown argument: '-mmovdir64b'

extensions_compiler_compat = {
    0:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"64 bits",
    1:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"movbe",
    2:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"mmx",
    3:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse",
    4:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse2",
    5:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse3",
    6:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"ssse3",
    7:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse41",
    8:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse42",
    9:   {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sse4a",
    10:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"popcnt",
    11:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"lzcnt",
    12:  {'gcc':6, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 6}, #"pku",
    13:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx",
    14:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx2",
    15:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"aes",
    16:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"pclmul",
    17:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"fsgsbase",
    18:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"rdrnd",
    19:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"fma3",
    20:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"fma4",
    21:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"abm",
    22:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"bmi",
    23:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"bmi2",
    24:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"tbm",
    25:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"f16c",
    26:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"rdseed",
    27:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"adx",
    28:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"prefetchw",
    29:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"clflushopt",
    30:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"xsave",
    31:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"xsaveopt",
    32:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"xsavec",
    33:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"xsaves",

    34:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512f",
    35:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512pf",
    36:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512er",
    37:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512vl",
    38:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512bw",
    39:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512dq",
    40:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512cd",
    41:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx5124vnniw",
    42:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx5124fmaps",
    43:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512vbmi",
    44:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512ifma",
    45:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"avx512vbmi2",
    46:  {'gcc':6, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 6}, #"avx512vpopcntdq",
    47:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"avx512bitalg",
    48:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"avx512vnni",
    49:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"avx512bf16",
    50:  {'gcc':10,'apple-clang': 1,'clang': 9,'msvc': 14,'mingw': 10}, #"avx512vp2intersect",

    51:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sha",
    52:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"clwb",
    53:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"enclv",
    54:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"umip",
    55:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"ptwrite",
    56:  {'gcc':6, 'apple-clang': 1,'clang': 7,'msvc': 14,'mingw': 6}, #"rdpid",
    57:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"sgx",
    58:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"gfni",
    59:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"gfni_sse",
    60:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"vpclmulqdq",
    61:  {'gcc':8, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 8}, #"vaes",
    62:  {'gcc':8, 'apple-clang': 1,'clang': 7,'msvc': 14,'mingw': 8}, #"pconfig",
    63:  {'gcc':8, 'apple-clang': 1,'clang': 7,'msvc': 14,'mingw': 8}, #"wbnoinvd",
    64:  {'gcc':8, 'apple-clang': 1,'clang': 7,'msvc': 14,'mingw': 8}, #"movdir",
    65:  {'gcc':8, 'apple-clang': 1,'clang': 7,'msvc': 14,'mingw': 8}, #"movdir64b",
    66:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"bfloat16",
    67:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"3dnow",
    68:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"3dnowext",
    69:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"3dnowprefetch",
    70:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"xop",
    71:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"lwp",
    72:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"cx16",
    73:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"mwaitx",
    74:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"clzero",
    75:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"mmxext",
    76:  {'gcc':5, 'apple-clang': 1,'clang': 6,'msvc': 14,'mingw': 5}, #"prefetchwt1",
}

def get_available_extensions():
    data = []
    for _, f in extensions_map.items():
        # data.append(str(int(f())))
        data.append(int(f()))
    return data

def _to_chars_bin(data):
    res = []
    for x in data:
        res.append(str(x))
    return res

def _to_ints_bin(data):
    res = []
    for x in data:
        res.append(int(x))
    return res

def _pad_right_array(data):
    if len(data) >= len(extensions_map): return data
    n = len(extensions_map) - len(data)
    for i in range(n):
        data.append(int(0))
    return data

def encode_extensions(exts):
    exts = _to_chars_bin(exts)
    exts_str = ''.join(reversed(exts))
    exts_num = int(exts_str, 2)
    exts_num_b58 = base58_flex_encode(exts_num)
    return exts_num_b58

def decode_extensions(architecture_id):
    architecture_id = str(architecture_id)
    exts_num = base58_flex_decode(architecture_id)
    res = "{0:b}".format(exts_num)
    res = res.zfill(len(extensions_map))
    return _to_ints_bin(list(reversed(res)))

def get_architecture_id():
    exts = get_available_extensions()
    architecture_id = encode_extensions(exts)
    return architecture_id

def extensions_to_names(exts):
    res = []
    for i in range(len(exts)):
        if (exts[i] == 1):
            res.append(extensions_names[i])
    return res

def print_available_extensions(exts):
    for i in range(len(exts)):
        if (exts[i] == 1):
            print("your computer supports " + extensions_names[i])
            # conanobj.output.info("your computer supports " + extensions_names[i])

# ----------------------------------------------------------------------

class Vendor(Enum):
    Other = 0,
    Intel = 1,
    AMD = 2,
    VIA = 3,
    Transmeta = 4,
    NSC = 5,
    KVM = 6,         # Kernel-based Virtual Machine
    MSVM = 7,        # Microsoft Hyper-V or Windows Virtual PC
    VMware = 8,
    XenHVM = 9,
    Bhyve = 10,
    Hygon = 11,


# Except from http://en.wikipedia.org/wiki/CPUID#EAX.3D0:_Get_vendor_ID
vendorMapping = {
	"AMDisbetter!": Vendor.AMD,
	"AuthenticAMD": Vendor.AMD,
	"CentaurHauls": Vendor.VIA,
	"GenuineIntel": Vendor.Intel,
	"TransmetaCPU": Vendor.Transmeta,
	"GenuineTMx86": Vendor.Transmeta,
	"Geode by NSC": Vendor.NSC,
	"VIA VIA VIA ": Vendor.VIA,
	"KVMKVMKVMKVM": Vendor.KVM,
	"Microsoft Hv": Vendor.MSVM,
	"VMwareVMware": Vendor.VMware,
	"XenVMMXenVMM": Vendor.XenHVM,
	"bhyve bhyve ": Vendor.Bhyve,
	"HygonGenuine": Vendor.Hygon,
}

def vendorID():
    v = cpuid.cpu_vendor()
    vend = vendorMapping.get(v, Vendor.Other)
    return vend

def brandName():
    if max_extended_function() >= 0x80000004:
        return cpuid.cpu_name()
    return "unknown"

def cacheLine():
	if max_function_id() < 0x1:
		return 0

	_, ebx, _, _ = cpuid.cpuid(1)
	cache = (ebx & 0xff00) >> 5 # cflush size
	if cache == 0 and max_extended_function() >= 0x80000006:
		_, _, ecx, _ = cpuid.cpuid(0x80000006)
		cache = ecx & 0xff # cacheline size
	#TODO: Read from Cache and TLB Information
	return int(cache)

def familyModel():
	if max_function_id() < 0x1:
		return 0, 0
	eax, _, _, _ = cpuid.cpuid(1)
	family = ((eax >> 8) & 0xf) + ((eax >> 20) & 0xff)
	model = ((eax >> 4) & 0xf) + ((eax >> 12) & 0xf0)
	return int(family), int(model)

def threadsPerCore():
	mfi = max_function_id()
	if mfi < 0x4 or vendorID() != Vendor.Intel:
		return 1

	if mfi < 0xb:
		_, b, _, d = cpuid.cpuid(1)
		if (d & (1 << 28)) != 0:
			# v will contain logical core count
			v = (b >> 16) & 255
			if v > 1:
				a4, _, _, _ = cpuid.cpuid(4)
				# physical cores
				v2 = (a4 >> 26) + 1
				if v2 > 0:
					return int(v) / int(v2)
		return 1
	_, b, _, _ = cpuid.cpuid_count(0xb, 0)
	if b&0xffff == 0:
		return 1
	return int(b & 0xffff)


def logicalCores():
    mfi = max_function_id()
    vend = vendorID()
	
    if vend == Vendor.Intel:
        # Use this on old Intel processors
        if mfi < 0xb:
            if mfi < 1:
                return 0
            # CPUID.1:EBX[23:16] represents the maximum number of addressable IDs (initial APIC ID)
            # that can be assigned to logical processors in a physical package.
            # The value may not be the same as the number of logical processors that are present in the hardware of a physical package.
            _, ebx, _, _ = cpuid.cpuid(1)
            logical = (ebx >> 16) & 0xff
            return int(logical)
        _, b, _, _ = cpuid.cpuid_count(0xb, 1)
        return int(b & 0xffff)
    elif vend == Vendor.AMD or vend == Vendor.Hygon:
        _, b, _, _ = cpuid.cpuid(1)
        return int((b >> 16) & 0xff)
    else:
        return 0
	
def physicalCores():
    vend = vendorID()
	
    if vend == Vendor.Intel:
        return logicalCores() / threadsPerCore()
    elif vend == Vendor.AMD or vend == Vendor.Hygon:
        if max_extended_function() >= 0x80000008:
            _, _, c, _ = cpuid.cpuid(0x80000008)
            return int(c&0xff) + 1
    return 0


def support_rdtscp():
    if max_extended_function() < 0x80000001: return False
    _, _, _, d = cpuid.cpuid(0x80000001)
    return (d & (1 << 27)) != 0

#TODO(fernando): implementar RTCounter() del proyecto Golang
#TODO(fernando): implementar Ia32TscAux() del proyecto Golang

# LogicalCPU will return the Logical CPU the code is currently executing on.
# This is likely to change when the OS re-schedules the running thread
# to another CPU.
# If the current core cannot be detected, -1 will be returned.
def LogicalCPU():
    if max_function_id() < 1:
        return -1
    _, ebx, _, _ = cpuid.cpuid(1)
    return int(ebx >> 24)


# VM Will return true if the cpu id indicates we are in
# a virtual machine. This is only a hint, and will very likely
# have many false negatives.
def VM():
    vend = vendorID()
    if vend == Vendor.MSVM or vend == Vendor.KVM or vend == Vendor.VMware or vend == Vendor.XenHVM or vend == Vendor.Bhyve:
        return True
    return False

def Hyperthreading():
    if max_function_id() < 4: return False
    _, _, _, d = cpuid.cpuid(1)
    if vendorID() == Vendor.Intel and (d&(1<<28)) != 0:
        if threadsPerCore() > 1:
            return True
    return False


# ----------------------------------------------------------------------

def is_superset_of(a, b):
    n = min(len(a), len(b))

    for i in range(n):
        if a[i] < b[i]: return False

    for i in range(n, len(b)):
        if b[i] == 1: return False

    return True

def test_is_superset_of():
    assert(is_superset_of([], []))
    assert(is_superset_of([0], []))
    assert(is_superset_of([], [0]))
    assert(is_superset_of([0], [0]))
    assert(is_superset_of([0,0], [0,0]))
    assert(is_superset_of([0], [0,0]))
    assert(is_superset_of([0,0], [0]))
    assert(is_superset_of([1], [1]))
    assert(is_superset_of([1], [0]))
    assert(is_superset_of([1], []))

    assert(not is_superset_of([0], [1]))
    assert(not is_superset_of([], [1]))

test_is_superset_of()
# ----------------------------------------------------------------------

def filter_extensions(exts, os, comp, comp_ver):
    comp = adjust_compiler_name(os, comp)

    res = []
    for i in range(len(exts)):
        if i in extensions_compiler_compat:
            if extensions_compiler_compat[i][comp] <= comp_ver:
                res.append(exts[i])
            else:
                res.append(0)                
        else:
            res.append(0)                

    return res

def get_compiler_flags(exts, os, comp, comp_ver):
    exts = filter_extensions(exts, os, comp, comp_ver)
    comp = adjust_compiler_name(os, comp)
    comp_extensions_flags = extensions_flags[comp]

    res = []
    for i in range(len(comp_extensions_flags)):
        flag = comp_extensions_flags[i]
        if isinstance(flag, list):
            if (exts[i] == 1):
                res.append(flag[1])
            else:
                res.append(flag[0])
        else:
            if (exts[i] == 1):
                res.append(flag)

    res = list(set(res))
    return " ".join(res)

def get_compiler_flags_arch_id(arch_id, os, comp, comp_ver):
    exts = decode_extensions(arch_id)
    return get_compiler_flags(exts, os, comp, comp_ver)


# ----------------------------------------------------------------------


# intel_marchs = {
#     'i386':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'i486':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'i586':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'lakemont':       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentium-mmx':    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentiumpro':     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'i686':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentium2':       [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentium3':       [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentium-m':      [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'pentium4':       [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'prescott':       [0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'x86-64':         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'nocona':         [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'core2':          [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'nehalem':        [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'westmere':       [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'sandybridge':    [1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'ivybridge':      [1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?],
#     'haswell':        [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,?,?],
#     'broadwell':      [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,1,?,?,?,?],
#     'skylake':        [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,?,?,?,?],
#     'bonnell':        [1,1,1,1,1,1,1,0,0,0,0,?,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?,?],
#     'silvermont':     [1,1,1,1,1,1,1,1,1,0,1,?,0,0,0,1,1,0,1,0,0,?,0,0,0,0,0,0,0,0,?,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?,?],
#     'goldmont':       [1,1,1,1,1,1,1,1,1,0,1,?,0,0,0,1,1,1,1,0,0,?,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?,?],
#     'goldmont-plus':  [1,1,1,1,1,1,1,1,1,0,1,?,0,0,0,1,1,1,1,0,0,?,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?,?],
#     'tremont':        [1,1,1,1,1,1,1,1,1,0,1,?,0,0,0,1,1,1,1,0,0,?,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?,0,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,?,?,?,?,?,?,?,?],
#     'knl':            [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,?,?,?,?,?],
#     'knm':            [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,?,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,?,?,?,?,?],
#     'skylake-avx512': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,1,?,?,?,?],
#     'cannonlake':     [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,?,?,?,?,?],
#     'icelake-client': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,?,?,1,?,?,?,?],
#     'icelake-server': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0,0,1,?,?,1,?,?,?,?],
#     'cascadelake':    [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,?,?,?,?,?,?,?],
#     'cooperlake':     [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,?,?,?,?,?,?,?],
#     'tigerlake':      [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,1,?,?,1,?,?,?,?],
#     'alderlake':      [],
#     'meteor_lake':    [],
# }


intel_marchs = {
    'i386':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'i486':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'i586':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'lakemont':       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentium-mmx':    [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentiumpro':     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'i686':           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentium2':       [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentium3':       [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentium-m':      [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'pentium4':       [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'prescott':       [0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'x86-64':         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'nocona':         [1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'core2':          [1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'nehalem':        [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'westmere':       [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'sandybridge':    [1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'ivybridge':      [1,0,1,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'haswell':        [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    'broadwell':      [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0],
    'skylake':        [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0],
    'bonnell':        [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'silvermont':     [1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'goldmont':       [1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'goldmont-plus':  [1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'tremont':        [1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    'knl':            [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    'knm':            [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    'skylake-avx512': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0],
    'cannonlake':     [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    'icelake-client': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0],
    'icelake-server': [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0],
    'cascadelake':    [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    'cooperlake':     [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0],
    'tigerlake':      [1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0],
    'alderlake':      [],
    'meteor_lake':    [],
}


# # ----------------------------------------------------------------------------------


# print("vendorID: %s" % vendorID())
# print("brandName: %s" % brandName())
# print("cacheLine: %s" % cacheLine())
# print("familyModel: %s, %s" % familyModel())
# print("threadsPerCore: %s" % threadsPerCore())
# print("logicalCores: %s" % logicalCores())
# print("physicalCores: %s" % physicalCores())
# print("LogicalCPU: %s" % LogicalCPU())
# print("VM: %s" % VM())
# print("Hyperthreading: %s" % Hyperthreading())

# print("CPUID Microarchitecture : %s%s" % cpuid.cpu_microarchitecture())
# architecture_id = get_architecture_id()
# print(architecture_id)


# # ----------------------------------------------------------------------------------

# # architecture_id = encode_extensions(exts)

# for name, exts in intel_marchs.items():
#     if len(exts) > 0:
#         print('%s: %s' % (name, encode_extensions(exts)))

# # ----------------------------------------------------------------------------------


# tigerlake_arch_id = '4HxsTnmmzhZMZ'
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 10)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 9)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 8)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 7)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 6)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'gcc', 5)
# # print('Tigerlake GCC flags: %s' % (flags,))

# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'clang', 9)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'clang', 8)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'clang', 7)
# # flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'linux', 'clang', 6)
# # print('Tigerlake Clang flags: %s' % (flags,))


# flags = get_compiler_flags_arch_id(tigerlake_arch_id, 'windows', 'msvc', 14)
# print('Tigerlake MSVC flags: %s' % (flags,))



# # --------------------------------------------------------------------------------

# # tigerlake_exts = decode_extensions(tigerlake_arch_id)
# # gcc10_exts = filter_extensions(tigerlake_exts, 'linux', 'gcc', 10)
# # gcc9_exts  = filter_extensions(tigerlake_exts, 'linux', 'gcc', 9)
# # gcc8_exts  = filter_extensions(tigerlake_exts, 'linux', 'gcc', 8)
# # gcc7_exts  = filter_extensions(tigerlake_exts, 'linux', 'gcc', 7)
# # gcc6_exts  = filter_extensions(tigerlake_exts, 'linux', 'gcc', 6)
# # gcc5_exts  = filter_extensions(tigerlake_exts, 'linux', 'gcc', 5)

# # print(tigerlake_exts)
# # print(gcc10_exts)
# # print(gcc9_exts)
# # print(gcc8_exts)
# # print(gcc7_exts)
# # print(gcc6_exts)
# # print(gcc5_exts)

# # --------------------------------------------------------------------------------

# # # According XLS
# # haswell = [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
# # haswell = _pad_right_array(haswell)

# # skylake = [1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0]
# # skylake = _pad_right_array(skylake)

# # comparable_arch = skylake

# # if is_superset_of(skylake, haswell):
# #     print("Skylake is a superset of Haswell")
# # else:
# #     print("Skylake is NOT a superset of Haswell")



# # # print(comparable_arch)

# # # print_available_extensions(comparable_arch)

# # exts = get_available_extensions()
# # print(exts)
# # print_available_extensions(exts)

# # print("---------------------------------------------")
# # print(support_avx_os())
# # print(support_avx2_cpu())
# # print("---------------------------------------------")


# # for i in range(len(exts)):
# #     if exts[i] != comparable_arch[i]:
# #         print("difference in pos " + str(i) + "    " + extensions_names[i])
# #         if exts[i] == 0:
# #             print("XLS supports    " + extensions_names[i])
# #         else:
# #             print("CPU supports    " + extensions_names[i])






# #                                                        X        X              X  X                    X  X                                                                                                                          X  X                 
# # haswell xls [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# # calculated  [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
