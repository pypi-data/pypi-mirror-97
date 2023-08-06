"""
  Implements utility methods used to determine information and run commands across different platforms.
"""

import codecs
import ctypes
import fnmatch
import hashlib
import math
import os
import platform
import re
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import _thread
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
import socket

from inspect import isfunction
from subprocess import PIPE


# See http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named
class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


UNITS_BASE_TWO = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]
UNITS_BASE_TEN = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
BYTES_PER_KIBIBYTE = 1024
BYTES_PER_MEBIBYTE = BYTES_PER_KIBIBYTE * BYTES_PER_KIBIBYTE
BYTES_PER_MEGABYTE = 1e6
BYTES_PER_GIGABYTE = 1e9


def get_system():
    return platform.system()


def get_distribution():
    return platform.dist()


def get_release():
    return platform.release()


def get_architecture():
    return platform.architecture()


def get_platform():
    plat = platform.platform()
    if plat.lower().find('windows') != -1:
        return 'windows'
    if plat.lower().find('linux') != -1:
        return 'linux'
    if plat.lower().find('darwin') != -1:
        return 'osx'


def get_linux_distribution():
    # Examples of platform.platform() return values:
    # Ubuntu 18.10 on Azure:  Linux-5.0.0-1027-azure-x86_64-with-debian-buster-sid

    if not is_linux():
        return None

    platform_map = {
        'debian': 'debian',
        'ubuntu': 'debian',
        'fedora': 'fedora',
        'redhat': 'fedora',
        'centos': 'fedora'
    }

    plat = platform.platform().lower()
    for fragment, distribution in platform_map.items():
        if fragment in plat:
            return distribution

    return None


def get_system_bit():
    if is_64_bit():
        return '64bit'
    else:
        return '32bit'


def get_build_architecture():
    return os.environ['SQ_ARCHITECTURE']


def is_build_x86():
    return get_build_architecture() == 'x86'


def file_empty(path):
    apath = os.path.join(get_project_root_dir(), path)
    return not os.path.isfile(apath) or os.stat(apath).st_size == 0


def print_file(path, indent=''):
    with open(os.path.join(get_project_root_dir(), path)) as f:
        for line in f.readlines():
            print((indent + line))


def is_windows():
    return get_platform() == 'windows'


def is_linux():
    return get_platform() == 'linux'


def is_osx():
    return get_platform() == 'osx'


g_repo_root_dir = None


def get_repo_root_dir(windows_long_path=True):
    """
    Returns the path to the root of the repository. i.e., C:\crab\
    """
    global g_repo_root_dir
    if not g_repo_root_dir:
        # Cache it since this is an expensive call
        dir1 = os.path.abspath(os.path.dirname(__file__))
        while not os.path.exists(os.path.join(dir1, 'repo-root-dir.txt')):
            dir2 = os.path.abspath(os.path.join(dir1, os.pardir))
            if dir1 == dir2:
                # We hit the root and didn't find it
                return

            dir1 = dir2

        g_repo_root_dir = dir1

    return cleanse_path(g_repo_root_dir, windows_long_path)


def get_git_dir(windows_long_path=True):
    """
    In the most common case, returns the path to the to the repository's
    '.git' folder. i.e., C:\crab\.git
    """
    return cleanse_path(os.path.abspath(git_rev_parse('--git-dir')), windows_long_path)


def get_git_common_dir(windows_long_path=True):
    """
    Returns the path to the '.git' folder. In git worktrees the
    '--git-dir' flag returns a path to a text file. In a worktree
    the '--git-common-dir' flag returns the path to the true
    '.git' directory in the main git worktree
    """
    try:
        # common dir is incorrect when ran from a sub folder
        # See https://goo.gl/MTHFQf
        wd = get_repo_root_dir(windows_long_path)
        return cleanse_path(os.path.join(wd, git_rev_parse('--git-common-dir', cwd=wd)), windows_long_path)
    except BaseException:
        # We are likely on an older version of git, use the --git-dir flag (which has existed longer)
        return get_git_dir(windows_long_path)


