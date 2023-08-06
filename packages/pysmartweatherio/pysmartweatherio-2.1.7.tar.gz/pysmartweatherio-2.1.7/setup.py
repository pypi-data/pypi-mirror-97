from distutils.core import setup
setup(
  name = 'pysmartweatherio',
  packages = ['pysmartweatherio'],
  version = '2.1.7',
  license='MIT',
  description = 'Python Wrapper for Smart Home Weather REST API', 
  long_description=" ".join(
    ["Lightweight Python 3 module to receive data via",
    "REST API from a Smart Home Weather station from WeatherFlow."]),
  author = 'Bjarne Riis',
  author_email = 'bjarne@briis.com',
  url = 'https://github.com/briis/pysmartweatherio',
  keywords = ['SmartWeather', 'weatherflow', 'Python'],
  install_requires=[
          'asyncio',
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)

