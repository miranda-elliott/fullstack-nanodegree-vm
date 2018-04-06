from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# create session and connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# objectives:
# 1 - opening /restaurants lists all the restaurant names in the database
# 2 - after the name of each restaurant there is a link to edit and delete each restaurant
# 3 - there is a page to create new restaurants at /restaurants/new with a form for creating a new restaurant
# 4 - users can rename a restaurant by visiting /restaurant/id/edit
# 5 - clicking delete takes a user to a confirmation page that then sends a post command to the database to delete the selected restaurant

class WebServerHandler(BaseHTTPRequestHandler):
    # handles all get requests our web server recieves
    def do_GET(self):
        if self.path.endswith("/restaurants"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            allRestaurants = session.query(Restaurant).all()
            output = ''
            output += '<html><body><ul>'
            output += '''<a style='display: block;' href='/restaurant/new'>Add New Restaurant</a>'''
            for restaurant in allRestaurants:
                output += '<li>'
                output += '<p>' + restaurant.name + '</p>'
                output += '''<a style="display:block;" href='/restaurant/%s/edit'>Edit</a>''' % restaurant.id
                output += '''<a style="display:block;" href='/restaurant/%s/delete'>Delete</a>''' % restaurant.id
                output += '</li>'
            output += '</ul></body></html>'
            self.wfile.write(output)
            print(output)
            return

        elif self.path.endswith("/restaurant/new"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'
            output += '<form method="POST" enctype="multipart/form-data" action="/restaurant/new">'
            output += '<label>Name</label>'
            output += '<input name="name" type="text">'
            output += '<input type="submit" value="Create">'
            output += '</form></body></html>'
            self.wfile.write(output)
            print(output)
            return

        elif self.path.endswith("/edit"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            id = self.path.split("/")[-2]
            restaurant = session.query(Restaurant).filter_by(id = id).one()
            if restaurant:
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurant/%s/edit">' % restaurant.id
                output += '<input name="name" type="text" value="%s">' % restaurant.name
                output += '<input type="submit" value="Edit">'
                output += '</form></body></html>'
                self.wfile.write(output)
                return

        elif self.path.endswith("/delete"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            id = self.path.split("/")[-2]
            restaurant = session.query(Restaurant).filter_by(id = id).one()
            if restaurant:
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurant/%s/delete">' % restaurant.id
                output += '<label>Are you sure you want to delete %s?</label>' % restaurant.name
                output += '<input type="submit" value="Delete">'
                output += '</form></body></html>'
                self.wfile.write(output)
                return

        elif self.path.endswith("/hello"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'
            output += '<h1>Hello!</h1>'
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += '</body></html>'
            self.wfile.write(output)
            return

        elif self.path.endswith("/hola"):
            # send 200 response with html
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            output = ''
            output += '<html><body>&#161Hola! <a href="/hello">Back to Hello</a> </body></html>'
            self.wfile.write(output)
            return

        else:
            # send 404 response
            self.send_error(404, 'File Not Found: %s' % self.path)

    # handles all post requests that our web server recieves
    def do_POST(self):
        try:
            if self.path.endswith('/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    # get name from form
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')

                    # add restaurant to db
                    restaurant = Restaurant(name = messagecontent[0])
                    session.add(restaurant)
                    session.commit()

                    # send response
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

            elif self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    # get name from form
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')

                    # get restaurant from db
                    id = self.path.split("/")[-2]
                    restaurant = session.query(Restaurant).filter_by(id = id).one()

                    if restaurant:
                        # update restaurant in db
                        restaurant.name = messagecontent[0]
                        session.add(restaurant)
                        session.commit()

                        # send response
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return

            if self.path.endswith('/delete'):
                # get restaurant from db
                id = self.path.split("/")[-2]
                restaurant = session.query(Restaurant).filter_by(id = id).one()

                if restaurant:
                    # delete restaurant from db
                    session.delete(restaurant)
                    session.commit()

                    # send response
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

            elif self.path.endswith('hello'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return

        except:
            pass

def main():
    try:
        # specify port
        port = 8080
        # instantiate web server
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        # start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        # triggered when user types ^+C
        print("^C entered, stopping web server...")
        # stop server
        server.socket.close()


if __name__ == '__main__':
    main()
