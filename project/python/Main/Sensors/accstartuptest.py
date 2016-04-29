import subprocess


class Accelometer:

    def __init__(self):
        tes = "tes"

    def testonline(self):
        command = "i2cdetect -y 1"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        if "1d" not in str(output):
            # korjaa loputon looppi
            print("booting")
            self.boot()
        else:
            txtreturn = "Kiihdytysanturi löytyi"
        return txtreturn

    def boot(self):
        command = "gpio mode 9 out"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        command = "gpio write 9 1"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        command = "sudo reboot now"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)


