"""Consolidated UI schemas for plate girder Additional Inputs dialogs.

This module groups all schema objects used by the Additional Inputs
flow, including Typical Section Details, Support/Design options, and
Member Properties.  Schemas are expressed as frozen dataclasses defined
in :mod:`ui_schema_dto` instead of plain dictionaries.
"""

from osdagbridge.core.bridge_types.plate_girder.ui_schema_dto import (
    DoubleRangeValidator,
    IntRangeValidator,
    LineField,
    ComboField,
    ModeLineField,
    ComputedField,
    InlineLabelField,
    RowField,
    Row,
    Section,
    CheckboxGroup,
    CheckboxListSection,
    DynamicCheckboxListSection,
    CustomVehicleTableSection,
    CustomLoadComboTableSection,
    Card,
    DescriptionBlock,
    RowBasedSchema,
    SectionBasedSchema,
    CardBasedSchema,
    CustomLoadTabSchema,
    GirderDetailsSchema,
)
from osdagbridge.core.utils.common import (
    DEFAULT_CRASH_BARRIER_WIDTH,
    DEFAULT_GIRDER_SPACING,
    DEFAULT_RAILING_WIDTH,
    MIN_FOOTPATH_WIDTH,
    MIN_RAILING_HEIGHT,
    VALUES_GIRDER_DESIGN_MODE,
    VALUES_GIRDER_SPAN_MODE,
    VALUES_GIRDER_SYMMETRY,
    VALUES_GIRDER_TYPE,
    VALUES_PROFILE_SCOPE,
    VALUES_TORSIONAL_RESTRAINT,
    VALUES_WARPING_RESTRAINT,
    VALUES_WEB_TYPE,
    VALUES_RAILING_TYPE,
    VALUES_WEARING_COAT_MATERIAL,
)

LAYOUT_TAB_SCHEMA = RowBasedSchema(
    id="layout_tab",
    rows=(
        Row(fields=(
            LineField(
                id="girder_spacing",
                label="Girder Spacing (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.01, top=50.0, decimals=3),
                default=str(DEFAULT_GIRDER_SPACING),
                bind="girder_spacing",
                on_text_changed="on_girder_spacing_changed",
            ),
            LineField(
                id="no_of_girders",
                label="No. of Girders:",
                type="line",
                validator=IntRangeValidator(bottom=1, top=100),
                bind="no_of_girders",
                on_editing_finished="on_no_of_girders_changed",
            ),
        )),
        Row(fields=(
            LineField(
                id="deck_overhang",
                label="Deck Overhang Width (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=100.0, decimals=3),
                bind="deck_overhang",
                on_text_changed="on_deck_overhang_changed",
            ),
        )),
        Row(fields=(
            LineField(
                id="overall_bridge_width_display",
                label="Overall Bridge Width (m):",
                type="line",
                read_only=True,
                bind="overall_bridge_width_display",
                on_text_changed="_reject_overall_width_override",
            ),
        )),
        Row(fields=(
            LineField(
                id="deck_thickness",
                label="Deck Thickness (mm):",
                type="line",
                validator=DoubleRangeValidator(bottom=100.0, top=500.0, decimals=0),
                default="200",
                bind="deck_thickness",
                on_editing_finished="validate_deck_thickness",
            ),
        )),
        Row(fields=(
            LineField(
                id="footpath_width",
                label="Footpath Width (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=MIN_FOOTPATH_WIDTH, top=5.0, decimals=3),
                default=f"{MIN_FOOTPATH_WIDTH:.2f}",
                bind="footpath_width",
                on_text_changed="on_footpath_width_changed",
            ),
            LineField(
                id="footpath_thickness",
                label="Footpath Thickness (mm):",
                type="line",
                validator=DoubleRangeValidator(bottom=100.0, top=500.0, decimals=0),
                default="200",
                bind="footpath_thickness",
                on_editing_finished="validate_footpath_thickness",
            ),
        )),
    ),
)

CRASH_BARRIER_TAB_SCHEMA = RowBasedSchema(
    id="crash_barrier_tab",
    label_width=210,
    rows=(
        Row(fields=(
            ComboField(
                id="crash_barrier_type",
                label="Type:",
                choices=(
                    "IRC 5 - RCC Crash Barrier",
                    "IRC 5 - High Containment RCC Crash Barrier",
                    "IRC 5 - Metallic Crash Barrier with Single W-Beam",
                    "IRC 5 - Metallic Crash Barrier with Double W-Beam",
                    "Custom",
                ),
                bind="crash_barrier_type",
                on_change="on_crash_barrier_type_changed",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_density",
                label="Material Density (kN/m\u00b3):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=100.0, decimals=2),
                bind="crash_barrier_density",
                on_editing_finished="_auto_compute_crash_barrier_load",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_width",
                label="Width (m):",
                type="line",
                default=str(DEFAULT_CRASH_BARRIER_WIDTH),
                validator=DoubleRangeValidator(bottom=0.0, top=2.0, decimals=3),
                bind="crash_barrier_width",
                on_text_changed="recalculate_girders",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_height",
                label="Height (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=3.0, decimals=3),
                bind="crash_barrier_height",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_area",
                label="Area (m\u00b2):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=10.0, decimals=4),
                bind="crash_barrier_area",
                on_editing_finished="_auto_compute_crash_barrier_load",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_load",
                label="Load (kN/m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=500.0, decimals=3),
                bind="crash_barrier_load",
            ),
        )),
        Row(fields=(
            LineField(
                id="crash_barrier_post_spacing",
                label="Spacing between Posts (m):",
                type="line",
                default="1",
                validator=DoubleRangeValidator(bottom=0.0, top=10.0, decimals=3),
                bind="crash_barrier_post_spacing",
            ),
        )),
    ),
)

