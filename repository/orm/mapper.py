from sqlalchemy.orm import registry, relationship

import model
from .person import persons_table
from .settlement import settlements_table
from .gender import genders_table


def run_mapper():
    mapper_registry = registry()

    mapper_registry.map_imperatively(
        model.Gender, genders_table,
        # properties={
        #     'person_genders': relationship('Person'),
        #     'person_looking_for_genders': relationship('Person'),
        # }
    )

    mapper_registry.map_imperatively(
        model.Person,
        persons_table,
        properties={
            'settlement': relationship('Settlement', back_populates='persons')
            # '_looking_for': relationship('Gender', back_populates='persons_looking_for'),
            # '_gender': relationship('Gender', back_populates='persons_gender')
        }
    )

    mapper_registry.map_imperatively(
        model.Settlement,
        settlements_table,
        properties={
            'persons': relationship('Person', back_populates='settlement')
        }
    )