def get_project_name():
    project_root_dir = get_project_root_dir()

    # Get rid of everything before the last forward slash
    return project_root_dir.split(os.sep)[-1]


g_project_root_dir = ''


def get_project_root_dir(windows_long_path=True):
    if g_project_root_dir == '':
        raise Exception('g_project_root_dir not set')

    project_root_dir = cleanse_path(g_project_root_dir, windows_long_path)

    return project_root_dir


def set_project_root_dir(project_root_dir):
    global g_project_root_dir
    g_project_root_dir = project_root_dir


def get_common_dir(windows_long_path=True):
    common_dir = os.path.join(g_project_root_dir, '..', 'common')
    common_dir = os.path.normpath(common_dir)

    if not os.path.exists(common_dir):
        common_dir = os.path.join(g_project_root_dir, 'common')

    if not os.path.exists(common_dir):
        raise Exception('common directory could not be found')

    return cleanse_path(common_dir, windows_long_path)


def get_home_dir():
    if is_windows():
        home = os.environ['USERPROFILE']
    else:
        home = os.path.expanduser("~")

    return home


def get_sq_dir():
    return os.environ['SQ_FOLDER']


def is_64_bit():
    if is_windows():
        # On Windows, even if Python is running as a 32-bit process, we are actually
        # more interested in whether we are on a 64-bit flavor of Windows.
        # In a 32-bit process on 64-bit Windows, PROCESSOR_ARCHITEW6432 will be AMD64.
        # In a 64-bit process on 64-bit Windows, PROCESSOR_ARCHITECTURE will be AMD64.
        return os.environ.get('PROCESSOR_ARCHITEW6432') == 'AMD64' or os.environ.get(
            'PROCESSOR_ARCHITECTURE') == 'AMD64'
    else:
        # On UNIX operating systems, Python will be either 32- or 64-bit according to the
        # operating system. So we can just look at the size of a pointer.
        return True if struct.calcsize("P") * 8 == 64 else False


def is_os_headless():
    """
      Returns True if a display is not detected in the build environment
    """
    return get_platform() == 'linux' and 'DISPLAY' not in os.environ


def spawn(
        command_line,
        raise_on_error=True,
        capture_output=False,
        wait_for_end=True,
        suppress_input=False,
        suppress_output=False,
        suppress_error=False,
        new_process_group=False,
        cwd=None,
        virtual_display_if_necessary=False,
        env=None,
        echo=False,
        stdout=None,
        stderr=None):
    """
      Runs the 'command_line' input in the platform's command line.
    """
    additional_kargs = dict()

    if not cwd:
        try:
            cwd = get_project_root_dir(windows_long_path=False)
        except BaseException:
            cwd = os.getcwd()

    if not env:
        env = os.environ

    stdin = None

    if not stderr:
        # By default, we pipe stderr into stdout because Bamboo buffers stdout and not stderr, so you
        # can get out-of-order logs that are really confusing.
        # See https://answers.atlassian.com/questions/31595/bamboo-build-log-not-in-sync
        stderr = subprocess.STDOUT

    output = ''
    err = ''

    if capture_output and suppress_output:
        raise Exception('capture_output and suppress_output are mutually exclusive.')

    if capture_output:
        stdout = PIPE
        stderr = PIPE

    if suppress_input:
        stdin = open(os.devnull, 'r')

    if suppress_output:
        stdout = open(os.devnull, 'w')

    if suppress_error:
        stderr = open(os.devnull, 'w')

    # One reason you might want to do this is to prevent a CTRL^C in the parent process from killing the child
    # process so that the child process can be shutdown gracefully
    if new_process_group:
        # Based on https://stackoverflow.com/questions/5045771
        if is_windows():
            # https://docs.microsoft.com/en-us/windows/win32/procthread/process-creation-flags
            additional_kargs['creationflags'] = 0x00000200
        else:
            def preexec_fn():
                os.setpgrp()

            additional_kargs['preexec_fn'] = preexec_fn

    # Detect if we are running headless and if so run using xvfb
    if virtual_display_if_necessary and is_os_headless():
        command_line = 'xvfb-run --auto-servernum --server-args="-screen 0 1024x768x24" ' + command_line

    if echo:
        print(command_line)

    proc = subprocess.Popen(command_line, env=env, cwd=cwd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr,
                            **additional_kargs)

    if capture_output:
        (output, err) = proc.communicate()

    if wait_for_end:
        ret_code = proc.wait()

        if ret_code != 0 and raise_on_error:
            raise RuntimeError('Command failed with exit code %d: %s' %
                               (ret_code, command_line))

        if not isinstance(output, str):
            output = str(output, encoding=sys.stdout.encoding)

        if not isinstance(err, str):
            err = str(err, encoding=sys.stderr.encoding)

        return ret_code, output, err

    else:
        return proc


