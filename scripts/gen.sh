WORKPLACE="$HOME/workplace/SakuinSeizouki"
WORKSPACE="$WORKPLACE/SakuinSeizoukiApi"

(
  cd "$WORKSPACE/api"
  flask spec --output openapi.yaml > /dev/null
)
