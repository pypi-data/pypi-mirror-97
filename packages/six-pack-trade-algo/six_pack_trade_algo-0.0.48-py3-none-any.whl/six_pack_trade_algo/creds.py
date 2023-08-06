import alpaca_trade_api as tradeapi
# Create the api object
api_live = tradeapi.REST(
    key_id='AKKX4ZN1KOXH2ITZ3S3K',
    secret_key='f1Ejw7unlZltOChVKIWy5zWtusW7WPvgb4ILpq8M',
    base_url="https://api.alpaca.markets"
)
# Create the api object
api_paper = tradeapi.REST(
    key_id='PKZHFYO8P351N0WKHMZ6',
    secret_key='2l2bJDxWxSDejWdrrTOBiDlOaKeBrVXExHKKP1tj',
    base_url="https://paper-api.alpaca.markets"
)
poly = api_paper.polygon


