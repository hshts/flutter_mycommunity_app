import os
import pytest
import sys
from api import create_app, db
from api.models.activity import Activity

# 将应用路径添加到系统路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """创建应用实例"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret-key",
        "JWT_SECRET_KEY": "test-jwt-secret"
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """Mock authorization headers for testing."""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_activity_data():
    """Sample activity data for testing."""
    return {
        'content': 'Test Activity Content',
        'uid': 1,
        'province': 'Test Province',
        'city': 'Test City',
        'address': 'Test Address',
        'addresstitle': 'Test Address Title',
        'lat': 39.9042,
        'lng': 116.4074,
        'startyear': 2025,
        'endyear': 2025,
        'peoplenum': 10,
        'mincost': 50.0,
        'maxcost': 100.0,
        'coverimg': 'test_cover.jpg',
        'coverimgwh': '1920x1080',
        'actimagespath': 'image1.jpg,image2.jpg'
    }


@pytest.fixture
def sample_activity(app, sample_activity_data):
    """Create a sample activity in the database."""
    with app.app_context():
        activity = Activity(
            actid='test-activity-001',
            content=sample_activity_data['content'],
            uid=sample_activity_data['uid'],
            province=sample_activity_data['province'],
            city=sample_activity_data['city'],
            address=sample_activity_data['address'],
            addresstitle=sample_activity_data['addresstitle'],
            lat=sample_activity_data['lat'],
            lng=sample_activity_data['lng'],
            startyear=sample_activity_data['startyear'],
            endyear=sample_activity_data['endyear'],
            peoplenum=sample_activity_data['peoplenum'],
            mincost=sample_activity_data['mincost'],
            maxcost=sample_activity_data['maxcost'],
            coverimg=sample_activity_data['coverimg'],
            coverimgwh=sample_activity_data['coverimgwh'],
            actimagespath=sample_activity_data['actimagespath']
        )
        db.session.add(activity)
        db.session.commit()
        return activity