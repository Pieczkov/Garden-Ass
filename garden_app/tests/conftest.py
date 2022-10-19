import random
from datetime import date

from faker import Faker

import pytest

from garden_app.models import Plant, PlantType, Unit, Task, PlanOfWork

faker = Faker("pl_PL")


def create_fake_plant_type():
    new_plant_type = PlantType.objects.create(name=faker.word())
    return new_plant_type


def create_fake_unit():
    new_unit = Unit.objects.create(name=faker.word())
    return new_unit


def create_fake_plant():

    new_plant = Plant.objects.create(
        name=faker.word(),
        species=faker.word(),
        description=faker.sentence(),
        amount=random.randint(1, 10),
        unit=create_fake_unit(),
        type=create_fake_plant_type(),
    )
    return new_plant


def create_fake_task():
    """Generate new task and saves to database"""
    plant = create_fake_plant()
    new_task = Task.objects.create(name=faker.word(), description=faker.sentence(), plant=plant)
    return new_task


def create_fake_plan():
    new_plan = PlanOfWork.objects.create(name=faker.word(), description=faker.sentence(), date=faker.date())
    return new_plan


@pytest.fixture
def fake_plant_type():
    new_plant_type = PlantType.objects.create(name=faker.word())
    return new_plant_type


@pytest.fixture
def fake_unit():
    new_unit = Unit.objects.create(name=faker.word())
    return new_unit


@pytest.fixture
def fake_plant():
    unit = create_fake_unit()
    typee = create_fake_plant_type()
    new_plant = Plant.objects.create(
        name=faker.word(),
        species=faker.word(),
        description=faker.sentence(),
        amount=random.randint(1, 10),
        unit=unit,
        type=typee,
    )
    return new_plant


@pytest.fixture
def fake_task():
    """Generate new task and saves to database"""
    plan = create_fake_plan()
    plant = create_fake_plant()
    new_task = Task.objects.create(name=faker.word(), description=faker.sentence(), plant=plant)
    return new_task


@pytest.fixture
def fake_plan():
    new_plan = PlanOfWork.objects.create(name=faker.word(), description=faker.sentence(), date=faker.date())
    return new_plan


@pytest.fixture
def plant_types():
    data = []
    for _ in range(10):
        plant_type = create_fake_plant_type()
        data.append(plant_type)
    return data


@pytest.fixture
def plant_units():
    data = []
    for _ in range(10):
        unit = create_fake_unit()
        data.append(unit)
    return data


@pytest.fixture
def plants():
    data = []
    for _ in range(10):
        plant = create_fake_plant()
        data.append(plant)
    return data


@pytest.fixture
def tasks():
    data = []
    for _ in range(10):
        task = create_fake_task()
        data.append(task)
    return data


@pytest.fixture
def plans():
    data = []
    for _ in range(10):
        plan = create_fake_plan()
        data.append(plan)
    return data
