/* Inserts BTC/USDT strategy */

INSERT INTO t_strategies (id, name, pair_name, coin, stable, step, bid, bottom, ceiling, active)
VALUES ('BTC/USDT', 'BTC/USDT 2,5%', 'XBTUSDT', 'XBT', 'USDT', 2.5, 0.0038, 30000, 100000, True)
;