"""Railing sub-tab for Typical Section Details (schema-driven)."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QComboBox, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator

from osdagbridge.core.bridge_types.plate_girder.ui_fields_additional_input import RAILING_TAB_SCHEMA


class RailingTab(QWidget):
    """Constructs the Railing tab UI and binds fields to the owner."""

    def __init__(self, owner):
        super().__init__(owner)
        self.owner = owner
        self.setStyleSheet("background-color: white;")
        self._build_ui()

    def _create_field(self, field_def, field_width=200):
        owner = self.owner
        ftype = field_def.type

        if ftype == "combo":
            field = QComboBox()
            field.addItems(field_def.choices or ())
        else:
            field = QLineEdit()
            validator_def = field_def.validator
            if validator_def:
                if validator_def.type == "double_range":
                    field.setValidator(QDoubleValidator(validator_def.bottom, validator_def.top, validator_def.decimals))
            default = field_def.default
            if default is not None:
                field.setText(str(default))
            placeholder = field_def.placeholder
            if placeholder:
                field.setPlaceholderText(placeholder)
            if not field_def.enabled:
                field.setEnabled(False)

        field.setObjectName(field_def.id)
        field.setFixedWidth(field_width)
        owner.style_input_field(field)

        bind_name = field_def.bind
        if bind_name:
            setattr(owner, bind_name, field)

        on_change = getattr(field_def, "on_change", None)
        if on_change and hasattr(owner, on_change) and ftype == "combo":
            field.currentTextChanged.connect(getattr(owner, on_change))

        on_text_changed = getattr(field_def, "on_text_changed", None)
        if on_text_changed and hasattr(owner, on_text_changed) and ftype != "combo":
            field.textChanged.connect(getattr(owner, on_text_changed))

        on_editing_finished = getattr(field_def, "on_editing_finished", None)
        if on_editing_finished and hasattr(owner, on_editing_finished) and ftype != "combo":
            field.editingFinished.connect(getattr(owner, on_editing_finished))

        return field

    def _build_ui(self):
        owner = self.owner

        railing_layout = QVBoxLayout(self)
        railing_layout.setContentsMargins(18, 6, 18, 12)
        railing_layout.setSpacing(0)

        card, card_layout = owner._create_section_card("Railing Inputs:")
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        label_width = RAILING_TAB_SCHEMA.label_width

        row_idx = 0
        for row in RAILING_TAB_SCHEMA.rows:
            col = 0
            for field_def in row.fields:
                label = QLabel(field_def.label)
                label.setStyleSheet("font-size: 11px; color: #000;")
                label.setMinimumWidth(label_width)
                grid.addWidget(label, row_idx, col, Qt.AlignLeft)
                col += 1

                field = self._create_field(field_def, field_width=200)
                grid.addWidget(field, row_idx, col)
                col += 1
            row_idx += 1

        card_layout.addLayout(grid)
        railing_layout.addWidget(card)
        railing_layout.addStretch()