MEDIAN_TAB_SCHEMA = RowBasedSchema(
    id="median_tab",
    label_width=210,
    rows=(
        Row(fields=(
            ComboField(
                id="median_type",
                label="Type:",
                choices=(
                    "IRC 5 - Raised Kerb",
                    "IRC 5 - RCC Crash Barrier",
                    "IRC 5 - Metallic Crash Barrier with Single W-Beam",
                    "IRC 5 - Metallic Crash Barrier with Double W-Beam",
                    "Custom",
                ),
                bind="median_type",
                on_change="on_median_type_changed",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_density",
                label="Material Density (kN/m\u00b3):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=100.0, decimals=2),
                bind="median_density",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_width",
                label="Width (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=3.0, decimals=3),
                bind="median_width",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_height",
                label="Height (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=3.0, decimals=3),
                bind="median_height",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_area",
                label="Area (m\u00b2):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=10.0, decimals=4),
                bind="median_area",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_load",
                label="Load (kN/m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=500.0, decimals=3),
                bind="median_load",
            ),
        )),
        Row(fields=(
            LineField(
                id="median_post_spacing",
                label="Spacing between Posts (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=10.0, decimals=3),
                bind="median_post_spacing",
                default="1",
            ),
        )),
    ),
)

RAILING_TAB_SCHEMA = RowBasedSchema(
    id="railing_tab",
    label_width=180,
    rows=(
        Row(fields=(
            ComboField(
                id="railing_type",
                label="Type:",
                choices=tuple(VALUES_RAILING_TYPE),
                bind="railing_type",
            ),
        )),
        Row(fields=(
            LineField(
                id="railing_width",
                label="Width (mm):",
                type="line",
                default=f"{DEFAULT_RAILING_WIDTH * 1000:.0f}",
                validator=DoubleRangeValidator(bottom=0.0, top=2000.0, decimals=1),
                bind="railing_width",
                on_text_changed="recalculate_girders",
            ),
        )),
        Row(fields=(
            LineField(
                id="railing_height",
                label="Height (m):",
                type="line",
                validator=DoubleRangeValidator(bottom=MIN_RAILING_HEIGHT, top=3.0, decimals=3),
                bind="railing_height",
                on_editing_finished="validate_railing_height",
            ),
        )),
        Row(fields=(
            ComboField(
                id="railing_load_mode",
                label="Load Mode:",
                choices=("Automatic (IRC 6)", "User-defined"),
                bind="railing_load_mode",
                on_change="on_railing_load_mode_changed",
            ),
            LineField(
                id="railing_load_value",
                label="Load (kN/m):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=50.0, decimals=2),
                placeholder="Value",
                bind="railing_load_value",
                enabled=False,
            ),
        )),
    ),
)

WEARING_COURSE_TAB_SCHEMA = RowBasedSchema(
    id="wearing_course_tab",
    label_width=200,
    rows=(
        Row(fields=(
            ComboField(
                id="wearing_material",
                label="Material:",
                choices=tuple(VALUES_WEARING_COAT_MATERIAL),
                bind="wearing_material",
                on_change="on_wearing_material_changed",
            ),
        )),
        Row(fields=(
            LineField(
                id="wearing_density",
                label="Density (kN/m\u00b3):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=40.0, decimals=2),
                bind="wearing_density",
                default="24.0",
            ),
        )),
        Row(fields=(
            LineField(
                id="wearing_thickness",
                label="Thickness (mm):",
                type="line",
                validator=DoubleRangeValidator(bottom=0.0, top=200.0, decimals=1),
                bind="wearing_thickness",
                default="50",
            ),
        )),
    ),
)

LANE_DETAILS_TAB_SCHEMA = RowBasedSchema(
    id="lane_details_tab",
    rows=(
        Row(fields=(
            ComboField(
                id="lane_count",
                label="No. of Traffic Lanes:",
                choices=tuple(str(i) for i in range(1, 7)),
                bind="lane_count_combo",
                on_change="on_lane_count_changed",
            ),
        )),
    ),
)

