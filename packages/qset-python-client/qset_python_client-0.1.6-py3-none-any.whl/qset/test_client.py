from qset import Client


def test(api_key):
    cli = Client(api_key=api_key, api_url="http://localhost:8000/v0")
    print(cli.get_dataset_overview("binance_timebars_1800"))
    print(
        cli.get_asset_dataset_range("binance_timebars_1800"),
    )
    print(
        cli.get_asset_dataset_range("binance_timebars_1800", tickers=["COMP-USDT"]),
    )

    print(
        cli.get_dataset(
            dataset="binance_timebars_1800",
            query={
                "start": "2021.01.01 00:00:00",
                "end": "2021.01.02 00:00:00",
                "columns": ["startRange", "pVWAP", "ticker"],
                "tickers": ["BTC-USDT", "COMP-USDT"],
            },
        ).tail()
    )


if __name__ == "__main__":
    # todo: del
    test("debug.api-key")