def git_rev_parse(flag, cwd=None):
    """
    Calls the 'git rev-parse' command with the supplied flag. This is useful for
    getting a path from git. For example, 'git rev-parse --git-dir' will return
    the directory of the '.git' directory.
    """
    (ret_code, output, err) = spawn('git rev-parse --no-flags ' + flag, capture_output=True, cwd=cwd)
    result = output.strip()
    if result == '':
        raise Exception('git rev-parse failed to return a path')
    return result


def convert_windows_path_to_unix(path):
    return re.sub(r'\\', '/', path)


def cleanse_path(path, windows_long_path=True):
    """
    Takes a potentially 'mixed-platform' path (i.e., partially Windows, partially Unix)
    and turns it into a path that is guaranteed to work on the host platform. Also,
    on Windows it will optionally turn it into a 'long path' that can support >65k
    characters. (This is necessary especially for doing any operations on the
    node_modules folder.)
    """

    # Get rid of extra/unnecessary /../ or /./ sections of the path. Note that normpath does not work properly with
    # long filenames, so we have to convert to short paths and then call this before cleaning.
    path = os.path.normpath(re.sub(r'^([/\\][/\\]\?[/\\])?(\w:)', r'\2', path))

    if is_windows():
        # First replace all forward slashes with backslashes like Windows wants.
        path = re.sub(r'/', r'\\', path)
        if windows_long_path:
            # Turn it into Unicode if it isn't already, since Windows long paths require it
            path = str(path)

            # Windows 'long paths' are of the form \\?\D:\Foo\Bar (instead of the
            # regular D:\Foo\Bar). So we have to do a RegEx replacement that involves
            # A LOT of backslashes.
            path = re.sub(r'^(\w):\\', r'\\\\?\\\1:\\', path)
        else:
            # Turn it into bytestring if it isn't already, otherwise some functions will break
            # http://stackoverflow.com/questions/12253014/why-does-popen-fail-on-windows-if-the-env-parameter-contains-a-unicode-object
            path = str(path)

            # Get rid of the 'long path' form if it's in there. There are a some
            # APIs/utilities that can't handle them.
            path = re.sub(r'^(\\\\\?\\)?(\w:)', r'\2', path)
    else:
        path = convert_windows_path_to_unix(path)

    return path


def cleanse_filename(filename, replacement_char='_'):
    return re.sub(r'[:"%\\/<>^|?*&\[\]]', replacement_char, filename)


def concat_path(path1, path2):
    return cleanse_path(path1 + os.sep + path2)


def script_path_to_unix(path, retain_colon=False):
    """
    This function is used to convert a path into something that is suitable for
    a Unix script, including a Bash script being run on Windows in Git Bash.

    On Windows, a path like r"C:\Foo\Bar" or r"\\?\C:\Foo\Bar" will get turned into
    "/c/foo/bar".
    """
    path = path.replace('\\', '/')
    path = re.sub(r'^(//\?/)?(\w)\:', '/\\2%s' % (':' if retain_colon else ''), path)
    return path


def script_path_to_windows(path):
    """
    This function is used to convert a path into something that is suitable for
    a Windows batch script.

    On Windows, a path like "C:/Foo/Bar"  will get turned into
    'C:\foo\bar'. Note that the long path prefix ('\\?\') will also get stripped
    off because it's not supported in Windows batch scripts. (Go figure.)
    """
    path = path.replace('/', '\\')
    path = re.sub(r'^(\\\\\?\\)?(\w\:)', '\\2', path)
    return path


