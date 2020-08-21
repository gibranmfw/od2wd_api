from src.server.instance import server
from src.environment.instance import all_environments

from src.resources.property import *
from src.resources.entity import *
from src.resources.protagonist import *
from src.resources.ner import *

if __name__ == "__main__":
   server.app.run()

#if __name__ == "__main__":
#    server.app.run(all_environments['production'])

