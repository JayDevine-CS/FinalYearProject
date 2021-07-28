# FinalYearProject
-- University Final Year Project --

Welcome to the Celebrity Lookalike Generation App!

To begin using the application please open the command prompt.

Use the following commands to set up the required environment with the correct dependencies:

```bash
conda create -n stargan-v2 python=3.6.7
conda activate stargan-v2
conda install -y pytorch=1.4.0 torchvision=0.5.0 cudatoolkit=10.0 -c pytorch
conda install x264=='1!152.20180717' ffmpeg=4.0.2 -c conda-forge
pip install opencv-python==4.1.2.30 ffmpeg-python==0.2.0 scikit-image==0.16.2
pip install pillow==7.0.0 scipy==1.2.1 tqdm==4.43.0 munch==2.5.0
```

Then use the change directory command ('cd') to wherever the Artefact_Project\MainApplication\ folder is being stored:

```bash
cd ...\Artefact_Project\MainApplication
```

And finally run the mainApplication.py Python Script to start the application:

```bash
python mainApplication.py
```

The Application will then start with description of each stage on how to generate your images. Thankyou.
