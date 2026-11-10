from collections.abc import Callable

from app.src.models.rule import Rule
from app.src.ui.tabs.rules_tab import RulesTab


class RulesController:
    def __init__(
        self,
        tab: RulesTab,
        get_rules: Callable[[], list[Rule]],
        get_neighborhood_size: Callable[[], int],
        set_rules: Callable[
            [list[Rule], int],
            None,
        ],
    ) -> None:
        self.tab = tab

        self.get_rules = get_rules
        self.get_neighborhood_size = get_neighborhood_size
        self.set_rules = set_rules

    def bind(self) -> None:
        self.tab.bind_apply(self.apply_rules)

    def load(self) -> None:
        self.tab.set_neighborhood_size(self.get_neighborhood_size())

        self.tab.set_rules(self.get_rules())

    def apply_rules(self) -> None:
        try:
            neighborhood_size = self.tab.get_neighborhood_size()

            rules = self.tab.get_rules()

        except ValueError:
            self.tab.set_status("ERROR")
            return

        self.set_rules(
            rules,
            neighborhood_size,
        )

        self.tab.set_status("OK")
