
from time import sleep as _sleep
import os as _os

try:
    import boto3 as _boto3
except ImportError:
    _boto3_installed = False
else:
    _boto3_installed = True
    _ec2_resource = _boto3.resource('ec2')
    _ec2_client = _boto3.client('ec2')

def _get_ec2_instance_type(nprocs):
    if nprocs < 2:
        return "t2.micro"
    elif nprocs < 4:
        return "t2.medium"
    elif nprocs < 8:
        return "t2.xlarge"
    elif nprocs < 16:
        return "t3.2xlarge"
    elif nprocs < 36:
        return "c4.4xlarge"
    elif nprocs < 58:
        return "c5.9xlarge"
    elif nprocs < 72:
        return "c5.18xlarge"
    elif nprocs == 96:
        return "c5.24xlarge"
    else:
        raise ValueError("no known instanceType for nprocs={}".format(nprocs))

class AWSEC2Config(object):
    def __init__(self, KeyFile=None, KeyName=None, SubnetId=None, SecurityGroupId=None):
        # TODO: allow setting API KEY, SECRET, etc here as well... rather than requiring aws config?
        # TODO: setters and getters with validation
        # TODO: environment variable or config file support so this doesn't have to be typed out each time

        # TODO: if KeyFile is None:
        """
        ec2 = boto3.resource('ec2')

        # create a file to store the key locally
        outfile = open('ec2-keypair.pem','w')

        # call the boto ec2 function to create a key pair
        key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

        # capture the key and store it in a file
        KeyPairOut = str(key_pair.key_material)
        print(KeyPairOut)
        outfile.write(KeyPairOut)
        # may also need to chmod to 400
        """

        self.KeyFile = KeyFile

        if KeyName is None and KeyFile is not None:
            KeyName = _os.path.basename(KeyFile).split(".")[0]

        self.KeyName = KeyName
        self.SubnetId = SubnetId
        self.SecurityGroupId = SecurityGroupId


# TODO:
# def list_aws_ec2_instances():

