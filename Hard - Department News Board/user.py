from nameko.rpc import rpc
import depedencies

class user:
    name = 'service'
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

    @rpc
    def post_news(self, x):
        x = self.database.post_news(x)
        return x

    @rpc
    def delete_news(self, x):
        x = self.database.delete_news(x)
        return x

    @rpc
    def update_news(self, x, y):
        x = self.database.update_news(x, y)
        return x
    
    @rpc
    def get_all_news(self):
        x = self.database.get_all_news()
        return x

    @rpc
    def get_news(self, x):
        x = self.database.get_news(x)
        return x