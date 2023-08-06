
from .base.greetings import GreetingsCommand
from .base.goodbye import GoodbyeCommand
from .base.generate_code import GenerateScriptCommand
from .base.predict import PredictCommand
from .base.suggest import SuggestCommand
from .base.cancel_action import CancelCommand

from .context.load_dataset import LoadDatasetCommand

from .visualization.histogram import HistogramCommand
from .visualization.plot_bar import BarsPlotCommand
from .visualization.plot_scatter import ScatterPlotCommand

from .preprocess.extract_column import ColumnExtractCommand
from .preprocess.remove_column import ColumnRemoveCommand
from .preprocess.empty_cell import CellEmptyCommand
from .preprocess.white_spaces import WhiteSpacesCommand
from .preprocess.lower_upper_case import LowerUpperCommand
from .preprocess.normalize_column import NormalizeColumnCommand
from .preprocess.drop_duplicates import DropDuplicateCommand
from .preprocess.sort_column import SortColumnCommand

from .metrics.accuracy import AccuracyCommand

from .algoritms.algorithm import AlgorithmCommand
from .algoritms.statistical_correlation import StatisticalCorrelationCommand

from .pipeline.outliers import OutliersPipeCommand
from .pipeline.tpot_outliers import TPOTOutliersPipeCommand


commands = {
    GreetingsCommand.tag: GreetingsCommand,
    GoodbyeCommand.tag: GoodbyeCommand,
    GenerateScriptCommand.tag: GenerateScriptCommand,
    PredictCommand.tag: PredictCommand,
    SuggestCommand.tag: SuggestCommand,
    CancelCommand.tag: CancelCommand,

    LoadDatasetCommand.tag: LoadDatasetCommand,

    HistogramCommand.tag: HistogramCommand,
    BarsPlotCommand.tag: BarsPlotCommand,
    ScatterPlotCommand.tag: ScatterPlotCommand,

    ColumnExtractCommand.tag: ColumnExtractCommand,
    ColumnRemoveCommand.tag: ColumnRemoveCommand,
    CellEmptyCommand.tag: CellEmptyCommand,
    WhiteSpacesCommand.tag: WhiteSpacesCommand,
    LowerUpperCommand.tag: LowerUpperCommand,
    NormalizeColumnCommand.tag: NormalizeColumnCommand,
    DropDuplicateCommand.tag: DropDuplicateCommand,
    SortColumnCommand.tag: SortColumnCommand,

    AccuracyCommand.tag: AccuracyCommand,

    AlgorithmCommand.tag: AlgorithmCommand,
    StatisticalCorrelationCommand.tag: StatisticalCorrelationCommand,

    # TimeSeriesForestClassifierAlgorithmCommand.tag: TimeSeriesForestClassifierAlgorithmCommand,

    # OutliersPipeCommand.tag: OutliersPipeCommand
    TPOTOutliersPipeCommand.tag: TPOTOutliersPipeCommand,
    # TPOTSKTimePipeCommand.tag: TPOTSKTimePipeCommand
}

