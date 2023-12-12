WORKPLACE="$HOME/workplace/SakuinSeizouki"
WORKSPACE="$WORKPLACE/SakuinSeizoukiApi"

(
  cd "$WORKSPACE"
  ICON_SRC="$WORKPLACE/SakuinSeizoukiReactApp/public/vite.svg"

  rm -rf temp
  rm -rf dist/Icon.iconset
  rm -rf dist/Icon.icns

  mkdir temp
  mkdir -p dist
  svgexport "$ICON_SRC" temp/icon_16.png 16:16
  svgexport "$ICON_SRC" temp/icon_32.png 32:32
  svgexport "$ICON_SRC" temp/icon_64.png 64:64
  svgexport "$ICON_SRC" temp/icon_128.png 128:128
  svgexport "$ICON_SRC" temp/icon_256.png 256:256
  svgexport "$ICON_SRC" temp/icon_512.png 512:512
  sleep 2
  svgexport "$ICON_SRC" temp/icon_1024.png 1024:1024

  mkdir dist/Icon.iconset
  cp temp/icon_16.png dist/Icon.iconset/icon_16x16.png
  cp temp/icon_32.png dist/Icon.iconset/icon_16x16@2x.png
  cp temp/icon_32.png dist/Icon.iconset/icon_32x32.png
  cp temp/icon_64.png dist/Icon.iconset/icon_32x32@2x.png
  cp temp/icon_128.png dist/Icon.iconset/icon_128x128.png
  cp temp/icon_256.png dist/Icon.iconset/icon_128x128@2x.png
  cp temp/icon_256.png dist/Icon.iconset/icon_256x256.png
  cp temp/icon_512.png dist/Icon.iconset/icon_256x256@2x.png
  cp temp/icon_512.png dist/Icon.iconset/icon_512x512.png
  cp temp/icon_1024.png dist/Icon.iconset/icon_512x512@2x.png

  iconutil -c icns dist/Icon.iconset
  rm -rf temp
  rm -rf dist/Icon.iconset
)