def path_to_regex(path):
    """
    This function returns a regular expression that will match the given path
    properly against a string that may contain a variety of representations of
    the path on Windows.
    """

    drive_letter = None
    remaining_path = path
    regex = r''

    # On Windows, paths may be prefixed in the following ways:
    # Regular:      C:\
    # Long Paths:   \\?\C:\
    # Git Bash:     /C/

    # The following RegEx extracts the drive letter no matter which of the
    # ways happens to be used
    match = re.search(r'^((\\\\\?\\)?|/)(\w)(\:[\\/]|/)', path)
    if match:
        drive_letter = match.group(3)
        remaining_path = path[match.end():]

        # We use an almost identical RegEx for our pattern except we hard-code
        # the drive letter
        regex = r'((\\\\\?\\)?|/)%s(\:[\\/]|/)' % drive_letter

    # Windows is loosey-goosey in that it allows a mixture of backslashes and
    # forward slashes throughout the path, so we replace all of them with
    # a character matching set that includes both
    regex += re.sub(r'[\\/]', r'[\\\\/]', remaining_path)

    # The path could be wrapped in quotes
    regex = '[\'"]?' + regex + '[\'"]?'

    return regex


def find_files_recursively(starting_dir, wildcard):
    """
    Returns a list of files that match the wildcard passed in (honoring asterisks)
    by recursively searching the starting_dir and below.
    """
    matches = []
    for root, dirnames, filenames in os.walk(starting_dir):
        for filename in fnmatch.filter(filenames, wildcard):
            matches.append(cleanse_path(os.path.join(root, filename), False))
    return matches


def find_folders_recursively(starting_dir, wildcard):
    """
    Returns a list of folders that match the wildcard passed in (honoring asterisks)
    by recursively searching the starting_dir and below.
    """
    matches = []
    for root, dirnames, filenames in os.walk(starting_dir):
        for folder in fnmatch.filter(dirnames, wildcard):
            matches.append(cleanse_path(os.path.join(root, folder), False))
    return matches


def replace_in_string(str, replacements):
    """
    Replaces all instances of a regex in a string with the specified replacement.
    'replacements' is a list of tuples in the form (pattern, repl, [flags]) where 'pattern'
    is a regex pattern and 'repl' is either a function that, when called with the
    match object returns the replacement text, or a straight regex string that
    represents the replacement. 'flags' is an optional modifier for the regex
    such as re.MULTILINE
    """
    while True:
        at_least_one_match = False
        for replacement in replacements:
            pattern = replacement[0]
            repl = replacement[1]
            flags = replacement[2] if len(replacement) is 3 else 0
            compiled = re.compile(pattern, flags)
            match = compiled.search(str)
            if match:
                at_least_one_match = True
                if isfunction(repl):
                    replacement_text = repl(match)
                    str = str[:match.start()] + replacement_text + str[match.end():]
                else:
                    str = re.sub(pattern, repl, str, 0, flags)

        if not at_least_one_match:
            break

    return str


def replace_in_file(file_path, replacements):
    """
    Replaces all instances of a regex in a text file with the specified replacement.
    'replacements' is a list of tuples in the form (pattern, repl, [flags]) where 'pattern'
    is a regex pattern and 'repl' is either a function that, when called with the
    match object returns the replacement text, or a straight regex string that
    represents the replacement. 'flags' is an optional modifier for the regex
    such as re.MULTILINE
    """
    file = open(file_path, 'r', encoding='utf-8')
    file_content = file.read()
    file.close()

    file_content = replace_in_string(file_content, replacements)

    file = open(file_path, 'w', encoding='utf-8')
    file.write(file_content)
    file.close()


def replace_in_binary_file(file_path, replacements):
    """
    Replaces all instances of a pattern in a binary file with the specified replacement.
    'replacements' is a list of tuples in the form (pattern, repl) where 'pattern'
    is a pattern and 'repl' is its replacement. Regex is not supported.
    """
    file = open(file_path, 'rb')
    file_content = file.read()
    file.close()

    for replacement in replacements:
        (pattern, repl) = replacement
        file_content = file_content.replace(pattern, repl)

    file = open(file_path, 'wb')
    file.write(file_content)
    file.close()


