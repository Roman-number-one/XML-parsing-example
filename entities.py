import dataclasses
from typing import *


@dataclasses.dataclass(frozen=True)
class BaseEntity:
    _PRETTY_PRINT_MARGIN_STEP = 4

    def __str__(self):
        stack = [(self, None, 0)]
        line_buffer = []
        while stack:
            element, parent_name, left_margin = stack.pop()

            if parent_name is not None:
                if left_margin >= self._PRETTY_PRINT_MARGIN_STEP:
                    margin_str = (' ' * (left_margin - self._PRETTY_PRINT_MARGIN_STEP))
                    line_buffer.append(margin_str + f'{parent_name}:')

            for field in dataclasses.fields(element):
                field_value = getattr(element, field.name)
                if isinstance(field_value, BaseEntity):
                    stack.append((field_value, field.name, left_margin + self._PRETTY_PRINT_MARGIN_STEP))
                    continue

                field_repr = f'{field.name}: {field_value}'
                if left_margin == 0:
                    line_buffer.append(field_repr)
                else:
                    line_buffer.append((' ' * left_margin) + field_repr)

        return '\n'.join(line_buffer)


@dataclasses.dataclass(frozen=True)
class PrintForm(BaseEntity):
    url: Optional[str]
    signature: Optional[str]


@dataclasses.dataclass(frozen=True)
class ResponsibleOrganization(BaseEntity):
    reg_num: Optional[str]
    cons_registry_num: Optional[str]
    full_name: Optional[str]


@dataclasses.dataclass(frozen=True)
class ResponsibleInfo(BaseEntity):
    post_address: Optional[str]
    fact_address: Optional[str]


@dataclasses.dataclass(frozen=True)
class PurchaseResponsible(BaseEntity):
    organization: ResponsibleOrganization
    info: ResponsibleInfo
    responsible_role: Optional[str]


@dataclasses.dataclass(frozen=True)
class Document(BaseEntity):
    id: Optional[str]
    external_id: Optional[str]
    purchase_responsible: PurchaseResponsible
