# %%
class ifm3dTinyException(Exception):
    pass

class Timeout(ifm3dTinyException):
    def __init__(self):
        self.message = "Timeout occurred - check power, connection, port, ip, timout in sec."
        super().__init__(self.message)
    

# %%
if __name__ == "__main__":
    raise Timeout
# %%
