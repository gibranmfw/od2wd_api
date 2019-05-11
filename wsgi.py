<<<<<<< HEAD
from src.server.instance import server
from src.environment.instance import all_environments

from src.resources.property import *
from src.resources.entity import *

if __name__ == "__main__":
   server.app.run()

=======
from src.resources.property import *
from src.resources.entity import *

from src.server.instance import server
from src.environment.instance import all_environments

#if __name__ == "__main__":
#    server.app.run(all_environments['production'])
>>>>>>> 267c126053e04e7787e23cf3202ac77304cc60e9
