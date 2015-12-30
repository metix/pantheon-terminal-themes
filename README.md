# pantheon-themes - simple theme switcher
pantheon-themes can switch the color theme of the pantheon terminal.

this script is written in python for the linux distro 'elementary OS [freya]'.

## features
- themes are defined in JSON
- themes can be added/changed easily
- current theme can be saved

## requirements
- python 2.7.3 or higher

## usage
a few themes are already defined in the directory 'themes'

load a theme:
```
# load only colors and opacity
./theme-switcher.py load themes/dark.theme

# load the font too
./theme-switcher.py load --font themes/dark.theme
```

save current theme:
```
# save only colors and opacity
./theme-switcher.py save themes/mytheme.theme

# save font too
./theme-switcher.py save --font themes/mytheme.theme
```

show all color variations of current theme:
```
./theme-switcher.py test
```

## notes
- to update the font, you have to close the terminal and open it again
