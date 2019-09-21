from os import walk

__all__ = []

for (dirpath, dirnames, filenames) in walk('council_minutes/cases'):
    for name in filenames:
      if '.py' in name: __all__.extend([name.replace('.py', '')])
    break
