application_id = 'org.thecodenomad.seeds'

scalable_dir = 'hicolor' / 'scalable' / 'apps'
install_data(
  scalable_dir / ('@0@.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)

# Install Application Icons

# Chat Bubble Icon
install_data(
  symbolic_dir / ('chat-bubble-empty-symbolic.svg'),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)

# Sprout Icon
install_data(
  symbolic_dir / ('sprout-symbolic.svg'),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)
