import factory
from api.models.activity import Activity
from api import db
from datetime import datetime
import random
import string

def random_string(length=10):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

class ActivityFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Activity
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    actid = factory.LazyAttribute(lambda _: random_string(10))
    content = factory.Faker('text', max_nb_chars=200)
    createtime = factory.LazyFunction(datetime.utcnow)
    updatetime = factory.LazyFunction(datetime.utcnow)
    status = factory.Faker('random_element', elements=[1, 2])
    peoplenum = factory.Faker('random_int', min=1, max=100)
    currentpeoplenum = factory.Faker('random_int', min=1, max=50)
    startyear = factory.Faker('random_int', min=1609459200, max=1709459200)  # 2021-2024时间戳
    endyear = factory.LazyAttribute(lambda obj: obj.startyear + 7200)  # 2小时后结束
    
    address = factory.Faker('address')
    addresstitle = factory.Faker('city')
    lat = factory.Faker('latitude')
    lng = factory.Faker('longitude')
    actcity = factory.Faker('city')
    actprovince = factory.Faker('state')
    
    coverimg = factory.Faker('image_url')
    coverimgwh = "640x480"
    actimagespath = factory.Faker('uri')
    
    maxcost = factory.Faker('pyfloat', left_digits=3, right_digits=2, positive=True)
    mincost = factory.LazyAttribute(lambda obj: round(obj.maxcost * 0.8, 2))
    paytype = factory.Faker('random_element', elements=[0, 1, 2])
    
    uid = factory.Faker('random_int', min=1, max=10000)
    goodpriceid = factory.LazyAttribute(lambda _: random_string(8))
    
    likenum = factory.Faker('random_int', min=0, max=1000)
    collectionnum = factory.Faker('random_int', min=0, max=1000)
    commentnum = factory.Faker('random_int', min=0, max=1000)
    viewnum = factory.Faker('random_int', min=0, max=10000)
    joinnum = factory.Faker('random_int', min=0, max=100)
    
    locked = factory.Faker('random_element', elements=[0, 1])