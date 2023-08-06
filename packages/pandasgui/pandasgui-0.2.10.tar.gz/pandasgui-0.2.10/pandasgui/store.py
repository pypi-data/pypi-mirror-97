import textwrap
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Union, Iterable
import pandas as pd
from pandas import DataFrame
from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyQt5.QtCore import Qt
import traceback
from functools import wraps
from datetime import datetime
from pandasgui.utility import unique_name, in_interactive_console, rename_duplicates, refactor_variable, parse_dates, \
    clean_dataframe
from pandasgui.constants import LOCAL_DATA_DIR, DEFAULT_TITLE_FORMAT, RENDER_MODE
import os
import collections
from enum import Enum
import json
import inspect
import logging

logger = logging.getLogger(__name__)

# JSON file that stores persistent user preferences
preferences_path = os.path.join(LOCAL_DATA_DIR, 'preferences.json')
if not os.path.exists(preferences_path):
    with open(preferences_path, 'w') as f:
        json.dump({'theme': "light"}, f)


def read_saved_settings():
    if not os.path.exists(preferences_path):
        return {}
    else:
        with open(preferences_path, 'r') as f:
            saved_settings = json.load(f)
        return saved_settings


def write_saved_settings(settings):
    with open(preferences_path, 'w') as f:
        json.dump(settings, f)


class DictLike:
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


class Setting(DictLike):
    def __init__(self, label, value, description, dtype, persist):
        self.label: str = label
        self.value: any = value
        self.description: str = description
        self.dtype: Union[type(str), type(bool), Enum] = dtype
        self.persist: bool = persist

    def __setattr__(self, key, value):
        try:
            if self.persist:
                settings = read_saved_settings()
                settings[self.label] = value
                write_saved_settings(settings)
        except AttributeError:
            # Get attribute error because of __setattr__ happening in __init__ before self.persist is set
            pass

        super().__setattr__(key, value)


DEFAULT_SETTINGS = {'editable': False,
                    'style': "Fusion",
                    'block': True,
                    'theme': 'Dark',
                    'title_format': DEFAULT_TITLE_FORMAT,
                    'render_mode': RENDER_MODE,
                    'apply_mean': True,
                    'apply_sort': True}


@dataclass
class SettingsStore(DictLike):
    block: Setting
    editable: Setting
    style: Setting
    theme: Setting
    title_format: Setting
    render_mode: Setting
    apply_mean: Setting
    apply_sort: Setting

    def __init__(self, **settings):

        saved_settings = read_saved_settings()

        for setting_name in DEFAULT_SETTINGS.keys():
            # Fill settings values if not provided
            if setting_name not in settings.keys():
                if setting_name in saved_settings.keys():
                    settings[setting_name] = saved_settings[setting_name]
                else:
                    settings[setting_name] = DEFAULT_SETTINGS[setting_name]

        if in_interactive_console():
            # Don't block if in an interactive console (so you can view GUI and still continue running commands)
            settings['block'] = False
        else:
            # If in a script, block or else the script will continue and finish without allowing GUI interaction
            settings['block'] = True

        self.block = Setting(label="block",
                             value=settings['block'],
                             description="Should GUI block code execution until closed?",
                             dtype=bool,
                             persist=False)

        self.editable = Setting(label="editable",
                                value=settings['editable'],
                                description="Are table cells editable?",
                                dtype=bool,
                                persist=True)

        self.style = Setting(label="style",
                             value=settings['style'],
                             description="PyQt app style",
                             dtype=Enum("StylesEnum", QtWidgets.QStyleFactory.keys()),
                             persist=True)

        self.theme = Setting(label="theme",
                             value=settings['theme'],
                             description="UI theme",
                             dtype=Enum("ThemesEnum", ['light', 'dark', 'classic']),
                             persist=True)

        self.title_format = Setting(label="title_format",
                                    value=settings['title_format'],
                                    description="format string for automatically generated chart title",
                                    dtype=str,
                                    persist=True)

        self.render_mode = Setting(label="render_mode",
                                   value=settings['render_mode'],
                                   description="render mode for plotly express charts",
                                   dtype=Enum("RenderEnum", ['auto', 'webgl', 'svg']),
                                   persist=True)

        self.apply_mean = Setting(label="apply_mean",
                                  value=settings['apply_mean'],
                                  description="Default flag for whether to aggregate automatically in Grapher",
                                  dtype=bool,
                                  persist=True)

        self.apply_sort = Setting(label="apply_sort",
                                  value=settings['apply_sort'],
                                  description="Default flag for whether to sort automatically in Grapher",
                                  dtype=bool,
                                  persist=True)


