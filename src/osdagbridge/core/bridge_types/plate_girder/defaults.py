"""Centralized defaults for Plate Girder Bridge."""
from .ui_fields_additional_input import (
    LAYOUT_TAB_SCHEMA,
    CRASH_BARRIER_TAB_SCHEMA,
    MEDIAN_TAB_SCHEMA,
    RAILING_TAB_SCHEMA,
    WEARING_COURSE_TAB_SCHEMA,
    LANE_DETAILS_TAB_SCHEMA,
    PERMANENT_LOAD_TAB_SCHEMA,
    LIVE_LOAD_TAB_SCHEMA,
    LOAD_COMBINATION_TAB_SCHEMA,
    SEISMIC_LOAD_TAB_SCHEMA,
    WIND_LOAD_TAB_SCHEMA,
    TEMPERATURE_LOAD_TAB_SCHEMA,
    CUSTOM_LOAD_TAB_SCHEMA,
    DESIGN_OPTIONS_SCHEMA,
    DESIGN_OPTIONS_CONT_SCHEMA,
    SUPPORT_CONDITIONS_SCHEMA,
)

#--------------Inp-dict-Start--------------
from osdagbridge.core.utils.common import (
    KEY_STRUCTURE_TYPE, KEY_PROJECT_LOCATION, KEY_SPAN, KEY_CARRIAGEWAY_WIDTH, KEY_INCLUDE_MEDIAN,
    KEY_FOOTPATH, KEY_SKEW_ANGLE, KEY_DESIGN_MODE, KEY_GIRDER, KEY_CROSS_BRACING, KEY_END_DIAPHRAGM, KEY_DECK_CONCRETE_GRADE_BASIC,
    connectdb,
)
steel_properties = connectdb("Steel_Grade_Properties")
concrete_properies = connectdb("Concrete_Grade_Properties")


def _schema_default_keys(schema):
    """Return {tab_id.field_id: None} for every field in a schema that declares a default.

    Recursively traverses any schema structure (rows, sections, cards, fields, etc.)
    so it works regardless of the top-level layout key used.  Both plain dicts
    and frozen dataclasses (converted via ``dataclasses.asdict``) are supported.
    """
    import dataclasses

    if dataclasses.is_dataclass(schema) and not isinstance(schema, type):
        schema = dataclasses.asdict(schema)

    tab_id = schema.get("id", "")
    if not tab_id:
        return {}

    result = {}

    def _collect(obj):
        if isinstance(obj, dict):
            if "id" in obj and "default" in obj:
                result[f"{tab_id}.{obj['id']}"] = None
            for v in obj.values():
                _collect(v)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                _collect(item)

    _collect(schema)
    return result


DEFAULTS_DICT = {
    # Input Dock Defaults
    KEY_STRUCTURE_TYPE: "Highway Bridge",
    KEY_PROJECT_LOCATION: None,
    KEY_SPAN: None,
    KEY_CARRIAGEWAY_WIDTH: None,
    KEY_INCLUDE_MEDIAN: "No",
    KEY_FOOTPATH: "None",
    KEY_SKEW_ANGLE: None,
    KEY_DESIGN_MODE: "Optimized",
    KEY_GIRDER: steel_properties[0],
    KEY_CROSS_BRACING: steel_properties[0],
    KEY_END_DIAPHRAGM: steel_properties[0],
    KEY_DECK_CONCRETE_GRADE_BASIC: concrete_properies[0],

    # Additional Inputs Defaults
    **_schema_default_keys(LAYOUT_TAB_SCHEMA),
    **_schema_default_keys(CRASH_BARRIER_TAB_SCHEMA),
    **_schema_default_keys(MEDIAN_TAB_SCHEMA),
    **_schema_default_keys(RAILING_TAB_SCHEMA),
    **_schema_default_keys(WEARING_COURSE_TAB_SCHEMA),
    **_schema_default_keys(LANE_DETAILS_TAB_SCHEMA),
    **_schema_default_keys(PERMANENT_LOAD_TAB_SCHEMA),
    **_schema_default_keys(LIVE_LOAD_TAB_SCHEMA),
    **_schema_default_keys(LOAD_COMBINATION_TAB_SCHEMA),
    **_schema_default_keys(SEISMIC_LOAD_TAB_SCHEMA),
    **_schema_default_keys(WIND_LOAD_TAB_SCHEMA),
    **_schema_default_keys(TEMPERATURE_LOAD_TAB_SCHEMA),
    **_schema_default_keys(CUSTOM_LOAD_TAB_SCHEMA),
    **_schema_default_keys(DESIGN_OPTIONS_SCHEMA),
    **_schema_default_keys(DESIGN_OPTIONS_CONT_SCHEMA),
    **_schema_default_keys(SUPPORT_CONDITIONS_SCHEMA),

}
#--------------Inp-dict-End----------------