class AWSEC2(object):
    def __init__(self, config, instanceId, username='ubuntu', start=False):
        """
        Connect to an **existing** (running or stopped) EC2 instance.

        To create a new instance, see <AWSEC2.new>.

        Arguments
        -------------
        * `config`
        * `instanceId`
        * `username`
        * `start`
        """
        if not _boto3_installed:
            raise ImportError("boto3 required for {}".format(self.__class__.__name__))

        self._instanceId = instanceId
        self._username = username

        # TODO: validate config
        self._config = config

        if instanceId is not None:
            # will raise an error if instanceId not valid
            self._instance

        if start:
            return self.start()

    @classmethod
    def new(cls, config, nprocs=None, InstanceType=None, ImageId='ami-03d315ad33b9d49c4', username='ubuntu', start=False):
        """
        Create a new EC2 instance.

        To connect to an existing (running or stopped) instance, see <AWSEC2.__init__>.

        Arguments
        ------------
        * `config`
        * `nprocs`
        * `InstanceType`
        * `ImageId`
        * `username`
        * `start`
        """

        if nprocs is not None:
            if InstanceType is not None:
                raise ValueError("cannot provide both nprocs and instanceType")
            InstanceType = _get_ec2_instance_type(nprocs=nprocs)

        self = cls(config=config, instanceId=None, username=username, start=start)

        self._initialize_kwargs = {'InstanceType': InstanceType,
                                   'ImageId': ImageId,
                                   'KeyName': config.KeyName,
                                   'SubnetId': config.SubnetId,
                                   'SecurityGroupIds': [config.SecurityGroupId],
                                   'MaxCount': 1,
                                   'MinCount': 1}

        return self

    @property
    def state(self):
        """
        Current state of the EC2 instance.  Can be one of:
        * pending
        * running
        * shutting-down
        * terminated
        * stopping
        * stopped

        Returns
        -----------
        * (string)
        """
        if self._instanceId is None:
            return 'not-started'

        # pending, running, shutting-down, terminated, stopping, stopped
        return self._instance.state['Name']

    @property
    def instanceId(self):
        """
        instanceId of the EC2 instance.  This string is necessary to re-connect
        to an existing (running or stopped) server from a new <AWSEC2> instance.

        Returns
        -----------
        * (string)
        """
        return self._instanceId

    @property
    def _instance(self):
        return _ec2_resource.Instance(self._instanceId)

    @property
    def config(self):
        """
        <AWSEC2Config>

        Returns
        ----------
        * <AWSEC2Config>
        """

        return self._config

    @property
    def username(self):
        """
        Username on the server

        Returns
        ------------
        * (string)
        """
        return self._username

    @property
    def ip(self):
        """
        Public IP address of the server

        Returns
        ------------
        * (string)
        """
        return self._instance.public_ip_address

    @property
    def ssh_cmd(self):
        """
        ssh command to the server

        Returns
        ----------
        * (string): If the server is not yet started and <AWSEC2.ip> is not available,
            the ip will be replaced with {ip}
        """
        try:
            ip = self.ip
        except:
            ip = "{ip}"

        return "ssh -i {} {}@{}".format(self.config.KeyFile, self.username, ip)

    @property
    def scp_cmd_to(self):
        """
        scp command to copy files to the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `local_path` and `server_path`.
            If the server is not yet started and <AWSEC2.ip> is not available,
            the ip will be replaced with {ip}
        """
        try:
            ip = self.ip
        except:
            ip = "{ip}"

        return "scp -i %s {local_path} %s@%s:~/{server_path}" % (self.config.KeyFile, self.username, ip)

    @property
    def scp_cmd_from(self):
        """
        scp command to copy files from the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `server_path` and `local_path`.
            If the server is not yet started and <AWSEC2.ip> is not available,
            the ip will be replaced with {ip}
        """
        try:
            ip = self.ip
        except:
            ip = "{ip}"

        return "scp -i %s %s@%s:~/{server_path} {local_path}" % (self.config.KeyFile, self.username, ip)

    def wait_for_state(self, state, sleeptime=0.5):
        """
        Wait for the server to reach a specified state.

        Arguments
        ----------
        * `state` (string): the desired state.
        * `sleeptime` (float, optional, default): seconds to wait between
            successive state checks.

        Returns
        ----------
        * (string) <AWSEC2.state>
        """
        while self.state != state:
            _sleep(sleeptime)
        return self.state

    def start(self, wait=True):
        """
        Start the server.

        A running server charges per CPU-second.  See AWS pricing for more details.

        Note that <AWSEC2.submit_script> will automatically start the server
        if not already manually started.

        Arguments
        -------------
        * `wait` (bool, optional, default=False): whether to wait for the server
            to reach a running <AWSEC2.state> (and an additional 30 seconds
            to allow for initialization checks to complete and for the server
            to be ready for commands).

        Return
        --------
        * (string) <AWSEC2.state>
        """
        state = self.state
        if state in ['running', 'pending']:
            return
        elif state in ['terminated', 'shutting-down', 'stopping']:
            raise ValueError("cannot start: current state is {}".format(state))

        if self.instanceId is None:
            response = _ec2_client.run_instances(**self._initialize_kwargs)
            self._instanceId = response['Instances'][0]['InstanceId']
        else:
            response = _ec2_client.start_instances(InstanceIds=[self.instanceId], DryRun=False)

        if wait:
            print("waiting for EC2 instance to start...")
            self._instance.wait_until_running()
            # TODO: wait for status checks?
            print("waiting 30s for initialization checks to complete...")
            _sleep(30)

        return self.state

    def stop(self, wait=False):
        """
        Stop the server.

        Once stopped, the server can be restarted via <AWSEC2.start>, including
        by creating a new <AWSEC2> instance with the correct <AWSEC2.instanceId>.

        A stopped server still results in charges for the storage, but no longer
        charges for the CPU time.  See AWS pricing for more details.

        Arguments
        -------------
        * `wait` (bool, optional, default=False): whether to wait for the server
            to reach a stopped <AWSEC2.state>.

        Return
        --------
        * (string) <AWSEC2.state>
        """
        response = _ec2_client.stop_instances(InstanceIds=[self.instanceId], DryRun=False)
        if wait:
            print("waiting for EC2 instance to stop...")
            self._instance.wait_until_stopped()
        return self.state

    def terminate(self, wait=False):
        """
        Terminate the server.

        Once terminated, the server cannot be restarted, but will no longer
        result in charges.  See also <AWSEC2.stop> and AWS pricing for more details.

        Arguments
        -------------
        * `wait` (bool, optional, default=False): whether to wait for the server
            to reach a terminated <AWSEC2.state>.

        Return
        --------
        * (string) <AWSEC2.state>
        """
        response = _ec2_client.terminate_instances(InstanceIds=[self.instanceId], DryRun=False)
        if wait:
            print("waiting for EC2 instance to terminate...")
            self._instance.wait_until_terminated()
        return self.state

    def _submit_script_cmds(self, script, files, stop_on_complete, use_screen):
        if isinstance(script, str):
            # TODO: allow for http?
            if not _os.path.isfile(script):
                raise ValueError("cannot find valid script at {}".format(script))

            f = open(script, 'r')
            script = script.readlines()

        if not isinstance(script, list):
            raise TypeError("script must be of type string (path) or list (list of commands)")

        # TODO: use tmp file instead
        f = open('crimpl_script.sh', 'w')
        f.write("\n".join(script))
        if stop_on_complete:
            f.write("\nsudo shutdown now")
        f.close()

        if not isinstance(files, list):
            raise TypeError("files must be of type list")
        for f in files:
            if not _os.path.isfile(f):
                raise ValueError("cannot find file at {}".format(f))

        # TODO: use script id to create a directory on the server?
        scp_cmd = self.scp_cmd_to.format(local_path=" ".join(["crimpl_script.sh"]+files), server_path="")

        cmd = self.ssh_cmd
        cmd += " \"chmod +x {script}; {screen} sh {script}\"".format(script=_os.path.basename("crimpl_script.sh"), screen="screen -m -d " if use_scren else "")

        return [scp_cmd, cmd]

    def run_script(self, script, files=[], trial_run=False):
        """
        Run a script on the server, and wait for it to complete.

        See <AWSEC2.submit_script> to submit a script to leave running in the background
        on the server.

        Arguments
        ----------------
        * `script` (string or list): shell script to run on the remote server,
            including any necessary installation steps.  Note that the script
            can call any other scripts in `files`.  If a string, must be the
            path of a valid file which will be copied to the server.  If a list,
            must be a list of commands (i.e. a newline will be placed between
            each item in the list and sent as a single script to the server).
        * `files` (list, optional, default=[]): list of paths to additional files
            to copy to the server required in order to successfully execute
            `script`.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed
            (and the server is not started automatically - so these may include
            an <ip> placeholder).


        Returns
        ------------
        * None

        Raises
        ------------
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        if self.state != 'running' and not trial_run:
            self.start(wait=True)

        cmds = self._submit_script_cmds(script, files, stop_on_complete=False, use_screen=False)
        if trial_run:
            return cmds

        for cmd in cmds:
            print("running: {}".format(cmd))

            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)
            _os.system(cmd)

        return

    def submit_script(self, script, files=[], stop_on_complete=True, trial_run=False):
        """
        Submit a script to the server.

        This will call <AWSEC2.start> and wait for
        the server to intialize if it is not already running.  Once running,
        `script` and `files` are copied to the server, and `script` is executed
        in a screen session at which point this method will return.

        To check on any expected output files, call <AWSEC2.check_output>.

        See <AWSEC2.run_script> to run a script and wait for it to complete.

        Arguments
        ----------------
        * `script` (string or list): shell script to run on the remote server,
            including any necessary installation steps.  Note that the script
            can call any other scripts in `files`.  If a string, must be the
            path of a valid file which will be copied to the server.  If a list,
            must be a list of commands (i.e. a newline will be placed between
            each item in the list and sent as a single script to the server).
        * `files` (list, optional, default=[]): list of paths to additional files
            to copy to the server required in order to successfully execute
            `script`.
        * `stop_on_complete` (bool, optional, default=True): whether to stop
            the EC2 instance once `script` has completed.  This is useful for
            long jobs where you may not immediately be able to pull the results
            as a stopped server costs significantly less than a running server.
            If the server is stopped, it will be restarted when calling
            <AWSEC2.check_output>, by manually calling <AWSEC2.start>, or can
            still be terminated manually with <AWSEC2.terminate>.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed
            (and the server is not started automatically - so these may include
            an <ip> placeholder).


        Returns
        ------------
        * None

        Raises
        ------------
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        if self.state != 'running' and not trial_run:
            self.start(wait=True)

        cmds = self._submit_script_cmds(script, files, stop_on_complete=True, use_screen=True)
        if trial_run:
            return cmds

        for cmd in cmds:
            print("running: {}".format(cmd))

            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)
            _os.system(cmd)

        return

    def check_output(self, server_path, local_path="./",
                     wait_for_output=False,
                     restart_if_necessary=True,
                     stop_if_restarted=True):
        """
        Attempt to copy a file back from the server.

        Arguments
        -----------
        * `server_path` (string): path on the server of the file to retrieve.
        * `local_path` (string, optional, default="./"): local path to copy
            the retrieved file.
        * `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED
        * `restart_if_necessary` (bool, optional, default=True): start the server
            if it is not currently running.  This is particularly useful if
            `stop_on_complete` was sent to <AWSEC2.submit_script>.
        * `stop_if_restarted` (bool, optional, default=True): if `restart_if_necessary`
            resulted in the need to start the server, then immediately stop it
            again.  Note that the server must manually be terminated (at some point,
            unless you're super rich) via <AWSEC2.terminate>.

        Returns
        ----------
        * None

        """
        if wait_for_output:
            raise NotImplementedError("wait_for_output not yet implemented")

        did_restart = False
        if restart_if_necessary and self.state != 'running':
            self.start(wait=True)
            did_restart = True

        state = self.state
        if state != 'running':
            raise ValueError("cannot check output, current state: {}".format(state))

        scp_cmd = self.scp_cmd_from.format(server_path=server_path, local_path=local_path)
        # TODO: execute cmd, handle wait_for_output and also handle errors if stopped/terminated before getting results
        print("running: {}".format(scp_cmd))
        _os.system(scp_cmd)

        if did_restart and stop_if_restarted:
            self.stop()
