# mldock
Global Machine learning helpers for docker based development. Build, train and deploy on cloud with docker


# helpful tips

- docker compose sees my files as directories in mounted volume - *USE "./path/to/file" format* | https://stackoverflow.com/questions/42248198/how-to-mount-a-single-file-in-a-volume
- simlinks from my container have broken permissions in WSL2 | https://github.com/microsoft/WSL/issues/1475