def get_username():
    """
    Returns the current user's name in a cross platform way.
    """
    if is_windows():
        import win32api
        return win32api.GetUserName()
    else:
        import pwd
        return pwd.getpwuid(os.getuid()).pw_name


def keypress_event():
    """
    Returns a threading.Event object that is signaled if the user presses ENTER.
    """
    event = threading.Event()
    threading.Thread(target=_wait_for_keypress_thread, daemon=True, args=(event,)).start()
    return event


def _wait_for_keypress_thread(event):
    try:
        input()
    except EOFError:
        # If this occurs, then there is no input stream to read from. We exit this thread
        # and the original thread will wait forever (or until its timeout) for the event
        # to be set.
        #
        # This is the case for 'sq run' during 'sq build' for AppServer: The integration
        # test target manager kills 'sq run' using 'sq run --kill', not a keypress.
        return

    event.set()


def is_script_running_on_the_continuous_integration_server():
    return 'IS_CI' in os.environ


def copytree(src, dst, symlinks=False, update=False, mirror=False, permissions=False, progress=False, exclude=None):
    if is_windows():
        robocopy(src, dst, update=update, mirror=mirror, permissions=permissions, progress=progress, exclude=exclude)
    else:
        rsync(src, dst, symlinks=symlinks, update=update, mirror=mirror, permissions=permissions, progress=progress,
              exclude=exclude)


def copyfile(src, dst):
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    try:
        shutil.copy2(src, dst)
    except IOError as e:
        if e.errno == 13:  # Permission denied
            # Remove the read-only flag and try again
            os.chmod(dst, stat.S_IWRITE)
            shutil.copy2(src, dst)
        else:
            raise e


def on_rm_error(func, path, exc_info):
    # From
    # http://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows

    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def copy_windows_acls(src, dst):
    # From https://confidentialfiles.wordpress.com/2014/03/13/copying-ntfs-permissions-between-folders/

    # Create a temporary file for the ACL descriptors.
    temp_handle, temp_path = tempfile.mkstemp()
    os.close(temp_handle)

    # Write the ACL descriptors to the temp file.
    spawn('icacls "%s" /save "%s"' % (src, temp_path))

    # Open up the ACL descriptor file. It is encoded as UCS-2 Little Endian.
    with codecs.open(temp_path, 'r', 'utf_16_le') as f:
        lines = f.readlines()

    # Replace the first line, which is the name of the source directory, with the destination directory.
    lines[0] = str(os.path.basename(dst))

    # Write out the new ACL descriptor file.
    with codecs.open(temp_path, 'w', 'utf_16_le') as f:
        f.writelines(os.linesep.join(lines) + os.linesep)

    # Grab the directory name of the destination because (and this is so cool -- not!!) icacls restores ACLs by
    # using the parent directory as the command line input and then the target directory on the first line of the file.
    dst_dir = os.path.dirname(dst)

    # What a pain in the butt! icacls chokes if you pass in "C:\" (with surrounding quotes) for root folders.
    # So only wrap in quotes if there is actually a space somewhere in the directory name.
    if ' ' in dst_dir:
        dst_dir = '"%s"' % dst_dir

    # Finally, "restore" the ACLs to the new location
    spawn('icacls %s /restore "%s"' % (dst_dir, temp_path))

    # Clean up the temp file.
    os.remove(temp_path)


