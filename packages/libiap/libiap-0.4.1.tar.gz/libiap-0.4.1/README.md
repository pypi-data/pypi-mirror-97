# libiap

Please use `pip install libica` instead
- https://pypi.org/project/libica/
- https://github.com/umccr-illumina/libica

## Alpha Modules Deprecation Note

> 🙋‍♂️ only applicable to early adopter and/or existing user of _alpha_ modules in `libiap<=0.4.0`

- These _alpha_ modules directly under top level package (i.e. `libiap.libwes`, `libiap.libgds`, ...) are deprecated in `libica-0.5.0`.
- If you are still using these _alpha_ modules then you can still depend on `libiap-0.4.0` alongside with `libica-0.5.0`.
- However, there won't be side-by-side backward compatibility with `libiap-0.4.0` for all future releases of `libica-0.6.0` onwards.

## License

MIT License and DISCLAIMER

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