PERMANENT_LOAD_TAB_SCHEMA = SectionBasedSchema(
    id="permanent_load_tab",
    label_width=220,
    sections=(
        Section(
            title="Dead Load (DL)",
            fields=(
                LineField(
                    id="self_weight_factor",
                    label="Self-weight modification factor",
                    type="line",
                    validator=DoubleRangeValidator(bottom=0.0, top=10.0, decimals=2),
                    default="1.00",
                    bind="self_weight_factor_input",
                ),
            ),
        ),
    ),
)

LIVE_LOAD_TAB_SCHEMA = SectionBasedSchema(
    id="live_load_tab",
    label_width=220,
    field_width=180,
    field_height=28,
    sections=(
        CheckboxListSection(
            id="irc_vehicles_section",
            title="Vehicles from IRC 6",
            items=(
                "Class A",
                "Class 70R Wheeled",
                "Class 70R Tracked",
                "Class AA Wheeled",
                "Class AA Tracked",
                "Class SV",
                "Class 70R Bogie",
            ),
            bind="irc_vehicle_checkboxes",
            default_checked=True,
        ),
        CustomVehicleTableSection(
            id="custom_vehicle_section",
            title="Custom Vehicle",
            bind="custom_vehicle_table",
            add_button_bind="custom_vehicle_add_button",
        ),
        DynamicCheckboxListSection(
            id="braking_section",
            title="Braking Load from Vehicles",
            bind="braking_vehicle_checkboxes",
            default_checked=True,
        ),
        LineField(
            id="eccentricity",
            label="Eccentricity from top of Deck (m)",
            type="line",
            validator=DoubleRangeValidator(bottom=0.0, top=100.0, decimals=2),
            default="0.00",
            bind="eccentricity_input",
        ),
        ModeLineField(
            id="footpath_pressure",
            label="Footpath Pressure (kN/mm\u00b2)",
            mode_choices=("Automatic", "User-defined"),
            default_mode="Automatic",
            bind_mode="footpath_mode_combo",
            bind_value="footpath_value_input",
            default_value="5.00",
            mode_width=120,
            value_width=80,
            on_mode_change="_on_footpath_mode_changed",
        ),
    ),
    description=DescriptionBlock(
        title="Description Box",
        text=(
            "211.2 The braking effect on a simply supported span or a continuous unit of spans or on any other type of bridge unit shall be assumed to have the following value:\n\n"
            "a) In the case of a single lane or a two lane bridge: twenty percent of the first train "
            "load plus ten percent of the load of the succeeding trains or part thereof, the train "
            "loads in one lane only being considered for the purpose of this subclause. Where the "
            "entire first train is not on the full span, the braking force shall be taken as equal to "
            "twenty percent of the loads actually on the span or continuous unit of spans.\n"
            "b) In the case of bridges having more than two lanes: as in (a) above for the first two "
            "lanes plus five percent of the loads on the lanes in excess of two."
        ),
    ),
)

SEISMIC_LOAD_TAB_SCHEMA = SectionBasedSchema(
    id="seismic_load_tab",
    label_width=220,
    field_width=180,
    field_height=28,
    sections=(
        Section(
            id="seismic_inputs_section",
            title="Seismic/Earthquake Load (EL) Inputs",
            type="input_group",
            fields=(
                LineField(
                    id="seismic_zone",
                    label="Seismic Zone",
                    type="line",
                    bind="seismic_zone_combo",
                ),
                LineField(
                    id="importance_factor",
                    label="Importance Factor, I",
                    type="line",
                    default="1.0",
                    bind="importance_factor_input",
                ),
                ComboField(
                    id="soil_type",
                    label="Type of Soil",
                    choices=(
                        "Type I \u2013 Rocky or Hard",
                        "Type II \u2013 Medium Soil",
                        "Type III \u2013 Soft Soil",
                    ),
                    default="Type I \u2013 Rocky or Hard Soil",
                    bind="soil_type_combo",
                ),
                LineField(
                    id="time_period",
                    label="Fundamental Time Period, T (sec)",
                    type="line",
                    bind="time_period_input",
                ),
                LineField(
                    id="damping",
                    label="Damping Percentage",
                    type="line",
                    default="2",
                    bind="damping_input",
                ),
                ComboField(
                    id="response_reduction_factor",
                    label="Response Reduction Factor, R",
                    choices=("1", "2", "3", "4", "5"),
                    default="1",
                    bind="response_factor_combo",
                ),
                ModeLineField(
                    id="dead_load_seismic",
                    label="Dead Load for Seismic Force (kN)",
                    mode_choices=("Automatic", "Custom"),
                    default_mode="Automatic",
                    bind_mode="dead_load_seismic_combo",
                    bind_value="dead_load_custom_input",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_seismic_custom_inputs",
                ),
                ModeLineField(
                    id="live_load_seismic",
                    label="Live Load for Seismic Force (kN)",
                    mode_choices=("Automatic", "Custom"),
                    default_mode="Automatic",
                    bind_mode="live_load_seismic_combo",
                    bind_value="live_load_custom_input",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_seismic_custom_inputs",
                ),
            ),
        ),
        Section(
            id="computed_values_section",
            title="Computed Values",
            type="computed_group",
            fields=(
                ComputedField(id="zone_factor", label="Zone Factor, Z", bind="zone_factor"),
                ComputedField(
                    id="spectral_coeff",
                    label="Spectral Acceleration Coefficient, S<sub>a</sub>/g",
                    bind="spectral_coeff",
                ),
                ComputedField(
                    id="horizontal_coeff",
                    label="Horizontal Seismic Coefficient, A<sub>h</sub>",
                    bind="horizontal_coeff",
                ),
                ComputedField(
                    id="vertical_coeff",
                    label="Vertical Seismic Coefficient, A<sub>v</sub>",
                    bind="vertical_coeff",
                ),
            ),
        ),
    ),
    description=DescriptionBlock(
        title="Description Box",
        text=(
            "Seismic Zone is auto-filled from software output (project location).\n\n"
            "The spectral acceleration coefficient depends on soil type and "
            "fundamental time period, T.\n\n"
        ),
    ),
)

