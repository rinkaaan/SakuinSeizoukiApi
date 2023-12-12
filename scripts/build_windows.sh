WORKPLACE="$HOME/workplace/SakuinSeizouki"

(
  cd "$WORKPLACE/SakuinSeizoukiApi"
  # pyinstaller --onefile api/run.py --icon=dist\\Icon.ico --clean  --noconfirm
  pyinstaller windows.spec --clean --noconfirm
)
