"""This module has a class that validates that the "dli:required" attribute
has the same value as the base property for all properties in the ontology
file.
"""
from utils.constants import PARENT, PREFIXED, REQUIRED
from utils.ontology import Ontology
from utils.validation import is_property

from validators.validator import Validator


class RequiredValueInSubproperties(Validator):
    """This class has a method validate that the "dli:required" attribute has
    the same value as the base property for all properties in the ontology
    file.
    """

    def validate(self) -> bool:
        """Validates that the "dli:required" attribute has the same value as
        the base property for all properties in the ontology file.
        """
        valid_required = True

        for item in Ontology.defines:
            if is_property(Ontology.defines[item]):
                prop = Ontology.defines[item]

                if PARENT in prop:
                    base = Ontology.defines[prop[PARENT]]

                    if not prop[PREFIXED[REQUIRED]] and\
                            base[PREFIXED[REQUIRED]]:
                        base_name = prop[PARENT]
                        self.write_debug_message(
                            "The 'dli:required' attribute value is false "
                            f"for property '{item}' and is true for the "
                            f"base property '{base_name}'")

                        valid_required = False

        if not valid_required:
            self.write_validation_message()

        return valid_required
