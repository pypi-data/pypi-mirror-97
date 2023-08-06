import os
import subprocess


class Android:
    @staticmethod
    def start_app(cwd, package, serialno):
        result = subprocess.Popen(
            ['adb', '-s', serialno, 'shell', 'monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1'],
            shell=True, cwd=cwd)
        result.wait()
        return result.returncode

    @staticmethod
    def stop_app(cwd, package, serialno):
        result = subprocess.Popen(
            ['adb', '-s', serialno, 'shell', 'am', 'force-stop', package], shell=True, cwd=cwd)
        result.wait()
        return result.returncode

    @staticmethod
    def list_device(cwd):
        result = subprocess.Popen(
            ['adb', 'devices', '-l'],
            shell=True, cwd=cwd)
        result.wait()

        return result.returncode

    @staticmethod
    def list_package(cwd, serialno, third):
        cmd = ['adb', '-s', serialno, 'shell', 'pm', 'list', 'packages']
        if third:
            cmd.append('-3')
        result = subprocess.Popen(
            cmd,
            shell=True, cwd=cwd)
        result.wait()
        return result.returncode