WIND_LOAD_TAB_SCHEMA = SectionBasedSchema(
    id="wind_load_tab",
    label_width=260,
    field_width=140,
    field_height=28,
    sections=(
        Section(
            id="wind_inputs_section",
            title="Wind Load (WL) Inputs",
            type="input_group",
            fields=(
                LineField(
                    id="basic_wind_speed",
                    label="Basic Wind Speed, V<sub>b</sub> (m/s)",
                    type="line",
                    read_only=True,
                    enabled=False,
                    bind="basic_wind_speed_input",
                ),
                LineField(
                    id="avg_exposed_height",
                    label="Average Exposed Height, H (m)",
                    type="line",
                    default="10",
                    placeholder="10",
                    bind="avg_exposed_height_input",
                ),
                ComboField(
                    id="terrain_type",
                    label="Type of Terrain",
                    choices=("Plain Terrain", "Terrain with \nObstructions"),
                    default="Plain Terrain",
                    bind="terrain_type_combo",
                ),
                ComboField(
                    id="site_topography",
                    label="Site Topography",
                    choices=("Flat", "Hill, ridge, escarpment or cliff"),
                    default="Flat",
                    bind="site_topography_combo",
                ),
                ModeLineField(
                    id="gust_factor",
                    label="Gust Factor, G",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="gust_factor_combo",
                    bind_value="gust_factor_value",
                    default_value="2",
                    placeholder="2",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="drag_coeff",
                    label="Drag Coefficient, C<sub>D</sub>",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="drag_coeff_combo",
                    bind_value="drag_coeff_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="drag_coeff_ll",
                    label="Drag Coefficient against Live Load, C<sub>DLL</sub>",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="drag_coeff_ll_combo",
                    bind_value="drag_coeff_ll_value",
                    default_value="1.2",
                    placeholder="1.2",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="lift_coeff",
                    label="Lift Coefficient, C<sub>L</sub>",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="lift_coeff_combo",
                    bind_value="lift_coeff_value",
                    default_value="0.75",
                    placeholder="0.75",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="super_area_elev",
                    label="Superstructure Area in Elevation, A<sub>1</sub> (m\u00b2)",
                    mode_choices=("Automatic", "Custom"),
                    default_mode="Automatic",
                    bind_mode="super_area_elev_combo",
                    bind_value="super_area_elev_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="super_area_plain",
                    label="Superstructure Area in Plain, A<sub>3</sub> (m\u00b2)",
                    mode_choices=("Automatic", "Custom"),
                    default_mode="Automatic",
                    bind_mode="super_area_plain_combo",
                    bind_value="super_area_plain_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="exposed_frontal_area",
                    label="Exposed Frontal Area of Live Load, A<sub>1LL</sub> (m\u00b2)",
                    mode_choices=("Automatic", "Custom"),
                    default_mode="Automatic",
                    bind_mode="exposed_frontal_area_combo",
                    bind_value="exposed_frontal_area_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="wind_ecc_deck",
                    label="Wind Load Eccentricity from \nTop of Deck (m)",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="wind_ecc_deck_combo",
                    bind_value="wind_ecc_deck_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
                ModeLineField(
                    id="wind_ll_ecc",
                    label="Wind on Live Load Eccentricity from \nTop of Deck (m)",
                    mode_choices=("As per Code", "Custom"),
                    default_mode="As per Code",
                    bind_mode="wind_ll_ecc_combo",
                    bind_value="wind_ll_ecc_value",
                    placeholder="Custom Value",
                    on_mode_change="_toggle_wind_custom_input",
                ),
            ),
        ),
        Section(
            id="computed_values_section",
            title="Computed Values",
            type="computed_group",
            fields=(
                ComputedField(
                    id="hourly_mean_wind",
                    label="Hourly Mean Wind Speed, V<sub>z</sub> (m/s)",
                    bind="hourly_mean_wind",
                ),
                ComputedField(
                    id="hourly_wind_pressure",
                    label="Hourly Wind Pressure, P<sub>z</sub> (N/m\u00b2)",
                    bind="hourly_wind_pressure",
                ),
                ComputedField(
                    id="transverse_wind_force",
                    label="Transverse Wind Force, F<sub>T</sub> (N)",
                    bind="transverse_wind_force",
                ),
                ComputedField(
                    id="longitudinal_wind_force",
                    label="Longitudinal Wind Force, F<sub>L</sub> (N)",
                    bind="longitudinal_wind_force",
                ),
                ComputedField(
                    id="vertical_wind_force",
                    label="Vertical Wind Force, F<sub>V</sub> (N)",
                    bind="vertical_wind_force",
                ),
                ComputedField(
                    id="transverse_wind_ll",
                    label="Transverse Wind Force on Live Load, F<sub>TLL</sub> (N)",
                    bind="transverse_wind_ll",
                ),
                ComputedField(
                    id="longitudinal_wind_ll",
                    label="Longitudinal Wind Force on Live Load, F<sub>LLL</sub> (N)",
                    bind="longitudinal_wind_ll",
                ),
            ),
        ),
    ),
    description=DescriptionBlock(
        title="Description Box",
        text="Basic Wind Speed is auto-filled from software output (project location).\n\n",
    ),
)

TEMPERATURE_LOAD_TAB_SCHEMA = SectionBasedSchema(
    id="temperature_load_tab",
    label_width=240,
    field_width=140,
    sections=(
        Section(
            id="temperature_inputs_section",
            title="Temperature Load (TL) Inputs for Evaluation per IRC6",
            type="input_group",
            fields=(
                LineField(
                    id="highest_max_temp",
                    label="Highest Maximum Air Temperature (\u00b0C)",
                    type="line",
                    placeholder="From Project Location",
                    bind="highest_max_temp_input",
                    validator=DoubleRangeValidator(bottom=-50.0, top=100.0, decimals=2),
                    enabled=False,
                ),
                LineField(
                    id="lowest_min_temp",
                    label="Lowest Minimum Air Temperature (\u00b0C)",
                    type="line",
                    placeholder="From Project Location",
                    bind="lowest_min_temp_input",
                    validator=DoubleRangeValidator(bottom=-50.0, top=100.0, decimals=2),
                    enabled=False,
                ),
                LineField(
                    id="thermal_coeff_steel",
                    label="Coefficient of Thermal Expansion for Steel (1/\u00b0C)",
                    type="line",
                    default="12.0e-6",
                    bind="thermal_coeff_steel_input",
                    validator=DoubleRangeValidator(bottom=0.0, top=1.0, decimals=8, notation="scientific"),
                ),
                LineField(
                    id="thermal_coeff_rcc",
                    label="Coefficient of Thermal Expansion for RCC (1/\u00b0C)",
                    type="line",
                    default="12.0e-6",
                    bind="thermal_coeff_rcc_input",
                    validator=DoubleRangeValidator(bottom=0.0, top=1.0, decimals=8, notation="scientific"),
                ),
            ),
        ),
        Section(
            id="bridge_temp_range_section",
            title="Range of Effective Bridge Temperature:",
            type="output_group",
            fields=(
                LineField(
                    id="bridge_temp_min",
                    label="Minimum (\u00b0C)",
                    type="line",
                    read_only=True,
                    bind="bridge_temp_min_input",
                ),
                LineField(
                    id="bridge_temp_max",
                    label="Maximum (\u00b0C)",
                    type="line",
                    read_only=True,
                    bind="bridge_temp_max_input",
                ),
            ),
        ),
        Section(
            id="temp_design_section",
            title="Temperature for Design",
            type="output_group",
            fields=(
                LineField(
                    id="temp_rise",
                    label="Rise (\u00b0C)",
                    type="line",
                    read_only=True,
                    bind="temp_rise_input",
                ),
                LineField(
                    id="temp_fall",
                    label="Fall (\u00b0C)",
                    type="line",
                    read_only=True,
                    bind="temp_fall_input",
                ),
            ),
        ),
    ),
)

CUSTOM_LOAD_TAB_SCHEMA = CustomLoadTabSchema(
    id="custom_load_tab",
    label_width=260,
    field_width=140,
    load_case_choices=("DL", "DW", "SIDL", "LL", "EL", "WL", "TL", "Custom"),
    load_type_choices=("Point", "Line", "Area"),
    load_case=ComboField(
        id="custom_load_case",
        label="Load Case",
        choices=("DL", "DW", "SIDL", "LL", "EL", "WL", "TL", "Custom"),
        bind="custom_load_case_combo",
    ),
    custom_load_case_name=LineField(
        id="custom_load_case_name",
        label="",
        type="line",
        placeholder="Custom",
        bind="custom_load_case_name_input",
        enabled=False,
    ),
    load_type=ComboField(
        id="custom_load_type",
        label="Load Type",
        choices=("Point", "Line", "Area"),
        bind="custom_load_type_combo",
    ),
    point_left=LineField(
        id="custom_point_left",
        label="Distance from Left Edge of Bridge (m)",
        type="line",
        bind="custom_point_left_input",
        validator=DoubleRangeValidator(bottom=0.0, top=1000.0, decimals=3),
    ),
    point_bearing=LineField(
        id="custom_point_bearing",
        label="Distance from Center Line of Bearing (m)",
        type="line",
        bind="custom_point_bearing_input",
        validator=DoubleRangeValidator(bottom=-1000.0, top=1000.0, decimals=3),
    ),
    line_left_start=LineField(
        id="custom_line_left_start",
        label="Distance from Left Edge of Bridge (m):",
        type="line",
        bind="custom_line_left_start",
        width=70,
        validator=DoubleRangeValidator(bottom=0.0, top=1000.0, decimals=3),
    ),
    line_left_end=LineField(
        id="custom_line_left_end",
        label="",
        type="line",
        bind="custom_line_left_end",
        width=70,
        validator=DoubleRangeValidator(bottom=0.0, top=1000.0, decimals=3),
    ),
    line_bearing_start=LineField(
        id="custom_line_bearing_start",
        label="Distance from Center Line of Bearing (m):",
        type="line",
        bind="custom_line_bearing_start",
        width=70,
        validator=DoubleRangeValidator(bottom=-1000.0, top=1000.0, decimals=3),
    ),
    line_bearing_end=LineField(
        id="custom_line_bearing_end",
        label="",
        type="line",
        bind="custom_line_bearing_end",
        width=70,
        validator=DoubleRangeValidator(bottom=-1000.0, top=1000.0, decimals=3),
    ),
)

LOAD_COMBINATION_TAB_SCHEMA = SectionBasedSchema(
    id="load_combination_tab",
    label_width=280,
    sections=(
        DynamicCheckboxListSection(
            id="irc_load_combos_section",
            title="Load Combinations from IRC 6",
            bind="irc_load_combos_checkboxes",
            default_checked=False,
        ),
        CustomLoadComboTableSection(
            id="custom_load_combo_section",
            title="Custom Load Combination",
            bind="custom_load_combo_table",
            add_button_bind="load_combo_add_btn",
        ),
    ),
)

SUPPORT_CONDITIONS_SCHEMA = SectionBasedSchema(
    id="support_conditions",
    title="Support Conditions",
    sections=(
        Section(
            title="Support Conditions",
            fields=(
                ComboField(
                    id="left_support",
                    label="Left Support",
                    choices=("Fixed", "Pinned", "Roller"),
                    default="Pinned",
                    enabled_choices=("Pinned",),
                    bind="left_support_combo",
                ),
                ComboField(
                    id="right_support",
                    label="Right Support",
                    choices=("Fixed", "Pinned", "Roller"),
                    default="Roller",
                    enabled_choices=("Roller",),
                    bind="right_support_combo",
                ),
            ),
        ),
        Section(
            title="Bearing length",
            fields=(
                LineField(
                    id="bearing_length",
                    label="Bearing Length Value (mm)",
                    type="line",
                    default="400.00",
                    placeholder="Length",
                    bind="bearing_length_input",
                    validator=DoubleRangeValidator(bottom=0.00, top=600.00, decimals=3),
                ),
            ),
        ),
    ),
)

DESIGN_OPTIONS_SCHEMA = CardBasedSchema(
    id="design_options",
    cards=(
        # ---------------- Construction ----------------
        Card(
            title="Construction Stages",
            field_width=150,
            sections=(
                Section(
                    fields=(
                        ComboField(
                            id="construction_stage",
                            label="Include automatic",
                            choices=("Yes", "No"),
                            default="Yes",
                            bind="construction_stage_combo",
                        ),
                    ),
                ),
            ),
        ),

        # ---------------- Deck Design ----------------
        Card(
            title="Deck Design",
            field_width=150,
            sections=(
                Section(
                    fields=(
                        ComboField(
                            id="reinforcement_size",
                            label="Reinforcement Size",
                            choices=(
                                "4 mm", "5 mm", "6 mm", "8 mm", "10 mm",
                                "12 mm", "16 mm", "20 mm", "25 mm", "28 mm",
                                "32 mm", "36 mm", "40 mm",
                            ),
                            default="12 mm",
                            bind="reinforcement_size_combo",
                        ),
                        ComboField(
                            id="reinforcement_material",
                            label="Reinforcement Material",
                            choices=(
                                "Fe 415", "Fe 415D", "Fe 500", "Fe 500D",
                                "Fe 550", "Fe 550D", "Fe 600",
                            ),
                            default="Fe 500",
                            bind="reinforcement_material_combo",
                        ),
                        LineField(
                            id="top_clear_cover",
                            label="Top Clear Cover (mm)",
                            type="number",
                            default="50.0",
                            validator=DoubleRangeValidator(bottom=40.00, top=75.0, decimals=1),
                            bind="top_clear_cover_input",
                        ),
                        LineField(
                            id="bottom_clear_cover",
                            label="Bottom Clear Cover (mm)",
                            type="number",
                            default="40.0",
                            validator=DoubleRangeValidator(bottom=35.0, top=75.0, decimals=1),
                            bind="bottom_clear_cover_input",
                        ),
                        LineField(
                            id="side_clear_cover",
                            label="Side Clear Cover (mm)",
                            type="number",
                            default="40.0",
                            validator=DoubleRangeValidator(bottom=35.0, top=75.0, decimals=1),
                            bind="side_clear_cover_input",
                        ),
                    ),
                ),
            ),
        ),

        # ---------------- Shear Studs ----------------
        Card(
            title="Shear Studs",
            field_width=150,
            sections=(
                Section(
                    fields=(
                        LineField(
                            id="shear_stud_yield_strength",
                            label="Yield Strength (MPa)",
                            type="line",
                            default="385.00",
                            validator=DoubleRangeValidator(bottom=350, top=600, decimals=2),
                            bind="shear_stud_yield_strength_input",
                        ),
                        LineField(
                            id="shear_stud_ultimate_strength",
                            label="Ultimate Strength (MPa)",
                            type="line",
                            default="495.00",
                            validator=DoubleRangeValidator(bottom=350, top=600, decimals=2),
                            bind="shear_stud_ultimate_strength_input",
                        ),
                        ComboField(
                            id="shear_stud_diameter",
                            label="Diameter (mm)",
                            choices=("12", "16", "20", "22", "25"),
                            default="20",
                            bind="shear_stud_diameter_combo",
                        ),
                        LineField(
                            id="shear_stud_height",
                            label="Height (mm)",
                            type="line",
                            default="100.00",
                            validator=DoubleRangeValidator(bottom=0.0, top=500.0, decimals=2),
                            bind="shear_stud_height_input",
                        ),
                        ComboField(
                            id="shear_stud_count",
                            label="No. of Shear Studs per Section",
                            choices=tuple(str(i) for i in range(1, 11)),
                            default="2",
                            bind="shear_stud_count_combo",
                        ),
                        LineField(
                            id="shear_stud_transverse_spacing",
                            label="Transverse Spacing (mm)",
                            type="line",
                            default="100.00",
                            validator=DoubleRangeValidator(bottom=0.0, top=5000.0, decimals=2),
                            bind="shear_stud_spacing_input",
                        ),
                    ),
                ),
            ),
        ),
    ),
)

DESIGN_OPTIONS_CONT_SCHEMA = SectionBasedSchema(
    id="design_options_cont",
    sections=(
        # ---------------- Partial Factor ----------------
        Section(
            title="Partial Factor",
            fields=(
                LineField(
                    id="gamma_c_basic",
                    label="Concrete basic & seismic, &#947;<sub>c</sub>",
                    type="line",
                    default="1.50",
                    bind="gamma_c_basic_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_c_accidental",
                    label="Concrete Accidental, &#947;<sub>c</sub>",
                    type="line",
                    default="1.20",
                    bind="gamma_c_accidental_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_m0",
                    label="Structural steel for Yielding and Buckling, &#947;<sub>M0</sub>",
                    type="line",
                    default="1.10",
                    bind="gamma_m0_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_m1",
                    label="Structural Steel For Ultimate Stress, &#947;<sub>M1</sub>",
                    type="line",
                    default="1.25",
                    bind="gamma_m1_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_s",
                    label="Reinforcing Steel, &#947;<sub>s</sub>",
                    type="line",
                    default="1.15",
                    bind="gamma_s_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_v",
                    label="Shear Connectors For Yield, &#947;<sub>v</sub>",
                    type="line",
                    default="1.25",
                    bind="gamma_v_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_flt",
                    label="Fatigue Load, &#947;<sub>flt</sub>",
                    type="line",
                    default="1.00",
                    bind="gamma_flt_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
                LineField(
                    id="gamma_mf",
                    label="Fatigue Strength, &#947;<sub>Mf,t</sub>",
                    type="line",
                    default="1.35",
                    bind="gamma_mf_input",
                    validator=DoubleRangeValidator(bottom=1.0, top=2.0, decimals=2),
                ),
            ),
        ),

        # ---------------- Resistance to Fatigue ----------------
        Section(
            title="Resistance to Fatigue",
            fields=(
                LineField(
                    id="load_cycles",
                    label="Number of Load Cycles",
                    type="line",
                    default="2000000.00",
                    bind="load_cycles_input",
                    validator=DoubleRangeValidator(bottom=100000, top=100000000, decimals=2),
                ),
            ),
        ),

        # ---------------- Deflection Control ----------------
        Section(
            title="Deflection Control",
            fields=(
                RowField(
                    row_fields=(
                        InlineLabelField(label="Limit :", after_spacing=408),
                        InlineLabelField(label="L /"),
                        LineField(
                            id="limit_l",
                            label="",
                            type="line",
                            default="600.00",
                            bind="limit_input",
                            width=150,
                            validator=IntRangeValidator(bottom=300, top=800),
                        ),
                        InlineLabelField(label="m"),
                    ),
                ),
            ),
        ),

        # ---------------- Limit States ----------------
        Section(
            title="Limit States",
            checkbox_groups=(
                CheckboxGroup(
                    title="Ultimate Limit States",
                    items=(
                        "Bending Resistance",
                        "Resistance to Vertical Shear",
                        "Resistance to Lateral-torsional Buckling",
                        "Resistance to Transverse force",
                        "Resistance to Longitudinal Shear",
                        "Resistance to Fatigue",
                    ),
                    bind="ultimate_checkboxes",
                    default_checked=True,
                ),
                CheckboxGroup(
                    title="Serviceability Limit States",
                    items=(
                        "Stress Limitation",
                        "Longitudinal Shear (SLS)",
                        "Deflection Control",
                        "Crack Width Check",
                    ),
                    bind="service_checkboxes",
                    default_checked=True,
                ),
            ),
        ),
    ),
)

GIRDER_DETAILS_SCHEMA = GirderDetailsSchema(
    overview=(
        ComboField(
            id="select_girder",
            label="Select Girder:",
            choices=(),
            bind="select_girder_combo",
            include_all=True,
        ),
        ComboField(
            id="span",
            label="Span:",
            choices=tuple(VALUES_GIRDER_SPAN_MODE),
            bind="span_combo",
        ),
    ),
    section_inputs=(
        ComboField(
            id="design",
            label="Design:",
            choices=tuple(VALUES_GIRDER_DESIGN_MODE),
            bind="design_combo",
            visible_for=("welded",),
        ),
        ComboField(
            id="type",
            label="Type:",
            choices=tuple(VALUES_GIRDER_TYPE),
            bind="type_combo",
        ),
        ComboField(
            id="symmetry",
            label="Symmetry:",
            choices=tuple(VALUES_GIRDER_SYMMETRY),
            bind="symmetry_combo",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="depth",
            label="Total Depth (mm):",
            mode_choices=("Optimized", "Customized"),
            default_mode="Optimized",
            bind_mode="depth_mode_combo",
            bind_value="depth_input",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="top_flange_width",
            label="Top Flange Width (mm):",
            mode_choices=("Optimized", "Customized"),
            default_mode="Optimized",
            bind_mode="top_width_mode_combo",
            bind_value="top_width_input",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="top_flange_thickness",
            label="Top Flange Thickness (mm):",
            mode_choices=tuple(VALUES_PROFILE_SCOPE),
            default_mode="All",
            bind_mode="top_thickness_mode_combo",
            bind_value="top_thickness_input",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="bottom_flange_width",
            label="Bottom Flange Width (mm):",
            mode_choices=("Optimized", "Customized"),
            default_mode="Optimized",
            bind_mode="bottom_width_mode_combo",
            bind_value="bottom_width_input",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="bottom_flange_thickness",
            label="Bottom Flange Thickness (mm):",
            mode_choices=tuple(VALUES_PROFILE_SCOPE),
            default_mode="All",
            bind_mode="bottom_thickness_mode_combo",
            bind_value="bottom_thickness_input",
            visible_for=("welded",),
        ),
        ModeLineField(
            id="web_thickness",
            label="Web Thickness (mm):",
            mode_choices=tuple(VALUES_PROFILE_SCOPE),
            default_mode="All",
            bind_mode="web_thickness_mode_combo",
            bind_value="web_thickness_input",
            visible_for=("welded",),
        ),
        ComboField(
            id="is_section",
            label="IS Section:",
            choices=(
                "ISMB 500", "ISMB 550", "ISMB 600",
                "ISWB 500", "ISWB 550", "ISWB 600",
            ),
            bind="is_section_combo",
            visible_for=("rolled",),
        ),
        ComboField(
            id="torsional_restraint",
            label="Torsional Restraint:",
            choices=tuple(VALUES_TORSIONAL_RESTRAINT),
            bind="torsion_combo",
        ),
        ComboField(
            id="warping_restraint",
            label="Warping Restraint:",
            choices=tuple(VALUES_WARPING_RESTRAINT),
            bind="warping_combo",
        ),
        ComboField(
            id="web_type",
            label="Web Type*:",
            choices=tuple(VALUES_WEB_TYPE),
            bind="web_type_combo",
        ),
    ),
)
