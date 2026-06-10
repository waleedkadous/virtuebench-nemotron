# Standard VirtueBench Analysis Report

Verbatim output of the upstream analyzer run on the detailed per-scenario logs:

```
virtue-bench analyze results/nemotron_10run_sweep_logs.json
```

(The chi-squared test requires per-scenario `sample_details`, so it must be run against the
`_logs.json` file, not the summary. Gunzip `results/nemotron_10run_sweep_logs.json.gz` first.)

| Model                                     | Virtue     | Variant   |   Runs |   Mean Acc | 95% CI           |    Std |
|-------------------------------------------|------------|-----------|--------|------------|------------------|--------|
| openai/blackboxai/nvidia/nemotron-3-ultra | prudence   | ratio     |      9 |     0.8956 | [0.8837, 0.9059] | 0.0186 |
| openai/blackboxai/nvidia/nemotron-3-ultra | prudence   | caro      |     10 |     0.8993 | [0.8873, 0.9107] | 0.0197 |
| openai/blackboxai/nvidia/nemotron-3-ultra | prudence   | mundus    |     10 |     0.73   | [0.7173, 0.7420] | 0.0211 |
| openai/blackboxai/nvidia/nemotron-3-ultra | prudence   | diabolus  |     10 |     0.8707 | [0.8567, 0.8833] | 0.0227 |
| openai/blackboxai/nvidia/nemotron-3-ultra | prudence   | ignatian  |     10 |     0.8793 | [0.8667, 0.8907] | 0.0205 |
| openai/blackboxai/nvidia/nemotron-3-ultra | justice    | ratio     |     10 |     0.8387 | [0.8287, 0.8480] | 0.0166 |
| openai/blackboxai/nvidia/nemotron-3-ultra | justice    | caro      |     10 |     0.818  | [0.8067, 0.8273] | 0.0172 |
| openai/blackboxai/nvidia/nemotron-3-ultra | justice    | mundus    |     10 |     0.6707 | [0.6613, 0.6813] | 0.017  |
| openai/blackboxai/nvidia/nemotron-3-ultra | justice    | diabolus  |     10 |     0.9173 | [0.9100, 0.9253] | 0.0134 |
| openai/blackboxai/nvidia/nemotron-3-ultra | justice    | ignatian  |     10 |     0.9007 | [0.8873, 0.9140] | 0.0225 |
| openai/blackboxai/nvidia/nemotron-3-ultra | courage    | ratio     |     10 |     0.6253 | [0.6127, 0.6393] | 0.0224 |
| openai/blackboxai/nvidia/nemotron-3-ultra | courage    | caro      |     10 |     0.5907 | [0.5787, 0.6033] | 0.0211 |
| openai/blackboxai/nvidia/nemotron-3-ultra | courage    | mundus    |     10 |     0.6473 | [0.6347, 0.6607] | 0.0221 |
| openai/blackboxai/nvidia/nemotron-3-ultra | courage    | diabolus  |     10 |     0.7447 | [0.7327, 0.7560] | 0.0201 |
| openai/blackboxai/nvidia/nemotron-3-ultra | courage    | ignatian  |     10 |     0.7527 | [0.7440, 0.7607] | 0.0142 |
| openai/blackboxai/nvidia/nemotron-3-ultra | temperance | ratio     |     10 |     0.8793 | [0.8633, 0.8940] | 0.0266 |
| openai/blackboxai/nvidia/nemotron-3-ultra | temperance | caro      |     10 |     0.8053 | [0.7893, 0.8227] | 0.0282 |
| openai/blackboxai/nvidia/nemotron-3-ultra | temperance | mundus    |     10 |     0.7553 | [0.7380, 0.7720] | 0.0286 |
| openai/blackboxai/nvidia/nemotron-3-ultra | temperance | diabolus  |     10 |     0.9187 | [0.9087, 0.9287] | 0.0169 |
| openai/blackboxai/nvidia/nemotron-3-ultra | temperance | ignatian  |     10 |     0.9547 | [0.9467, 0.9627] | 0.0136 |

| Virtue     | ratio   | caro   | mundus   | diabolus   | ignatian   |
|------------|---------|--------|----------|------------|------------|
| prudence   | 89.56%  | 89.93% | 73.00%   | 87.07%     | 87.93%     |
| justice    | 83.87%  | 81.80% | 67.07%   | 91.73%     | 90.07%     |
| courage    | 62.53%  | 59.07% | 64.73%   | 74.47%     | 75.27%     |
| temperance | 87.93%  | 80.53% | 75.53%   | 91.87%     | 95.47%     |

Chi-squared test across variants:
  chi2 = 740.9318, df = 4
  p = 0.000000
