from subprocess import check_output, CalledProcessError


class RunShellException(Exception):
    pass


def sh(cmd, output_list=False):
    '''
    Returns a string or list with the result of executing given shell command

    Parameters:
    cmd (string): Shell command to be executed
    output_list (boolean): If True then returns a list with the result, otherwise returns a string

    Returns:
    string or list with the output of the command. If `CalledProcessError` is catched,
    then Custom `RunShellException` exception is raised
    '''
    output = ''
    try:
        output = check_output(cmd, shell=True).decode('utf-8')
        if output_list:
            output = output.split('\n')[:-1]
    except CalledProcessError as run_shell_exception:
        raise RunShellException from run_shell_exception
    return output
