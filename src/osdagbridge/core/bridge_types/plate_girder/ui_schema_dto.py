"""DTOs for UI schema definitions used by Additional Inputs dialogs.

These replace the plain ``dict`` schema literals previously defined in
``ui_fields_additional_input``.  Every attribute maps 1-to-1 to the
former dict key of the same name so that consumer code changes are
purely mechanical (``obj.get("key")`` → ``obj.key``).

All dataclasses are frozen to prevent accidental mutation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, Union

__all__ = [
    # Validators
    "DoubleRangeValidator",
    "IntRangeValidator",
    # Field DTOs
    "LineField",
    "ComboField",
    "ModeLineField",
    "ComputedField",
    "InlineLabelField",
    "RowField",
    # Section / grouping DTOs
    "Row",
    "Section",
    "CheckboxGroup",
    "CheckboxListSection",
    "DynamicCheckboxListSection",
    "CustomVehicleTableSection",
    "CustomLoadComboTableSection",
    "Card",
    "DescriptionBlock",
    # Schema DTOs
    "RowBasedSchema",
    "SectionBasedSchema",
    "CardBasedSchema",
    "CustomLoadTabSchema",
    "GirderDetailsSchema",
]

# ---------------------------------------------------------------------------
# Validator specs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DoubleRangeValidator:
    """Floating-point range validator (maps to ``QDoubleValidator``)."""
    bottom: float
    top: float
    decimals: int = 2
    notation: str = "standard"
    type: str = "double_range"


@dataclass(frozen=True)
class IntRangeValidator:
    """Integer range validator (maps to ``QIntValidator``)."""
    bottom: int
    top: int
    type: str = "int_range"


ValidatorSpec = Union[DoubleRangeValidator, IntRangeValidator]


# ---------------------------------------------------------------------------
# Individual field DTOs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LineField:
    """A ``QLineEdit`` field.  ``type`` is ``"line"`` or ``"number"`` —
    both are rendered identically."""
    id: str
    label: str
    bind: str
    type: str = "line"
    validator: Optional[ValidatorSpec] = None
    default: Optional[str] = None
    read_only: bool = False
    enabled: bool = True
    placeholder: Optional[str] = None
    on_text_changed: Optional[str] = None
    on_editing_finished: Optional[str] = None
    width: Optional[int] = None
    visible_for: Optional[tuple] = None


@dataclass(frozen=True)
class ComboField:
    """A ``QComboBox`` field."""
    id: str
    label: str
    bind: str
    choices: tuple
    type: str = "combo"
    default: Optional[str] = None
    enabled: bool = True
    on_change: Optional[str] = None
    enabled_choices: Optional[tuple] = None
    visible_for: Optional[tuple] = None
    include_all: bool = False


@dataclass(frozen=True)
class ModeLineField:
    """A paired ``QComboBox`` (mode) + ``QLineEdit`` (value) field."""
    id: str
    label: str
    bind_mode: str
    bind_value: str
    mode_choices: tuple
    type: str = "mode_line"
    default_mode: Optional[str] = None
    default_value: Optional[str] = None
    placeholder: Optional[str] = None
    on_mode_change: Optional[str] = None
    mode_width: Optional[int] = None
    value_width: Optional[int] = None
    enabled: bool = True
    visible_for: Optional[tuple] = None


@dataclass(frozen=True)
class ComputedField:
    """A read-only computed-value display field."""
    id: str
    label: str
    bind: str
    type: str = "computed"


@dataclass(frozen=True)
class InlineLabelField:
    """A static ``QLabel`` used inside a ``RowField``."""
    label: str
    type: str = "label"
    after_spacing: int = 0


@dataclass(frozen=True)
class RowField:
    """A horizontal row that contains multiple inline sub-fields.

    Used for layouts like the Deflection Control limit row.
    """
    row_fields: tuple  # tuple of InlineLabelField | LineField | ComboField …


# ---------------------------------------------------------------------------
# Section / grouping DTOs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Row:
    """A horizontal row of fields in a row-based schema."""
    fields: tuple  # tuple of field DTOs


@dataclass(frozen=True)
class CheckboxGroup:
    """One checkbox group within a ``Section`` that holds limit-state checks."""
    title: str
    bind: str
    items: tuple
    default_checked: bool = True


@dataclass(frozen=True)
class Section:
    """A labelled card section containing fields and/or checkbox groups."""
    title: str = ""
    fields: tuple = ()
    checkbox_groups: tuple = ()
    field_width: Optional[int] = None
    type: Optional[str] = None   # e.g. "input_group", "output_group", "computed_group"
    id: Optional[str] = None


@dataclass(frozen=True)
class CheckboxListSection:
    """A section rendered as a static list of checkboxes."""
    id: str
    title: str
    bind: str
    items: tuple
    type: str = "checkbox_list"
    default_checked: bool = True


@dataclass(frozen=True)
class DynamicCheckboxListSection:
    """A section whose checkbox items are populated at runtime."""
    id: str
    title: str
    bind: str
    type: str = "dynamic_checkbox_list"
    default_checked: bool = True


@dataclass(frozen=True)
class CustomVehicleTableSection:
    """A section rendered as a custom vehicle entry table."""
    id: str
    title: str
    bind: str
    add_button_bind: str
    type: str = "custom_vehicle_table"


@dataclass(frozen=True)
class CustomLoadComboTableSection:
    """A section rendered as a custom load combination table."""
    id: str
    title: str
    bind: str
    add_button_bind: str
    type: str = "custom_load_combo_table"


@dataclass(frozen=True)
class Card:
    """A titled card grouping used in ``CardBasedSchema``."""
    title: str
    sections: tuple
    field_width: int = 150


@dataclass(frozen=True)
class DescriptionBlock:
    """A descriptive text block rendered below the main form content."""
    title: str
    text: str


# ---------------------------------------------------------------------------
# Top-level schema DTOs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RowBasedSchema:
    """Schema whose top-level layout is a list of ``Row`` objects.

    Used by the Layout, Crash Barrier, Median, Railing, Wearing Course and
    Lane Details tabs.
    """
    id: str
    rows: tuple
    label_width: int = 200


@dataclass(frozen=True)
class SectionBasedSchema:
    """Schema whose top-level layout is a list of section-type objects.

    Used by Permanent Load, Live Load, Seismic, Wind, Temperature, Load
    Combination, Support Conditions and Design Options (Cont.) tabs.
    """
    id: str
    sections: tuple
    label_width: int = 200
    field_width: int = 150
    field_height: int = 28
    title: Optional[str] = None
    description: Optional[DescriptionBlock] = None


@dataclass(frozen=True)
class CardBasedSchema:
    """Schema whose top-level layout is a list of ``Card`` objects.

    Used by the Design Options tab.
    """
    id: str
    cards: tuple


@dataclass(frozen=True)
class CustomLoadTabSchema:
    """Schema for the Custom Load tab, whose fields are named attributes
    rather than an ordered list."""
    id: str
    label_width: int
    field_width: int
    load_case_choices: tuple
    load_type_choices: tuple
    load_case: ComboField
    custom_load_case_name: LineField
    load_type: ComboField
    point_left: LineField
    point_bearing: LineField
    line_left_start: LineField
    line_left_end: LineField
    line_bearing_start: LineField
    line_bearing_end: LineField


@dataclass(frozen=True)
class GirderDetailsSchema:
    """Schema for the Girder Details section (no top-level id)."""
    overview: tuple
    section_inputs: tuple
