{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/23.11";
  };

  outputs = inputs:
    let
      pkgs = import inputs.nixpkgs { system = "aarch64-darwin"; };
    in
    {
      devShells."aarch64-darwin".default = pkgs.mkShell {
        buildInputs = with pkgs; [
          act
          poetry
          python312
        ];
      };
    };
}
