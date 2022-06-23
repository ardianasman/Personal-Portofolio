from nameko.rpc import rpc
import depedencies

class Userservice:
    name = 'user_service'
    database = depedencies.Database()

    @rpc
    def register(self,x,y):
        x = self.database.register(x,y)
        return x

    @rpc
    def login(self,x,y):
        x = self.database.login(x,y)
        return x

    @rpc
    def logout(self):
        x = self.database.logout()
        return x