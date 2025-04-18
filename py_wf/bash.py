from subprocess import check_output, STDOUT

class bash:

    def __init__(self,pre_script="") -> None:
        self.pre_script=pre_script
    
    def __call__(self,script) -> str:
        full_script= self.pre_script + "\n" + script
        return check_output(full_script,stderr=STDOUT,shell=True,).decode("utf-8").strip()
    

    