import dataclasses
from typing import *
from xml.etree import ElementTree

import model


@dataclasses.dataclass(frozen=True)
class ModelXMLBuilder:
    namespaces: Optional[Dict[str, str]] = None

    def _find(self, element: ElementTree.Element, path: str) -> Optional[ElementTree.Element]:
        return element.find(path, namespaces=self.namespaces)

    def _find_text(self, element: ElementTree.Element, path: str) -> Optional[str]:
        el = self._find(element, path)
        if el is None:
            return None
        return el.text

    def build(self, element: ElementTree.Element) -> model.BaseElement:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class ResponsibleOrganizationBuilder(ModelXMLBuilder):
    def build(self, element: ElementTree.Element) -> model.ResponsibleOrganization:
        return model.ResponsibleOrganization(
            reg_num=self._find_text(element, 'default:regNum'),
            cons_registry_num=self._find_text(element, 'default:consRegistryNum'),
            full_name=self._find_text(element, 'default:fullName'),
        )


@dataclasses.dataclass(frozen=True)
class ResponsibleInfoBuilder(ModelXMLBuilder):
    def build(self, element: ElementTree.Element) -> model.ResponsibleInfo:
        return model.ResponsibleInfo(
            fact_address=self._find_text(element, 'default:orgFactAddress'),
            post_address=self._find_text(element, 'default:orgPostAddress'),
        )


@dataclasses.dataclass(frozen=True)
class PurchaseResponsibleBuilder(ModelXMLBuilder):
    def build(self, element: ElementTree.Element) -> model.PurchaseResponsible:
        responsible_organization = ResponsibleOrganizationBuilder(
            self.namespaces,
        ).build(self._find(element, 'default:responsibleOrg'))

        responsible_info = ResponsibleInfoBuilder(
            self.namespaces,
        ).build(self._find(element, 'default:responsibleInfo'))

        return model.PurchaseResponsible(
            organization=responsible_organization,
            info=responsible_info,
            responsible_role=self._find_text(element, 'default:responsibleRole'),
        )
