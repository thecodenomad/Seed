pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'seeds'
gnome = import('gnome')

# Add a reference to the compiler to use
blueprint_compiler = find_program('blueprint-compiler')

# The blueprint files to be converted
blueprint_files = files(
    'view/window.blp'
)

# The list of the converted .ui files to inject into the build
ui_files = []

foreach blueprint_file : blueprint_files
  path_as_string = '@0@'.format(blueprint_file)
  filename = path_as_string.split('/')[-1]

  ui_file = custom_target(path_as_string.underscorify(),
    input: blueprint_file,
    output: filename.replace('.blp', '.ui'),
    command: [blueprint_compiler, 'compile', '--output', '@OUTPUT@', '@INPUT@'])
  ui_files += ui_file
endforeach

gnome.compile_resources('seeds',
  'seeds.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: [ui_files]
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'seeds.in',
  output: 'seeds',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

seeds_sources = [
  '__init__.py',
  'main.py',
  'view/window.py'
]

install_data(seeds_sources, install_dir: moduledir)
