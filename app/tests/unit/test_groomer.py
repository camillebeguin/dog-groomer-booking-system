import unittest
from unittest.mock import MagicMock

import pytest

from app.repository.groomer import GroomerRepository


def test_create_groomer(session):
    obj_in = {
        "name": "CANISTYLE", 
        "price": 50_00, 
        "status": "active",
        "address": "10 rue Paradis 13100 Marseille", 
        "description": "Dog grooming services",
    }

    groomer = GroomerRepository.create(session, obj_in)
    assert groomer.name == "CANISTYLE" 
    assert groomer.status == "active"
    assert len(GroomerRepository.get_many(session)) == 1