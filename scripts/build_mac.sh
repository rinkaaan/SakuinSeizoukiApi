WORKPLACE="$HOME/workplace/SakuinSeizouki"

(
  cd "$WORKPLACE/SakuinSeizoukiApi"
  pyinstaller mac.spec --clean --noconfirm
)
