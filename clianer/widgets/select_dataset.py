import urwid

from clianer.widgets.dialog import Dialog
from clianer.widgets.button import CustomButton

from opuscleaner.config import DATA_PATH
from opuscleaner.datasets import list_datasets
from opuscleaner.server import api_get_dataset_filters
from opuscleaner.categories import get_mapping

class SelectDatasetDialog(Dialog):

    def __init__(self):
        # datasets: Dict[str, List[Tuple[str, Path]]]
        self.datasets = list_datasets(DATA_PATH)
        category_mapping = get_mapping()

        have_mapping = []
        for cat in category_mapping.categories:
            if cat.name in category_mapping.mapping:
                have_mapping.extend(category_mapping.mapping[cat.name])

        have_mapping = set(have_mapping)

        self.dataset_widgets = []
        for dataset_name in self.datasets:
            langs = ", ".join(
                sorted(lang for lang, _ in self.datasets[dataset_name]))

            label = f"{dataset_name} ({langs})"

            pipeline = api_get_dataset_filters(dataset_name)
            if pipeline.filters:
                label += f" [{len(pipeline.filters)}]"

            if dataset_name in have_mapping:
                label = f"* {label}"

            button = CustomButton(
                label, on_press=self.select_dataset, user_data=dataset_name)

            self.dataset_widgets.append(button)

        self.listbox = urwid.ListBox(
            urwid.SimpleFocusListWalker(self.dataset_widgets))

        urwid.register_signal(self.__class__, ["close"])
        super().__init__(self.listbox, "Select dataset", width=70, height=30)

    def select_dataset(self, button, dataset):
        self._emit("close", dataset)
