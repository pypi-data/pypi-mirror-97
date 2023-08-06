#
# Copyright 2021 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Module for gcp compute engine data generation."""
from datetime import datetime
from random import choice

from nise.generators.gcp.gcp_generator import GCP_REPORT_COLUMNS_JSONL
from nise.generators.gcp.gcp_generator import GCPGenerator


class ComputeEngineGenerator(GCPGenerator):
    """Generator for GCP Compute Engine data."""

    SERVICE = ("Compute Engine", "6F81-5844-456A")  # Service Description and Service ID

    SKU = (  # (ID, Description, Usage Unit, Pricing Unit)
        ("CF4E-A0C7-E3BF", "Instance Core running in Americas", "seconds", "hour"),
        ("D973-5D65-BAB2", "Storage PD Capacity", "byte-seconds", "gibibyte month"),
        ("D0CC-50DF-59D2", "Network Inter Zone Ingress", "bytes", "gibibyte"),
        ("F449-33EC-A5EF", "E2 Instance Ram running in Americas", "byte-seconds", "gibibyte hour"),
        ("CD20-B4CA-0F7C", "Licensing Fee for Debian 10 Buster (RAM cost)", "byte-seconds", "gibiyte hour"),
        ("6B8F-E63D-832B", "Network Internet Egress from Americas to APAC", "bytes", "gibibyte"),
        ("DFA5-B5C6-36D6", "Network Internet Egress from Americas to EMEA", "bytes", "gibibyte"),
        ("9DE9-9092-B3BC", "Network Internet Egress from Americas to China", "bytes", "gibibyte"),
        ("7151-106A-2684", "Network Internet Ingress from APAC to Americas", "bytes", "gibibyte"),
        ("2F99-3A90-373B", "Network Internet Ingress from EMEA to Americas", "bytes", "gibibyte"),
        ("92CB-C25F-B1D1", "Network Google Egress from Americas to Americas", "bytes", "gibibyte"),
        ("227B-5B2B-A75A", "Network Internet Ingress from China to Americas", "bytes", "gibibyte"),
        ("123C-0EFC-B7C8", "Network Google Ingress from Americas to Americas", "bytes", "gibibyte"),
        ("F274-1692-F213", "Network Internet Engress from Americas to Americas", "bytes", "gibibyte"),
        ("92CB-C25F-B1D1", "Network Google Egress from Americas to Americas", "bytes", "gibibyte"),  # Left off at 125
    )

    LABELS = (("[{'key': 'vm_key_proj2', 'value': 'vm_label_proj2'}]"), ("[]"))

    def __init__(self, start_date, end_date, project, attributes=None):
        """Initialize the cloud storage generator."""
        super().__init__(start_date, end_date, project, attributes)
        if self.attributes:
            if self.attributes.get("tags"):
                self._tags = self.attributes.get("tags")
            if self.attributes.get("usage.amount"):
                self._usage_amount = self.attributes.get("usage.amount")
            if self.attributes.get("usage.amount_in_pricing_units"):
                self._pricing_amount = self.attributes.get("usage.amount_in_pricing_units")
            if self.attributes.get("price"):
                self._price = self.attributes.get("price")
            if self.attributes.get("usage.pricing_unit"):
                for sku in self.SKU:
                    if self.attributes.get("usage.pricing_unit") == sku[3]:
                        self._sku = sku
            if self.attributes.get("instance_type"):
                self._instance_type = self.attributes.get("instance_type")

    def _update_data(self, row):  # noqa: C901
        """Update a data row with compute values."""
        sku = choice(self.SKU)
        if self._sku:
            sku = self._sku
        row["system_labels"] = "[]"
        row["service.description"] = self.SERVICE[0]
        row["service.id"] = self.SERVICE[1]
        row["sku.id"] = sku[0]
        row["sku.description"] = sku[1]
        usage_unit = sku[2]
        pricing_unit = sku[3]
        row["usage.unit"] = usage_unit
        row["usage.pricing_unit"] = pricing_unit
        row["labels"] = self.determine_labels(self.LABELS)
        row["credits"] = "[]"
        row["cost_type"] = "regular"
        row["currency"] = "USD"
        row["currency_conversion_rate"] = 1
        row["usage.amount"] = self._gen_usage_unit_amount(usage_unit)
        row["usage.amount_in_pricing_units"] = self._gen_pricing_unit_amount(pricing_unit, row["usage.amount"])
        row["cost"] = self._gen_cost(row["usage.amount_in_pricing_units"])
        usage_date = datetime.strptime(row.get("usage_start_time"), "%Y-%m-%dT%H:%M:%S")
        row["invoice.month"] = f"{usage_date.year}{usage_date.month:02d}"
        row["system_labels"] = self.determine_system_labels(sku[3])
        if self.attributes:
            for key in self.attributes:
                if key in self.column_labels:
                    row[key] = self.attributes[key]
        return row

    def generate_data(self, report_type=None):
        """Generate GCP compute data for some days."""
        return self._generate_hourly_data()


class JSONLComputeEngineGenerator(ComputeEngineGenerator):
    """Generator for GCP Compute Engine data."""

    LABELS = (([{"key": "vm_key_proj2", "value": "vm_label_proj2"}]), ([]))

    def __init__(self, start_date, end_date, project, attributes=None):
        super().__init__(start_date, end_date, project, attributes)
        self.column_labels = GCP_REPORT_COLUMNS_JSONL
        self.return_list = True

    def _update_data(self, row):  # noqa: C901
        """Update a data row with compute values."""
        sku_choice = choice(self.SKU)
        if self._sku:
            sku_choice = self._sku
        service = {}
        service["description"] = self.SERVICE[0]
        service["id"] = self.SERVICE[1]
        row["service"] = service
        sku = {}
        sku["id"] = sku_choice[0]
        sku["description"] = sku_choice[1]
        row["sku"] = sku
        usage_unit = sku_choice[2]
        pricing_unit = sku_choice[3]
        usage = {}
        usage["unit"] = usage_unit
        usage["pricing_unit"] = pricing_unit
        row["labels"] = self.determine_labels(self.LABELS)
        usage["amount"] = self._gen_usage_unit_amount(usage_unit)
        usage["amount_in_pricing_units"] = self._gen_pricing_unit_amount(pricing_unit, usage["amount"])
        row["cost"] = self._gen_cost(usage["amount_in_pricing_units"])
        row["usage"] = usage
        row["credits"] = {}
        row["cost_type"] = "regular"
        row["currency"] = "USD"
        row["currency_conversion_rate"] = 1
        invoice = {}
        year = datetime.strptime(row.get("usage_start_time"), "%Y-%m-%dT%H:%M:%S").year
        month = datetime.strptime(row.get("usage_start_time"), "%Y-%m-%dT%H:%M:%S").month
        invoice["month"] = f"{year}{month:02d}"
        row["invoice"] = invoice
        row["system_labels"] = self.determine_system_labels(sku_choice[3])
        if self.attributes:
            for key in self.attributes:
                if key in self.column_labels:
                    row[key] = self.attributes[key]
                elif key.split(".")[0] in self.column_labels:
                    outer_key, inner_key = key.split(".")
                    row[outer_key][inner_key] = self.attributes[key]
        return row

    def generate_data(self, report_type=None):
        """Generate GCP compute data for some days."""
        return self._generate_hourly_data()