def robocopy(src, dst, mirror=False, update=False, permissions=False, progress=False, exclude=None):
    # Arguments cannot use long path names
    src = cleanse_path(src, windows_long_path=False)
    dst = cleanse_path(dst, windows_long_path=False)
    mode = '/MIR' if mirror else '/E'
    upd = '/XO' if update else ''
    logging = '/NP /NS /NC /NFL /NDL /NJH /NJS'
    if progress:
        logging = '/NP /NS /NC /NJH /NJS'
    exclusions = ''
    if exclude is not None:
        files = list()
        dirs = list()
        for x in exclude:
            absolute_path = os.path.join(src, x)
            if os.path.isdir(absolute_path):
                dirs.append(absolute_path)
            else:
                files.append(absolute_path)
        if len(files) > 0:
            exclusions = exclusions + ' /XF ' + ' '.join(files)
        if len(dirs) > 0:
            exclusions = exclusions + ' /XD ' + ' '.join(dirs)
    cmdline = 'robocopy "%s" "%s" %s %s /R:0 /MT %s %s' % (src, dst, mode, upd, logging, exclusions)
    (ret_code, output, err) = spawn(cmdline, capture_output=not progress, raise_on_error=False)
    if ret_code > 3:
        raise Exception(
            'Robocopy failed to copy "%s" to "%s" with error code %d:\n%s\n%s' % (src, dst, ret_code, output, err))

    # Why not use the /SEC switch on robocopy? Because it doesn't seem to work in Windows Server 2008 R2. CRAB-12017
    if permissions:
        copy_windows_acls(src, dst)


def rsync(src, dst, symlinks=False, mirror=False, update=False, permissions=False, progress=False, exclude=None):
    if not os.path.exists(dst):
        os.makedirs(dst)

    args = '-rtE'
    if symlinks:
        args = args + 'l'

    if update:
        args = args + 'u'

    if permissions:
        args = args + 'p'

    if not progress:
        args = args + 'q'

    if mirror:
        args = args + ' --del'

    if exclude is not None:
        args = args + ' ' + ' '.join([('--exclude %s' % x) for x in exclude])

    # Add a trailing slash so that rsync won't create an additional level below the destination
    if not src.endswith('/'):
        src = src + '/'

    cmdline = 'rsync %s "%s" "%s"' % (args, src, dst)
    spawn(cmdline)


def do_with_retry(func, timeout_sec=5, retry_sleep_sec=0.1):
    timer = time.time()
    while True:
        try:
            func()
            break
        except BaseException as e:
            if time.time() - timer > timeout_sec:
                raise

            time.sleep(retry_sleep_sec)


def removetree(path, keep_top_folder=False):
    if is_windows():
        # If we're on Windows, and there is a folder with contents where part of the path >260 characters, we have to
        # use Robocopy to remove the contents of the folder due to extremely long path names.
        # Ironically, however, the top-level folder can't be long-named.
        empty_folder = None
        try:
            empty_folder = tempfile.mkdtemp()
            robocopy(empty_folder, path, mirror=True)
        finally:
            if empty_folder:
                os.removedirs(empty_folder)

    if not keep_top_folder:
        # It appears the robocopy process can hold on to the directory we're trying to delete for a short time.
        do_with_retry(lambda: shutil.rmtree(path, onerror=on_rm_error))


def remove_deep_folder(path):
    removetree(path)


def get_git_branch():
    """
    Return the name of the current git branch.

    Taken from:
    http://stackoverflow.com/questions/1593051/how-to-programmatically-determine-the-current-checked-out-git-branch
    :return: Name of the current git branch
    """
    (ret_code, output, err) = spawn('git symbolic-ref HEAD', capture_output=True)
    return output.replace('refs/heads/', '').strip()


def get_aws_metadata(metadata):
    """
    Return information about the AWS instance that this code is running on.

    Taken from:
    http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    :param metadata: The key for the metadata you want to retrieve
    :return: The desired metadata
    """
    url = 'http://169.254.169.254/latest/meta-data/%s' % metadata
    with urllib.request.urlopen(url, timeout=1) as f:
        return f.read().decode('utf-8')


def get_current_user_name_and_email():
    user_name = None
    user_email = None

    try:
        (ret_code, output, err) = spawn('git config user.name', capture_output=True)
        user_name = output.strip() if len(output.strip()) > 0 else None
        (ret_code, output, err) = spawn('git config user.email', capture_output=True)
        user_email = output.strip() if len(output.strip()) > 0 else None
    except BaseException:
        # Didn't work, pass back None
        pass

    return user_name, user_email


