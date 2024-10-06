


jupytext: seems cool for collaborative jupyter notebooks, but doesn't add much otherwise :(



# jupyter `.ipynb` (vscode)

```
nix shell nixpkgs#jupyter nixpkgs#python312Packages.bash-kernel
```

# quarto `.qmd` (Rstudio)

i got this working but i forget
 
```
nix shell nixpkgs#rstudio nixpkgs#rPackages.rmarkdown nixpkgs#rPackages.httpgd nixpkgs#rPackages.languageserver
```
# quarto `.qmd` (VScode)

```
nix shell nixpkgs#quarto nixpkgs#jupyter nixpkgs#python312Packages.notebook
```
 