@dataclass
class Filter:
    expr: str
    enabled: bool
    failed: bool


@dataclass
class HistoryItem:
    comment: str
    code: str
    time: str

    def __init__(self, comment, code):
        self.comment = comment
        self.code = code
        self.time = datetime.now().strftime("%H:%M:%S")


class PandasGuiDataFrameStore:
    """
    All methods that modify the data should modify self.df_unfiltered, then self.df gets computed from that
    """

    def __init__(self, df: DataFrame, name: str = 'Untitled'):
        super().__init__()
        df = df.copy()

        self.df: DataFrame = df
        self.df_unfiltered: DataFrame = df
        self.name = name

        self.history: List[HistoryItem] = []
        self.history_imports = {"import pandas as pd"}

        # References to other object instances that may be assigned later
        self.settings: SettingsStore = SETTINGS_STORE
        self.store: Union[PandasGuiStore, None] = None
        self.gui: Union["PandasGui", None] = None
        self.dataframe_explorer: Union["DataFrameExplorer", None] = None
        self.dataframe_viewer: Union["DataFrameViewer", None] = None
        self.filter_viewer: Union["FilterViewer", None] = None

        self.column_sorted: Union[int, None] = None
        self.index_sorted: Union[int, None] = None
        self.sort_is_ascending: Union[bool, None] = None

        self.filters: List[Filter] = []
        self.filtered_index_map = df.reset_index().index

    ###################################
    # Code history

    def code_export(self):

        if len(self.history) == 0:
            return f"# No actions have been recorded yet on this DataFrame ({self.name})"

        code_history = "# 'df' refers to the DataFrame passed into 'pandasgui.show'\n\n"

        # Add imports to setup
        code_history += '\n'.join(self.history_imports) + '\n\n'

        for history_item in self.history:
            code_history += f'# {history_item.comment}\n'
            code_history += history_item.code
            code_history += "\n\n"

        if any([filt.enabled for filt in self.filters]):
            code_history += f"# Filters\n"
        for filt in self.filters:
            if filt.enabled:
                code_history += f"df = df.query('{filt.expr}')\n"

        return code_history

    def add_history_item(self, comment, code):
        history_item = HistoryItem(comment, code)
        self.history.append(history_item)

    ###################################
    # Editing cell data

    def edit_data(self, row, col, value):
        # Map the row number in the filtered df (which the user interacts with) to the unfiltered one
        row = self.filtered_index_map[row]

        self.df_unfiltered.iat[row, col] = value
        self.apply_filters()

        self.add_history_item("edit_data",
                              f"df.iat[{row}, {col}] = {value}")

    def paste_data(self, top_row, left_col, df_to_paste):
        new_df = self.df_unfiltered.copy()

        # Not using iat here because it won't work with MultiIndex
        for i in range(df_to_paste.shape[0]):
            for j in range(df_to_paste.shape[1]):
                value = df_to_paste.iloc[i, j]
                new_df.at[self.df.index[top_row + i],
                          self.df.columns[left_col + j]] = value

        self.df_unfiltered = new_df
        self.apply_filters()

        self.add_history_item("paste_data", inspect.cleandoc(
            f"""
            df_to_paste = pd.DataFrame({df_to_paste.to_dict(orient='list')})
            for i in range(df_to_paste.shape[0]):
                for j in range(df_to_paste.shape[1]):
                    value = df_to_paste.iloc[i, j]
                    df.at[df.index[{top_row} + i],
                          df.columns[{left_col} + j]] = value
            """))

    ###################################
    # Sorting

    def sort_column(self, ix: int):
        col_name = self.df_unfiltered.columns[ix]

        # Clicked an unsorted column
        if ix != self.column_sorted:
            self.df_unfiltered = self.df_unfiltered.sort_values(col_name, ascending=True, kind='mergesort')
            self.column_sorted = ix
            self.sort_is_ascending = True

            self.add_history_item("sort_column",
                                  f"df = df.sort_values(df.columns[{ix}], ascending=True, kind='mergesort')")

        # Clicked a sorted column
        elif ix == self.column_sorted and self.sort_is_ascending:
            self.df_unfiltered = self.df_unfiltered.sort_values(col_name, ascending=False, kind='mergesort')
            self.column_sorted = ix
            self.sort_is_ascending = False

            self.add_history_item("sort_column",
                                  f"df = df.sort_values(df.columns[{ix}], ascending=False, kind='mergesort')")

        # Clicked a reverse sorted column - reset to sorted by index
        elif ix == self.column_sorted:
            self.df_unfiltered = self.df_unfiltered.sort_index(ascending=True, kind='mergesort')
            self.column_sorted = None
            self.sort_is_ascending = None

            self.add_history_item("sort_column",
                                  "df = df.sort_index(ascending=True, kind='mergesort')")

        self.index_sorted = None
        self.apply_filters()

    def sort_index(self, ix: int):
        # Clicked an unsorted index level
        if ix != self.index_sorted:
            self.df_unfiltered = self.df_unfiltered.sort_index(level=ix, ascending=True, kind='mergesort')
            self.index_sorted = ix
            self.sort_is_ascending = True

            self.add_history_item("sort_index",
                                  f"df = df.sort_index(level={ix}, ascending=True, kind='mergesort')")

        # Clicked a sorted index level
        elif ix == self.index_sorted and self.sort_is_ascending:
            self.df_unfiltered = self.df_unfiltered.sort_index(level=ix, ascending=False, kind='mergesort')
            self.index_sorted = ix
            self.sort_is_ascending = False

            self.add_history_item("sort_index",
                                  f"df = df.sort_index(level={ix}, ascending=False, kind='mergesort')")

        # Clicked a reverse sorted index level - reset to sorted by full index
        elif ix == self.index_sorted:
            self.df_unfiltered = self.df_unfiltered.sort_index(ascending=True, kind='mergesort')

            self.index_sorted = None
            self.sort_is_ascending = None

            self.add_history_item("sort_index",
                                  "df = df.sort_index(ascending=True, kind='mergesort')")

        self.column_sorted = None
        self.apply_filters()

    ###################################
    # Filters

    def any_filtered(self):
        return any(filt.enabled for filt in self.filters)

    def add_filter(self, expr: str, enabled=True):
        filt = Filter(expr=expr, enabled=enabled, failed=False)
        self.filters.append(filt)
        self.apply_filters()

    def remove_filter(self, index: int):
        self.filters.pop(index)
        self.apply_filters()

    def edit_filter(self, index: int, expr: str):
        filt = self.filters[index]
        filt.expr = expr
        filt.failed = False
        self.apply_filters()

    def toggle_filter(self, index: int):
        self.filters[index].enabled = not self.filters[index].enabled
        self.apply_filters()

    def apply_filters(self):
        df = self.df_unfiltered.copy()
        df['_temp_range_index'] = df.reset_index().index

        for ix, filt in enumerate(self.filters):
            if filt.enabled and not filt.failed:
                try:
                    df = df.query(filt.expr)
                except Exception as e:
                    self.filters[ix].failed = True
                    logger.exception(e)

        self.filtered_index_map = df['_temp_range_index'].reset_index(drop=True)
        df = df.drop('_temp_range_index', axis=1)

        self.df = df
        self.update()

    ###################################
    # Other

    # Refresh PyQt models when the underlying pgdf is changed in anyway that needs to be reflected in the GUI
    def update(self):

        # Update models
        self.models = []
        if self.dataframe_viewer is not None:
            self.models += [self.dataframe_viewer.dataView.model(),
                            self.dataframe_viewer.columnHeader.model(),
                            self.dataframe_viewer.indexHeader.model(),
                            self.dataframe_viewer.columnHeaderNames.model(),
                            self.dataframe_viewer.indexHeaderNames.model(),
                            ]

        if self.filter_viewer is not None:
            self.models += [self.filter_viewer.list_model,
                            ]

        for model in self.models:
            model.beginResetModel()
            model.endResetModel()

        if self.dataframe_viewer is not None:
            # Update multi-index spans
            for view in [self.dataframe_viewer.columnHeader,
                         self.dataframe_viewer.indexHeader]:
                view.set_spans()

            # Update sizing
            for view in [self.dataframe_viewer.columnHeader,
                         self.dataframe_viewer.indexHeader,
                         self.dataframe_viewer.dataView]:
                view.updateGeometry()

    @staticmethod
    def cast(x: Union["PandasGuiDataFrameStore", pd.DataFrame, pd.Series, Iterable]):
        if isinstance(x, PandasGuiDataFrameStore):
            return x
        if isinstance(x, pd.DataFrame):
            return PandasGuiDataFrameStore(x.copy())
        elif isinstance(x, pd.Series):
            return PandasGuiDataFrameStore(x.to_frame())
        else:
            try:
                return PandasGuiDataFrameStore(pd.DataFrame(x))
            except:
                raise TypeError(f"Could not convert {type(x)} to DataFrame")


