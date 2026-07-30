import unittest

from quant_toolkit.registry import FactorRegistry, FactorSpec


class FactorRegistryTest(unittest.TestCase):
    def test_registers_factor_metadata(self) -> None:
        registry = FactorRegistry()
        spec = FactorSpec(
            factor_id="demo_alpha",
            family="price_volume",
            description="Demo factor.",
            input_fields=("close",),
            point_in_time_rule="formed after close",
        )
        registry.register(spec)
        self.assertEqual(registry.get("demo_alpha").family, "price_volume")

    def test_rejects_duplicate_factor_id(self) -> None:
        registry = FactorRegistry()
        spec = FactorSpec(
            factor_id="demo_alpha",
            family="price_volume",
            description="Demo factor.",
            input_fields=("close",),
            point_in_time_rule="formed after close",
        )
        registry.register(spec)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            registry.register(spec)

    def test_requires_point_in_time_rule(self) -> None:
        registry = FactorRegistry()
        with self.assertRaisesRegex(ValueError, "point_in_time_rule"):
            registry.register(
                FactorSpec(
                    factor_id="bad_alpha",
                    family="price_volume",
                    description="Missing timing metadata.",
                    input_fields=("close",),
                    point_in_time_rule="",
                )
            )


if __name__ == "__main__":
    unittest.main()
