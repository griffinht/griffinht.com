[[kubernetes]]
map m
map mm $k9s
map ma !kubectl apply -f "$f"
map mA !kubectl apply --force -f "$f"
map md !kubectl delete -f "$f"
map mD !kubectl delete -f "$f"

map C %guix shell jupyter -- code --new-window "$f"


or maybe this is just kubernetes? todo write a lab on kubernetes tooling???