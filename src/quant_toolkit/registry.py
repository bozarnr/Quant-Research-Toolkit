from __future__ import annotations

from dataclasses import dataclass, field


VALID_STATUSES = {
    "research_seed",
    "registered",
    "computed",
    "diagnosed",
    "validated_candidate",
    "portfolio_candidate",
}


@dataclass(frozen=True)
class FactorSpec:
    factor_id: str
    family: str
    description: str
    input_fields: tuple[str, ...]
    point_in_time_rule: str
    status: str = "research_seed"

    def validate(self) -> None:
        if not self.factor_id or not self.factor_id.replace("_", "").replace("-", "").isalnum():
            raise ValueError("factor_id must be a non-empty slug")
        if not self.family:
            raise ValueError("family is required")
        if not self.input_fields:
            raise ValueError("input_fields cannot be empty")
        if not self.point_in_time_rule:
            raise ValueError("point_in_time_rule is required")
        if self.status not in VALID_STATUSES:
            raise ValueError(f"unknown factor status: {self.status}")


@dataclass
class FactorRegistry:
    _items: dict[str, FactorSpec] = field(default_factory=dict)

    def register(self, spec: FactorSpec) -> None:
        spec.validate()
        if spec.factor_id in self._items:
            raise ValueError(f"duplicate factor_id: {spec.factor_id}")
        self._items[spec.factor_id] = spec

    def get(self, factor_id: str) -> FactorSpec:
        return self._items[factor_id]

    def by_family(self, family: str) -> list[FactorSpec]:
        return [spec for spec in self._items.values() if spec.family == family]

    def as_rows(self) -> list[dict[str, str]]:
        return [
            {
                "factor_id": spec.factor_id,
                "family": spec.family,
                "description": spec.description,
                "input_fields": "|".join(spec.input_fields),
                "point_in_time_rule": spec.point_in_time_rule,
                "status": spec.status,
            }
            for spec in sorted(self._items.values(), key=lambda item: item.factor_id)
        ]
