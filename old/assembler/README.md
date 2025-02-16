## Environment
```commandline
conda create -n assembler python=3.9
conda activate assembler
pip install moviepy
pip install ffmpeg
```


Download font otf : https://www.fontspace.com/kanok-font-f136188

Create a directory for OpenType fonts if it doesn't exist:
```commandline
sudo mkdir -p /usr/share/fonts/opentype
```

Copy the .otf file to this directory:

```commandline
sudo cp /path/to/your/fontfile.otf /usr/share/fonts/opentype/
```

Update the font cache:
```commandline
sudo fc-cache -f -v
```