def prepend_to_path_environment_variable(env, path_to_prepend):
    # On UNIX, it's PATH, on Windows it's Path
    variable_name = 'PATH'
    if 'Path' in env:
        variable_name = 'Path'

    path_variable = env[variable_name]

    path_variable = path_to_prepend + os.pathsep + path_variable

    env[path_variable] = path_variable

    return env


def get_md5_hash(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        return hashlib.md5(data).hexdigest()


def is_admin():
    try:
        return (os.getuid() == 0)
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()


def fix_permissions(file_or_folder):
    if is_windows():
        # If this is Windows, we might be in an elevated process and that means we'll create the folder with
        # restricted access, which can cause problems later. Use icacls to give "Everyone" access. Administrators
        # can lock it down later.
        cmdline = 'icacls "%s" /grant "Everyone:%sF" >NUL' % (file_or_folder,
                                                              '(OI)(CI)' if os.path.isdir(file_or_folder) else '')
        spawn(cmdline)
    else:
        if os.path.isdir(file_or_folder):
            cmdline = "chmod -R g=rwx,o=rwx '%s'" % file_or_folder
        else:
            cmdline = "chmod g=rw,o=rw '%s'" % file_or_folder
        spawn(cmdline)


def create_folder_if_necessary_with_correct_permissions(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        fix_permissions(folder)


def force_unicode(s):
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return str(s, errors='replace')
    else:
        return str(s)


def force_print(s):
    if s is None:
        return

    print(force_unicode(s))


def get_branch_details():
    (ret_code, output, err) = spawn('git status', capture_output=True)

    if ret_code != 0:
        raise RuntimeError('Error calling "git status"')

    branch_name = None
    for match in re.finditer(r'On branch (.*?)\n', output):
        branch_name = match.group(1)

    if not branch_name:
        raise RuntimeError('ERROR: Could not discern git branch from "git status":\n%s' % output)

    pushed = False
    if 'Your branch is' in output:
        pushed = True

    matcher = re.match(r'.*crab-(\d+).*', branch_name.lower())
    if not matcher:
        return None, None, None

    crab_number = matcher.group(1)

    return branch_name, crab_number, pushed


def human_readable_byte_count(bytes, use_base_two, round_to_int):
    """
    Python version of SystemInfo#humanReadableByteCount.
    Constructs a human readable string of the given bytes, such as '2.02GiB' or '9.75TB'.
    :param bytes: Number of bytes
    :param use_base_two: If true, use base-two units (GiB); if false, use base-ten (GB)
    :param round_to_int: If true, round the result to the nearest integer. If false, return the result rounded to two
    decimal points.
    :return: A human readable string of the given bytes, such as '2.02GiB' or '9.75TB'.
    """
    baseKilo = 1024 if use_base_two else 1000

    if bytes < baseKilo:
        return "%s B" % bytes

    exponent = int(math.log(bytes) // math.log(baseKilo))
    number = bytes / (baseKilo ** exponent)

    if round_to_int and (round(number) >= baseKilo):
        exponent += 1
        number = bytes / baseKilo ** exponent

    units = UNITS_BASE_TWO[exponent] if use_base_two else UNITS_BASE_TEN[exponent]

    if round_to_int:
        return "%d %s" % (round(number), units)
    else:
        return "%.2f %s" % (number, units)


def pytest(mark, cwd):
    spawn(f'pytest -v -m {mark} --timeout 3600', cwd=cwd)


def periodic_background_task(period: int, initial_delay=0, times=-1):
    """
    Annotate a function with e.g. `periodic_background_task(period=30, initial_delay=5)` to execute that function every
    30 seconds until the python script exits. The task is executed on a daemon thread created just for the task.

    :param period: Seconds between task executions as measured from the end of one execution to the start of the next.
    :param initial_delay: Seconds to delay the first task execution.
    :param times: Number of times to execute the task. -1 to execute forever.
    """

    def outer_wrap(function):
        def wrap(*args, **kwargs):
            stop = threading.Event()

            def inner_wrap():
                i = 0
                stop.wait(initial_delay)
                while i != times and not stop.isSet():
                    function(*args, **kwargs)
                    stop.wait(period)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop

        return wrap

    return outer_wrap
