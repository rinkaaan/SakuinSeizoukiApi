WORKPLACE="$HOME/workplace/SakuinSeizouki"
WORKSPACE="$WORKPLACE/SakuinSeizoukiApi"

(
  cd "$WORKSPACE"
  ICON_SRC="$WORKPLACE/SakuinSeizoukiReactApp/public/vite.svg"

  # Remove temporary files before starting
  rm -rf temp
  rm -rf dist/Icon.ico

  # Create temporary directory
  mkdir temp

  # Generate icon files with different sizes
  svgexport "$ICON_SRC" temp/icon_16.png 16:16
  svgexport "$ICON_SRC" temp/icon_32.png 32:32
  svgexport "$ICON_SRC" temp/icon_48.png 48:48
  svgexport "$ICON_SRC" temp/icon_64.png 64:64
  svgexport "$ICON_SRC" temp/icon_128.png 128:128
  svgexport "$ICON_SRC" temp/icon_256.png 256:256

  # Create target directory
  mkdir dist

  # Convert PNGs to ICO
  magick convert temp/icon_16.png temp/icon_16.ico
  magick convert temp/icon_32.png temp/icon_32.ico
  magick convert temp/icon_48.png temp/icon_48.ico
  magick convert temp/icon_64.png temp/icon_64.ico
  magick convert temp/icon_128.png temp/icon_128.ico
  magick convert temp/icon_256.png temp/icon_256.ico

  # Merge ICO files into a single ICO file
  magick mogrify -format ico temp/*.ico
  magick convert temp/*.ico dist/Icon.ico

  # Clean up temporary files
  rm -rf temp
)
