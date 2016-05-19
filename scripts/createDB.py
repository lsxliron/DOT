import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import settings
import random


def main():
	engine = create_engine("sqlite:///" + settings.dbName, echo=settings.debug)
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()

	#imgPath = 'localhost:8000/Users/lsxliron/Desktop/DOTProject/img'
        imgPath = '/home/lsxliron/lxrdata/DOT_0310_0514/'
	idCounter = 1


	for (dirpath, dirname, filenames) in os.walk(imgPath):
		for f in filenames:
			if f[-3:]=='jpg':
				temp = DotImage()
				temp.id = idCounter
				temp.path = dirpath + '/' + f
				temp.locationId = f[1:-4]
				temp.filename = f

				fileStats = os.stat(temp.path)

				temp.date = datetime.fromtimestamp(fileStats.st_mtime).date()
				temp.time = datetime.fromtimestamp(fileStats.st_mtime).time()
				temp.size = round(fileStats.st_size/1024.0, 2)

				#TODO: REMOVE!!!
				temp.rain = int(round(random.random()))

				session.add(temp)
				idCounter += 1

                        session.commit()


if __name__ == "__main__":
	main()

