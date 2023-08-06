import pandas as pd
import pdpipe as pdp
import json
from datetime import timedelta
from polygon import RESTClient
from pdsando.ta.pipeline.transforms import ToDateTime, FillMissingTimeFrames
from pdsando.ta.pipeline.filters import RemoveNonMarketHours
from pdsando.ta.datafeeds.tsdata import TimeSeriesData


class Polygon:
    def __init__(self, key=None, debug=False):
        self._key = key
        self._debug = debug
        self._schema = {
            "Volume": {"order": 0, "orig": "v", "type": "float64"},
            "VolumeWeighted": {"order": 1, "orig": "vw", "type": "float64"},
            "Open": {"order": 2, "orig": "o", "type": "float64"},
            "Close": {"order": 3, "orig": "c", "type": "float64"},
            "High": {"order": 4, "orig": "h", "type": "float64"},
            "Low": {"order": 5, "orig": "l", "type": "float64"},
            "EstTimestamp": {"order": 6, "orig": "t", "type": "datetime64"},
            "UnixTimestamp": {"order": 8, "orig": "ux_ts", "type": "int64"},
        }

    def _enforce_schema(self, df):
        for c in df.columns:
            df[c] = df[c].astype(self._schema[c]["type"])

        for c in self._schema:
            if c not in df.columns:
                if self._schema[c]["type"] == "float64":
                    df[c] = 0.0
                elif self._schema[c]["type"] == "int64":
                    df[c] = 0

        return df[
            sorted(list(self._schema.keys()), key=(lambda k: self._schema[k]["order"]))
        ]

    def _get_data(
        self,
        symbol,
        multiplier,
        from_date,
        to_date,
        tz="US/Eastern",
        timespan="minute",
        mode="default",
        cache=None,
    ):
        raw = None
        date_format = "%Y-%m-%d"

        # Support different modes of submitting requests
        if mode == "httplib2":
            import httplib2

            h = httplib2.Http(cache)
            _, content = h.request(
                "https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?limit=50000&sort=asc&apiKey={}".format(
                    symbol,
                    multiplier,
                    timespan,
                    from_date.strftime(date_format),
                    to_date.strftime(date_format),
                    self._key,
                ),
                "GET",
            )
            raw = json.loads(content.decode())["results"]
        elif mode == "urllib":
            import urllib.request

            r = urllib.request.urlopen(
                "https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?limit=50000&sort=asc&apiKey={}".format(
                    symbol,
                    multiplier,
                    timespan,
                    from_date.strftime(date_format),
                    to_date.strftime(date_format),
                    self._key,
                )
            )
            raw = json.loads(r.read().decode("utf-8"))["results"]
        else:
            client = RESTClient(self._key)
            resp = client.stocks_equities_aggregates(
                ticker=symbol.upper(),
                multiplier=multiplier,
                timespan=timespan,
                from_=from_date.strftime(date_format),
                to=to_date.strftime(date_format),
                limit=50000,
            )
            if resp.status not in ("OK", "DELAYED"):
                raise RuntimeError(
                    "Polygon API responded with status {} for date range: {} to {}".format(
                        resp.status,
                        from_date.strftime(date_format),
                        to_date.strftime(date_format),
                    )
                )
            raw = resp.results

            # No valid results
            if not raw:
                return None

        ret_df = pd.DataFrame(raw).fillna(0)

        # Polygon response is inconsistent and stops returning 'n' after 2020-12-01.
        ret_df.drop(columns=["n"], axis=1, errors="ignore", inplace=True)

        ret_df["ux_ts"] = ret_df["t"]
        ret_df = ToDateTime("t", "t", unit="ms", to_tz=tz).apply(ret_df)

        # Rename columns and reindex to align with expectations for mplfinance package.
        ret_df = pdp.ColRename(
            {self._schema[k]["orig"]: k for k in self._schema}
        ).apply(ret_df)

        # Ensure schema
        ret_df = self._enforce_schema(ret_df)

        return ret_df

    def ohlc(
        self,
        symbol,
        multiplier,
        from_date,
        to_date,
        tz="US/Eastern",
        timespan="minute",
        mode="default",
        cache=None,
        only_market_hours=False,
        fill_missing_timeframes=False,
    ):
        # Prepare download batches.
        chunks = []
        if timespan == "minute":
            interval = timedelta(days=34)  # 34.7222 days in 50,000 minutes
            temp_start = to_date - interval
            temp_end = to_date

            # Download chunks until full timespan is received.
            while from_date < temp_start:
                chunks.append((temp_start, temp_end))
                temp_end = temp_start - timedelta(days=1)
                temp_start = temp_end - interval
            chunks.append((from_date, temp_end))
        else:
            # 50,000 days/weeks/etc. exceed the oldest historical data
            chunks.append((from_date, to_date))

        # Debug
        if self._debug:
            for s, e in chunks:
                print("{} to {}".format(s, e))

        # Concatenate all batches/chunks into single DataFrame, ordering by timestamp.
        df = pd.concat(
            [
                self._get_data(
                    symbol.upper(), multiplier, s, e, tz, timespan, mode, cache
                )
                for s, e in chunks
            ]
        ).set_index("EstTimestamp")

        # Optionally remove all data not between 9:30 AM and 4:00 PM EST.
        if only_market_hours:
            df = RemoveNonMarketHours().apply(df)

        # Optionally fill gaps in the data, if any.
        if fill_missing_timeframes and timespan == "minute":
            start = "9:30" if only_market_hours else "0:00"
            end = "16:00" if only_market_hours else "24:00"
            df = FillMissingTimeFrames(
                delta=multiplier, from_time=start, to_time=end
            ).apply(df)

        return TimeSeriesData(
            df, timespan=timespan, multiplier=multiplier, source="polygon"
        )
