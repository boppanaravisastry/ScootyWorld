from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from migrations import Scooter_category, Scooter, User, Model

engine = create_engine('sqlite:///ScooterWorld.db')
# Bind the engine to the metadata of the Model class so that the
# declaratives can be accessed through a DBSession instance
Model.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="admin", email="bravisastry@gmail.com")
session.add(User1)
session.commit()

category_1 = Scooter_category(name="Honda", user_id=1)
session.add(category_1)
session.commit()

category_2 = Scooter_category(name="Suzuki", user_id=1)
session.add(category_2)
session.commit()

# inserting scooty data
honda_activa_5G = Scooter(model="Honda Activa 5G",
                          price="56,071",
                          fuel_capacity="5.75 Litres",
                          image="https://www.drivespark.com/bikes-photos/"
                          "modelsoverview/600x450/781/honda-activa-5g-"
                          "review-verdict.jpg/3/x.pagespeed.ic.zbiHzu1rKC.jpg",
                          description="Notifications such as service intervals"
                          "and ECO speed indicator are now part of the Honda"
                          "Activa 5G. The 2018 Activa 5G is now available in"
                          "two new colours: Dazzle Yellow Metallic and Pearl"
                          "Spartan Red. The scooter is feature-rich and boasts"
                          "a host of convenience features compared to the"
                          "Activa 4G.",
                          mileage="60 Kmpl", user_id=1, scooter_category_id=1)
session.add(honda_activa_5G)
session.commit()

honda_dio = Scooter(model="Honda Dio",
                          price="53,385",
                          fuel_capacity="5.3 Litres",
                          image="https://www.motorbeam.com/wp-content/uploads"
                          "/Honda-Dio-Blue.jpg",
                          description="It has a new 110 cc (6.7 cu in) engine,"
                          "which also runs Honda's Activa and Aviator. It also"
                          "has a new look and new headlight. The 2013 HMSI Dio"
                          "had claimed improvements in fuel efficiency and"
                          "combined brakes.",
                          mileage="66 Kmpl", user_id=1, scooter_category_id=1)
session.add(honda_dio)
session.commit()

suzuki_access = Scooter(model="Suzuki Access",
                              price="66,759",
                              fuel_capacity="6.0 Litres",
                              image="https://auto.ndtvimg.com/bike-images/"
                              "colors/suzuki/new-access-125/suzuki-new-access-"
                              "125-metallic-sonic-silver.png?v=34",
                              description="The new model of Suzuki Access has"
                              "a variety of six colour options to choose from"
                              "i.e. White, blue, black, grey, red & silver."
                              "Grey colour with matte finish is another good"
                              "option.Since, the grab handle is of silver"
                              "colour, going for the silver colour may be not"
                              "a great option.",
                              mileage="64 Kmpl", user_id=1,
                              scooter_category_id=2)
session.add(suzuki_access)
session.commit()
print ("added scooters!")