@dataclass
class PandasGuiStore:
    settings: Union["SettingsStore", None] = None
    data: Dict[str, PandasGuiDataFrameStore] = field(default_factory=dict)
    gui: Union["PandasGui", None] = None
    navigator: Union["Navigator", None] = None
    selected_pgdf: Union[PandasGuiDataFrameStore, None] = None

    def __post_init__(self):
        self.settings = SETTINGS_STORE

    ###################################
    # IPython magic

    def eval_magic(self, line):

        names_to_update = []
        command = line
        for name in self.data.keys():
            names_to_update.append(name)
            command = refactor_variable(command, name, f"self.data['{name}'].df_unfiltered")

        # print(command)
        exec(command)

        for name in names_to_update:
            self.data[name].apply_filters()
        # self.data[0].df_unfiltered = self.data[0].df_unfiltered[self.data[0].df_unfiltered.HP > 50]
        return line

    ###################################

    def add_dataframe(self, pgdf: Union[DataFrame, PandasGuiDataFrameStore],
                      name: str = "Untitled"):

        name = unique_name(name, self.get_dataframes().keys())
        pgdf = PandasGuiDataFrameStore.cast(pgdf)
        pgdf.settings = self.settings
        pgdf.name = name
        pgdf.store = self

        pgdf.df = clean_dataframe(pgdf.df, name)

        # Add it to store and create widgets
        self.data[name] = pgdf
        if pgdf.dataframe_explorer is None:
            from pandasgui.widgets.dataframe_explorer import DataFrameExplorer
            pgdf.dataframe_explorer = DataFrameExplorer(pgdf)
        dfe = pgdf.dataframe_explorer
        self.gui.stacked_widget.addWidget(dfe)

        # Add to nav
        shape = pgdf.df.shape
        shape = str(shape[0]) + " X " + str(shape[1])

        item = QtWidgets.QTreeWidgetItem(self.navigator, [name, shape])
        self.navigator.itemSelectionChanged.emit()
        self.navigator.setCurrentItem(item)
        self.navigator.apply_tree_settings()

    def remove_dataframe(self, name):
        self.data.pop(name)
        self.gui.navigator.remove_item(name)

    def import_file(self, path):
        if not os.path.isfile(path):
            logger.warning("Path is not a file: " + path)
        elif path.endswith(".csv"):
            filename = os.path.split(path)[1].split('.csv')[0]
            df = pd.read_csv(path, engine='python')
            self.add_dataframe(df, filename)
        elif path.endswith(".xlsx"):
            filename = os.path.split(path)[1].split('.csv')[0]
            df_dict = pd.read_excel(path, sheet_name=None)
            for sheet_name in df_dict.keys():
                df_name = f"{filename} - {sheet_name}"
                self.add_dataframe(df_dict[sheet_name], df_name)
        elif path.endswith(".parquet"):
            filename = os.path.split(path)[1].split('.parquet')[0]
            df = pd.read_parquet(path, engine='pyarrow')
            self.add_dataframe(df, filename)

        else:
            logger.warning("Can only import csv / xlsx / parquet. Invalid file: " + path)

    def get_pgdf(self, name):
        return self.data[name]

    def get_dataframes(self, names: Union[None, str, list] = None):
        if type(names) == str:
            return self.data[names].df

        df_dict = {}
        for pgdf in self.data.values():
            if names is None or pgdf.name in names:
                df_dict[pgdf.name] = pgdf.df

        return df_dict

    def select_pgdf(self, name):
        pgdf = self.get_pgdf(name)
        dfe = pgdf.dataframe_explorer
        self.gui.stacked_widget.setCurrentWidget(dfe)
        self.selected_pgdf = pgdf

    def to_dict(self):
        import json
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


SETTINGS_STORE = SettingsStore()
