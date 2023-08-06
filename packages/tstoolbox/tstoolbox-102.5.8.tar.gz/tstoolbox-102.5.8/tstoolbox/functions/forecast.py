from __future__ import absolute_import, division, print_function

import mando
import pandas as pd

from tstoolbox import tsutils

mando.main.add_subprog("forecast", help="Forecast algorithms")


@mando.main.forecast.command("arima")
@tsutils.doc(tsutils.docstrings)
def automatic_cli(
    input_ts="-",
    columns=None,
    start_date=None,
    end_date=None,
    dropna="no",
    clean=False,
    statistic="sum",
    round_index=None,
    skiprows=None,
    index_type="datetime",
    names=None,
    source_units=None,
    target_units=None,
    print_input=False,
    tablefmt="csv",
):
    """Machine learning automatic forecasting

    Machine learning forecast using PyAF (Python Automatic Forecasting)

        Uses a machine learning approach (The signal is cut into estimation
        and validation parts, respectively, 80% and 20% of the signal).  A
    time-series cross-validation can also be used.

        Forecasting a time series model on a given horizon (forecast result
        is also pandas data-frame) and providing prediction/confidence
    intervals for the forecasts.

    Generic training features
        * Signal decomposition as the sum of a trend, periodic and AR
      component
        * Works as a competition between a comprehensive set of possible
          signal transformations and linear decompositions. For each
          transformed signal , a set of possible trends, periodic components
          and AR models is generated and all the possible combinations are
          estimated.  The best decomposition in term of performance is kept
          to forecast the signal (the performance is computed on a part of
          the signal that was not used for the estimation).
        * Signal transformation is supported before signal decompositions.
          Four transformations are supported by default. Other
      transformation are available (Box-Cox etc).
        * All Models are estimated using standard procedures and
          state-of-the-art time series modeling. For example, trend
          regressions and AR/ARX models are estimated using scikit-learn
          linear regression models.
    * Standard performance measures are used (L1, RMSE, MAPE, etc)

    Exogenous Data Support
        * Exogenous data can be provided to improve the forecasts. These are
          expected to be stored in an external data-frame (this data-frame
      will be merged with the training data-frame).
        * Exogenous data are integrated in the modeling process through
      their past values (ARX models).
        * Exogenous variables can be of any type (numeric, string , date, or
      object).
        * Exogenous variables are dummified for the non-numeric types, and
      standardized for the numeric types.

        Hierarchical Forecasting
        * Bottom-Up, Top-Down (using proportions), Middle-Out and Optimal
      Combinations are implemented.
        * The modeling process is customizable and has a huge set of
          options. The default values of these options should however be OK
          to produce a reasonable quality model in a limited amount of time
      (a few minutes).

    Parameters
    ----------
    {input_ts}
    {start_date}
    {end_date}
    {skiprows}
    {names}
    {columns}
    {dropna}
    {clean}
    {source_units}
    {target_units}
    {round_index}
    {index_type}
    {print_input}
    {tablefmt}

    """
    tsutils.printiso(
        automatic(
            input_ts=input_ts,
            columns=columns,
            start_date=start_date,
            end_date=end_date,
            dropna=dropna,
            clean=clean,
            statistic=statistic,
            round_index=round_index,
            skiprows=skiprows,
            index_type=index_type,
            names=names,
            source_units=source_units,
            target_units=target_units,
            print_input=print_input,
        ),
        tablefmt="csv",
    )


def automatic(
    input_tsd=None,
    start_date=None,
    end_date=None,
    pick=None,
    force_freq=None,
    groupby=None,
    dropna="no",
    round_index=None,
    clean=False,
    target_units=None,
    source_units=None,
    bestfreq=True,
    parse_dates=True,
    extended_columns=False,
    skiprows=None,
    index_type="datetime",
    names=None,
):
    tsd = tsutils.common_kwds(
        tsutils.read_iso_ts(
            input_ts, skiprows=skiprows, names=names, index_type=index_type
        ),
        start_date=start_date,
        end_date=end_date,
        pick=columns,
        round_index=round_index,
        dropna=dropna,
        source_units=source_units,
        target_units=target_units,
        clean=clean,
    )
    ntsd = pd.DataFrame()
