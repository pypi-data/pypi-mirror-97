# PyBioLib

PyBioLib is a Python package for running BioLib applications from Python scripts, and the command line.

### Python Example
```python
# pip3 install pybiolib
from biolib.samtools import samtools
result = samtools()
print(result.stdout)
```

### Command Line Example
```bash
pip3 install pybiolib
biolib run samtools/samtools
```
