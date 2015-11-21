import subprocess

options = {
   'scriptPath':'/Pamela/script.sh',
}

class Command:
   'Class for script execution'
   def __init__(self,_methodName):
      self.methodName = _methodName
   def execute(self, arg):
      p = subprocess.Popen(['sh', options['scriptPath'], self.methodName, arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      p.wait()
      return p.returncode


class Container:
   'Common base class for all container'
   def __init__(self, _userName):
      self.userName = _userName
   def open(self):
      return Command('open').execute(self.userName)
   def close(self):
      return Command('close').execute(self.userName)
   def create(self):
      print('Do you want to crypt your data ? (Type uppercase yes)')
      return Command('create').execute(self.userName)
   def exists(self):
      return Command('exists').execute(self.userName)
   def remove(self):
      return Command('remove').execute(self.userName)

def pam_sm_authenticate(pamh, flags, argv):
   if pamh.user == "root":
      return pamh.PAM_SUCCESS
   container = Container(pamh.user)
   if container.exists() != pamh.PAM_SUCCESS:
      if container.create() != pamh.PAM_SUCCESS:
         return container.remove()
   container.open()
   return pamh.PAM_SUCCESS;


def pam_sm_end(pamh):
   Container(pamh.user).close()
   return pamh.PAM_SUCCESS

def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    return pamh.PAM_SUCCESS
