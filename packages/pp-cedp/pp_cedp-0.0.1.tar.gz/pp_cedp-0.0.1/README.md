## Introduction
This project implements "Privacy-Preserving Continuous Event Data Publishing". 
## Python package
The implementation has been published as a standard Python package. Use the following command to install the corresponding Python package:

```shell
pip install pp-cedp
```

## Usage
```python
from pp_cedp.CEDP import CEDP
from datetime import datetime

if __name__ == '__main__':
    log_name1 = "./event_logs/EL1_minutes_4_5_1_sequence.xes"
    log_name2 = "./event_logs/EL2_minutes_4_5_1_sequence.xes"

    event_attributes = ['concept:name']
    sensitive = ['Diagnose']
    life_cycle = ['complete', '', 'COMPLETE']
    all_life_cycle = True #True will ignore the transitions specified in life_cycle
    time_accuracy = "original" # original, seconds, minutes, hours, days
    bk_length = 3
    n = 1
    results_dir = "./Results"
    result_log_name = "test_"
    multiprocess = True
    cedp = CEDP()
    while n <= bk_length:
        start = datetime.now()
        cedp.calc_FCB_anonymity(log_name1, log_name2, event_attributes, life_cycle, all_life_cycle, sensitive, time_accuracy, n, bk_length,
                            result_log_name, results_dir = results_dir, from_time_days =0, to_time_days = 0, multiprocess = multiprocess)
        print(datetime.now()-start)
        n += 1

```