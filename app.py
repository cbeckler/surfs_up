################# FLASK #####################

# routes are the paths a search can take

# import
from flask import Flask

# create a new Flask instance
## __name__ is a magic method that will determine if code is being run from command line or imported into other code
### __name__ is the name of the current function
app = Flask(__name__)

# create the first route
## '/' denotates that the data is at the root of our route
@app.route('/')
def hello_world():
    return 'Hello world'