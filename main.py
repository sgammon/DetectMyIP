import os

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import users


## Stores site visitors and their IPs
class Visitor(db.Model):
    
    user = db.UserProperty()
    ip_address = db.StringProperty()
    timeVisited = db.DateProperty(auto_now_add=True)


## Handles incoming requests
class Landing(webapp.RequestHandler):
    
    def get(self):
        
        user = users.get_current_user()
        
        visitors_ip = os.environ['REMOTE_ADDR']
        
        v = Visitor()
        v.user = user
        v.ip_address = visitors_ip
        v.put()
        
        self.response.out.write('<b>Hello world! Your IP address is '+str(visitors_ip)+'</b>.')


## Prints who's been visiting
class VisitorsList(webapp.RequestHandler):
    
    def get(self):
        
        visitors_query = Visitor.all().order('-timeVisited').fetch(25)
        
        self.response.out.write('<b>Latest Visitors:</b><ul>')

        if len(visitors_query) == 0:
            self.response.out.write('<li>No visitors! :(</li>')
        else:
            for visitor in visitors_query:
                self.response.out.write('<li>IP: '+str(visitor.ip_address)+' at time '+str(visitor.timeVisited)+' from user '+str(visitor.user.nickname())+' at email address '+str(visitor.user.email()))
                
        self.response.out.write('</ul><br />Done!')


application = webapp.WSGIApplication([('/', Landing),('/visitors', VisitorsList)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()