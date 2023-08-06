import abc
import enum
from typing import Iterable

import networkx as nx


class LabelPosition(enum.Enum):
    HEAD = 0
    MIDDLE = 1
    TAIL = 2


class DataTypeEnum(enum.Enum):
    """
    Non exaustive data type. Used only to avoid writing magic strings
    """
    ID = "id"
    STR = "str"
    INT = "int"
    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"


class FieldKindEnum(enum.Enum):
    PRIMARY = 0
    FOREIGN = 1
    NORMAL = 2


class YaerrrContext:

    def __init__(self):
        self.er: "ErDiagram" = ErDiagram(name="ER")


class IErNode(abc.ABC):
    """
    Either a entity or a diamong
    """

    def __init__(self, n: int):
        self.id = n

    def get_id(self) -> int:
        return self.id


class Field:

    def __init__(self, name: str, datatype: str, kind: FieldKindEnum):
        self.name = name
        self.datatype = datatype
        self.kind = kind


class StandardField(Field):

    def __init__(self, name: str, datatype: str):
        super().__init__(name, datatype, FieldKindEnum.NORMAL)


class PrimaryKey(Field):
    """
    Aprimary key
    """

    def __init__(self, name: str, datatype: str):
        super().__init__(name, datatype, FieldKindEnum.PRIMARY)


class Entity(IErNode):
    """
    A ER entity
    """

    def __init__(self, n: int, name: str, fields: Iterable[Field]):
        super().__init__(n)
        self.name = name
        self.fields = fields

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if not isinstance(other, Entity):
            return False

        return self.name == other.name


class Comment(IErNode):

    def __init__(self, n: int, description: str):
        super().__init__(n)
        self.description = description


class Diamond(Entity):

    def __init__(self, n: int, name: str, fields: Iterable[Field]):
        super().__init__(n, name, fields)

    def is_anonymous(self) -> bool:
        """
        True if the relation has no name
        :return:
        """
        return self.name == ""


class IErEdge(abc.ABC):
    """
    A generic edge in the network graph
    """
    pass


class DashedEdge(IErEdge):

    def __init__(self):
        pass


class ImplementsErEdge(IErEdge):
    """
    A connection repersenting an inheritance
    """

    def __init__(self):
        pass


class RelationshipConnection(IErEdge):
    """
    A ER relationship **branch**
    """

    def __init__(self, label: str, position: LabelPosition):
        self.label = label
        self.position = position


class ErDiagram:

    def __init__(self, name: str):
        self.er = nx.Graph(name=name)
        self.__next_id = 0

    def generate_primary_id_key(self, name: str = None) -> Field:
        name = name or "id"
        return PrimaryKey(name, datatype=DataTypeEnum.ID.value)

    def generate_field(self, name: str, datatype: str) -> Field:
        return StandardField(name, datatype=datatype)

    def generate_int_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.INT.value)

    def generate_id_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.ID.value)

    def generate_str_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.STR.value)

    def generate_date_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.DATE.value)

    def generate_time_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.TIME.value)

    def generate_datetime_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.DATETIME.value)

    def generate_bool_field(self, name: str) -> Field:
        return StandardField(name, datatype=DataTypeEnum.BOOLEAN.value)

    def add_entity(self, name: str, fields: Iterable[Field]):
        """
        Adds an entity in the ER diagram. Entities are uniquely identified by their names
        :param name: name fo the entity
        :param fields: fields to add in the entity
        :return:
        """
        for n in self.er.nodes:
            if n.name == name:
                raise KeyError(f"There is already an entity whose name is \"{name}\"")
        self.er.add_node(Entity(n=self.__next_id, name=name, fields=list(fields)))
        self.__next_id = self.__next_id + 1

    def add_entity_with_int_id(self, name: str, fields: Iterable[Field]):
        f = list(fields)
        f.append(PrimaryKey("id", DataTypeEnum.ID.value))
        self.add_entity(name=name, fields=f)

    def add_entity_with_str_id(self, name: str, fields: Iterable[Field]):
        f = list(fields)
        f.append(PrimaryKey("id", DataTypeEnum.STR.value))
        self.add_entity(name=name, fields=f)

    def get_entity_by_name(self, name: str) -> Entity:
        for n in self.er.nodes:
            if n.name == name:
                return n
        else:
            raise KeyError(f"entity whose name is \"{name}\" not found")

    def let_entity_inherit_from(self, name: str, interface: str):
        """
        Ensure that the entity named "name" implements the entity named "interface"
        :param name: derived entity
        :param interface: interfce entity
        :return:
        """
        source = self.get_entity_by_name(name)
        sink = self.get_entity_by_name(interface)
        self.er.add_edge(source, sink, weight=ImplementsErEdge())

    def add_relationship(self, entity_from: str, entity_to: str, from_label: str, to_label: str, relationship_name: str, fields: Iterable[Field] = None):
        fields = fields or []
        source = self.get_entity_by_name(entity_from)
        sink = self.get_entity_by_name(entity_to)
        # add diamond
        diamond = Diamond(n=self.__next_id, name=relationship_name, fields=fields)
        self.__next_id = self.__next_id + 1

        self.er.add_node(diamond)
        self.er.add_edge(source, diamond, weight=RelationshipConnection(label=from_label, position=LabelPosition.TAIL))
        self.er.add_edge(diamond, sink, weight=RelationshipConnection(label=to_label, position=LabelPosition.TAIL))

    def add_1_to_1(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1",
            to_label="1",
            fields=fields
        )

    def add_1_to_0_1(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1",
            to_label="0..1",
            fields=fields
        )

    def add_1_to_1_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1",
            to_label="1..n",
            fields=fields
        )

    def add_1_to_0_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1",
            to_label="0..n",
            fields=fields
        )

    def add_1_n_to_1_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1..n",
            to_label="1..n",
            fields=fields
        )

    def add_0_n_to_0_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="0..n",
            to_label="0..n",
            fields=fields
        )

    def add_0_n_to_1_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="0..n",
            to_label="1..n",
            fields=fields
        )

    def add_1_n_to_0_n(self, entity_from: str, entity_to: str, relationship_name: str, fields: Iterable[Field] = None):
        self.add_relationship(
            entity_from=entity_from,
            entity_to=entity_to,
            relationship_name=relationship_name,
            from_label="1..n",
            to_label="0..n",
            fields=fields
        )

    def add_comment_to_entity(self, name: str, comment: str):
        source = self.get_entity_by_name(name)
        comment = Comment(n=self.__next_id, description=comment)
        self.__next_id = self.__next_id + 1
        self.er.add_node(comment)
        self.er.add_edge(source, comment, weight=DashedEdge())

    def add_comment_to_relationship(self, relationship_name: str, comment: str):
        source = self.get_entity_by_name(relationship_name)
        comment = Comment(n=self.__next_id, description=comment)
        self.__next_id = self.__next_id + 1
        self.er.add_node(comment)
        self.er.add_edge(source, comment, weight=DashedEdge())



