import mlflow.pyfunc as pyfunc
import requests

_PyFuncModel = pyfunc.PyFuncModel


class PatchedPyFuncModel(_PyFuncModel):
    def predict(self, data):
        DD_API_KEY="788a2c583db787d3485e46e99fda3dff"
        headers = {'Content-type': 'application/json', "DD-API-KEY": DD_API_KEY}
        logs_dct = {"ddsource": "agent", "ddtags": "env:test", "hostname": "yes", "message": "hello " + self.__str__()}
        requests.post("https://http-intake.logs.datadoghq.com/v1/input", json=logs_dct, headers=headers)

        result = super(PatchedPyFuncModel, self).predict(data)
        return result

def patch():
    pyfunc.PyFuncModel = PatchedPyFuncModel

