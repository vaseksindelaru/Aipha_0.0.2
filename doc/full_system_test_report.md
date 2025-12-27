# Reporte de Ejecución Completa del Sistema Aipha
**Fecha de ejecución**: mar 23 dic 2025 01:23:34 CET
Este reporte documenta el flujo completo desde la adquisición de datos hasta la automejora autónoma.
## Capa 2: Data Processor
**Comando**: `python3 data_processor/acquire_data.py`
```text
INFO:__main__:Descargando datos para BTCUSDT 1h...
INFO:data_processor.data_system.fetcher:Procesando plantilla 'BTC_1h_Q1_2024' para BTCUSDT...
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-01
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-01.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-01.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-02
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-02.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-02.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-03
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-03.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-03.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-04
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-04.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-04.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-05
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-05.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-05.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-06
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-06.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-06.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-07
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-07.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-07.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-08
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-08.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-08.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-09
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-09.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-09.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-10
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-10.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-10.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-11
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-11.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-11.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-12
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-12.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-12.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-13
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-13.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-13.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-14
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-14.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-14.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-15
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-15.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-15.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-16
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-16.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-16.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-17
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-17.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-17.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-18
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-18.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-18.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-19
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-19.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-19.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-20
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-20.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-20.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-21
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-21.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-21.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-22
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-22.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-22.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-23
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-23.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-23.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-24
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-24.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-24.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-25
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-25.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-25.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-26
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-26.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-26.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-27
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-27.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-27.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-28
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-28.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-28.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-29
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-29.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-29.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-30
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-30.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-30.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-01-31
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-01-31.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-01-31.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-01
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-01.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-01.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-02
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-02.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-02.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-03
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-03.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-03.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-04
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-04.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-04.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-05
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-05.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-05.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-06
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-06.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-06.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-07
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-07.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-07.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-08
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-08.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-08.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-09
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-09.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-09.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-10
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-10.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-10.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-11
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-11.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-11.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-12
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-12.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-12.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-13
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-13.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-13.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-14
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-14.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-14.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-15
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-15.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-15.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-16
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-16.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-16.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-17
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-17.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-17.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-18
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-18.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-18.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-19
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-19.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-19.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-20
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-20.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-20.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-21
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-21.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-21.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-22
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-22.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-22.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-23
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-23.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-23.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-24
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-24.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-24.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-25
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-25.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-25.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-26
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-26.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-26.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-27
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-27.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-27.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-28
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-28.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-28.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-02-29
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-02-29.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-02-29.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-01
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-01.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-01.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-02
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-02.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-02.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-03
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-03.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-03.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-04
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-04.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-04.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-05
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-05.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-05.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-06
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-06.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-06.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-07
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-07.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-07.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-08
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-08.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-08.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-09
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-09.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-09.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-10
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-10.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-10.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-11
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-11.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-11.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-12
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-12.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-12.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-13
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-13.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-13.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-14
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-14.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-14.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-15
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-15.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-15.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-16
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-16.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-16.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-17
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-17.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-17.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-18
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-18.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-18.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-19
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-19.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-19.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-20
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-20.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-20.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-21
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-21.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-21.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-22
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-22.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-22.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-23
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-23.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-23.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-24
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-24.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-24.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-25
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-25.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-25.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-26
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-26.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-26.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-27
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-27.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-27.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-28
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-28.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-28.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-29
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-29.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-29.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-30
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-30.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-30.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Obteniendo datos de klines para BTCUSDT 1h en 2024-03-31
INFO:data_processor.data_system.fetcher:Usando archivo ZIP local existente: data_processor/data/test_downloaded_data/BTCUSDT/1h/BTCUSDT-1h-2024-03-31.zip
INFO:data_processor.data_system.fetcher:Datos cargados exitosamente desde 'BTCUSDT-1h-2024-03-31.csv' (24 filas)
INFO:data_processor.data_system.fetcher:Concatenando 91 DataFrames diarios...
INFO:data_processor.data_system.fetcher:Proceso completado. Total de filas: 2184
INFO:__main__:Éxito: 2184 filas obtenidas.
INFO:data_processor.data_system.storage:Guardando 2184 filas en la tabla 'btc_1h_data' de DuckDB...
INFO:data_processor.data_system.storage:Datos guardados exitosamente en 'btc_1h_data'.
INFO:__main__:Datos guardados en la tabla 'btc_1h_data'.
```
## Capa 3: Trading Manager
**Comando**: `python3 trading_manager/strategies/proof_strategy.py`
```text
Total Señales: 366
Take Profit (1): 65
Stop Loss (-1): 174
Neutral (0): 127
Win Rate (TP vs Total): 17.76%

INFO: MemoryManager inicializado en memory
INFO: --- INICIANDO PROOF STRATEGY ---
INFO: Datos cargados: 24024 velas de 2024-01-01 00:00:00 a 2024-03-31 23:00:00
INFO: Detectando velas clave...
INFO: Detección completada (REVERSIÓN). Velas clave encontradas: 366
INFO: Se detectaron 366 eventos de señal.
INFO: Etiquetando eventos con Triple Barrier Method (ATR)...
INFO: --- RESULTADOS FINALES ---
```
## Capa 4: Oracle
**Comando**: `python3 oracle/strategies/proof_strategy_v2.py`
```text
Total Señales Filtradas: 127
Take Profit (1): 65
Stop Loss (-1): 0
Neutral (0): 62
Win Rate Filtrado: 51.18%

INFO: MemoryManager inicializado en memory
INFO: --- INICIANDO PROOF STRATEGY V2 (CON ORÁCULO) ---
INFO: Modelo cargado desde oracle/models/oracle_reversal_v1.joblib
INFO: Detección completada (REVERSIÓN). Velas clave encontradas: 366
INFO: Señales originales: 366
INFO: Señales filtradas por el Oráculo: 127
INFO: --- RESULTADOS FINALES (ESTRATEGIA FILTRADA) ---
```
## Capa 1: Autonomous Intelligence
**Comando**: `python3 -m core.orchestrator`
```text
2025-12-23 01:24:16,887 [INFO] core.memory_manager: MemoryManager inicializado en memory
2025-12-23 01:24:16,888 [INFO] core.change_proposer: ChangeProposer inicializado
2025-12-23 01:24:16,888 [INFO] core.change_evaluator: ChangeEvaluator inicializado
2025-12-23 01:24:16,888 [INFO] core.alerts: AlertsSystem inicializado
2025-12-23 01:24:16,888 [INFO] __main__: 🤖 CentralOrchestrator inicializado
2025-12-23 01:24:16,888 [INFO] __main__: ════════════════════════════════════════════════════════════
2025-12-23 01:24:16,889 [INFO] __main__: 🔄 INICIANDO CICLO DE AUTOMEJORA
2025-12-23 01:24:16,889 [INFO] __main__: ════════════════════════════════════════════════════════════
2025-12-23 01:24:16,889 [INFO] __main__: 
[PASO 1] Recolectando métricas...
2025-12-23 01:24:16,889 [INFO] __main__: 
[PASO 2] Generando propuestas de cambio...
2025-12-23 01:24:16,893 [INFO] core.change_proposer: Generated 2 proposals
2025-12-23 01:24:16,893 [INFO] __main__:   → 2 propuestas generadas
2025-12-23 01:24:16,893 [INFO] __main__: 
[PASO 3] Evaluando propuestas...
2025-12-23 01:24:16,893 [INFO] core.change_evaluator: Evaluated AIPHA-8BEFC6: 0.80 → APPROVED
2025-12-23 01:24:16,893 [INFO] __main__:   → AIPHA-8BEFC6: 0.80 → ✅
2025-12-23 01:24:16,894 [INFO] core.change_evaluator: Evaluated AIPHA-605033: 0.80 → APPROVED
2025-12-23 01:24:16,894 [INFO] __main__:   → AIPHA-605033: 0.80 → ✅
2025-12-23 01:24:16,894 [INFO] __main__: 
[PASO 4] Implementando cambios aprobados...
2025-12-23 01:24:16,904 [INFO] core.config_manager: Configuración guardada en memory/aipha_config.json
2025-12-23 01:24:16,905 [INFO] core.memory_manager: [CentralOrchestrator] applied_change_AIPHA-8BEFC6 → success
2025-12-23 01:24:16,905 [INFO] core.alerts: ℹ️  ALERT: [INFO] Cambio Aplicado: Se aplicó el cambio AIPHA-8BEFC6 en Trading.tp_factor
2025-12-23 01:24:16,906 [INFO] core.memory_manager: [AlertsSystem] notification_sent → success
2025-12-23 01:24:16,906 [INFO] __main__:   ✅ Aplicado: AIPHA-8BEFC6
2025-12-23 01:24:16,908 [INFO] core.config_manager: Configuración guardada en memory/aipha_config.json
2025-12-23 01:24:16,908 [INFO] core.memory_manager: [CentralOrchestrator] applied_change_AIPHA-605033 → success
2025-12-23 01:24:16,908 [INFO] core.alerts: ℹ️  ALERT: [INFO] Cambio Aplicado: Se aplicó el cambio AIPHA-605033 en Orchestrator.confidence_threshold
2025-12-23 01:24:16,909 [INFO] core.memory_manager: [AlertsSystem] notification_sent → success
2025-12-23 01:24:16,909 [INFO] __main__:   ✅ Aplicado: AIPHA-605033
2025-12-23 01:24:16,909 [INFO] __main__: 
[PASO 5] Registrando ciclo...
2025-12-23 01:24:16,909 [INFO] core.memory_manager: Sistema state actualizado: ['last_improvement_cycle', 'last_cycle_proposals', 'last_cycle_approved', 'last_cycle_applied', 'last_cycle_duration_seconds']
2025-12-23 01:24:16,910 [INFO] core.memory_manager: [CentralOrchestrator] improvement_cycle_completed → success
2025-12-23 01:24:16,910 [INFO] __main__: 
════════════════════════════════════════════════════════════
2025-12-23 01:24:16,910 [INFO] __main__: 📊 RESUMEN DEL CICLO
2025-12-23 01:24:16,910 [INFO] __main__: ════════════════════════════════════════════════════════════
2025-12-23 01:24:16,910 [INFO] __main__: ⏱️  Duración: 0.0s
2025-12-23 01:24:16,910 [INFO] __main__: 📝 Propuestas generadas: 2
2025-12-23 01:24:16,910 [INFO] __main__: ✅ Propuestas aprobadas: 2
2025-12-23 01:24:16,910 [INFO] __main__: 🔧 Cambios aplicados: 2
2025-12-23 01:24:16,911 [INFO] __main__: ════════════════════════════════════════════════════════════
```
