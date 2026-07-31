from __future__ import annotations

import unittest

from quant_toolkit.demo import make_synthetic_panel
from quant_toolkit.manifest import DataManifest


class DataManifestTest(unittest.TestCase):
    def test_manifest_records_panel_shape_and_limits(self) -> None:
        panel = make_synthetic_panel(days=3, assets=2)
        manifest = DataManifest.from_panel(panel, source="synthetic-public-demo", known_limits=["not production data"])

        payload = manifest.to_dict()

        self.assertEqual(payload["rows"], 6)
        self.assertIn("momentum_5d", payload["columns"])
        self.assertEqual(payload["known_limits"], ["not production data"])

    def test_requires_identity_columns(self) -> None:
        panel = make_synthetic_panel(days=2, assets=2).drop(columns=["asset"])

        with self.assertRaises(ValueError):
            DataManifest.from_panel(panel, source="broken")


if __name__ == "__main__":
    unittest.main()
