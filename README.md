# Improving the Training of World-GAN (CS598TZ Final Project)

This project attempts to implement the paper ["Improving the Improved Training of Wasserstein GANs: A Consistency Term and Its Dual Effect"](https://arxiv.org/abs/1803.01541) to World-GAN. This README will go over how to run our code.
Our code is a fork from the original code repository of [World-GAN](https://github.com/Mawiszus/World-GAN)

## Getting Started

This section includes the necessary steps to train World-GAN on your system. We used Windows 11 and were not able to get it running on Mac or Linux.

### Python

You will need [Python 3](https://www.python.org/downloads) and the packages specified in requirements.txt.
We recommend setting up a [virtual environment with pip](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
and installing the packages there.

**NOTE:** If you have a **GPU**, check if it is usable with [Pytorch](https://pytorch.org) and change the requirement in the file to use +gpu instead of +cpu.
Training on a GPU is significantly faster.

Install packages with:
```
$ pip3 install -r requirements.txt -f "https://download.pytorch.org/whl/torch_stable.html"
```
Make sure you use the `pip3` that belongs to your previously defined virtual environment.

### Download Mineways

You will need [Mineways](https://www.realtimerendering.com/erich/minecraft/public/mineways/downloads.html) to read blocks from an input Minecraft world and export them into readable obj files for training.
**Note:** When you run the python script for training below, you may get a warning alert from Mineways. You will need to click "Ok" and training should proceed as normal.
There are instructions in ```minecraft/mineways/README.md```

### Download Blender 

You will need [Blender](https://www.blender.org/download/releases/) render your generated Minecraft output and export to PNG format using the ```CyclesMineways.py``` script in ```minecraft/blender_scripts```.
We used version 2.79, since that is what the authors recommended, however the latest version may work as well.
Included are powershell and bash scripts to render all generated outputs in a directory and move them to a separate ```render/``` directory.
Powershell script run template:
```
.\minecraft\blender_scripts\cycles_render_full_folder.ps1 -objDirectory "[OUTPUT_FOLDER]\wandb\[OUTPUT_RUN_NAME]\files\random_samples\objects\3" -orthScale [ORTHOGONAL_SCALE (default 14.5)] -view [VIEW_PRESET (default: 0)] 
```
The bash script has the same parameters and have a similar command to run.
There are further instructions in ```minecraft/blender_scripts/README.md```

### Set up Wandb 

The original World-GAN code sent training results and model saves to Wandb. We needed to set up accounts to get our graphs and experimental results.

## World-GAN

### Training

Once all prerequisites are installed, World-GAN can be trained by running `main.py`.
Make sure you are using the python installation you installed the prerequisites into.

There are several command line options available for training. These are defined in `config.py`.
An example call which we used to train a 3-layer World-GAN with 4000 iterations each scale was:

```
$ python main.py --input_dir input/minecraft --input_name test --output_dir output/minecraft --output_name print --alpha 100 --niter 4000 --nfc 64 --gan_type 1
```
This command takes a chunk of the world from the input minecraft world "test" to train and exports the generated result to the output Minecraft world "print". The `gan_type` parameter indicates which WGAN variant to train with: 0 - original Wasserstein GAN, 1 - Original World-GAN with gradient penalty, 2 - Our W-GAN with both gradient penalty and consistency term.

To train on other structures, you will need to specify which coordinates of the input world you want `main.py` to grab from. This is configurable in `minecraft/level_utils.py`, specifically in `read_level()`.
For the village we showed in the paper, you will need to comment out the coordinates under `#Village Segment in test World` with `# vol 32000`. 
For the larger village we showed in the slides, you will need to comment out the coordinates under `#Village Segment in test World` with `# vol 98164`. 

The generate the other structures like harbor, fountain, or windmill in ouyr paper some more changes need to be done.
First we will need to get the structures from the "castle" world, so the parameter `--input_name` should change to `castle`.
Next in `levels.util` uncomment the coordinates for the structure you want to use as input for generation. 
The output world can remain the same as long as it is empty, so no changes should need to be done to `output_name`, however if you do get unexpected results, you can try changing to the other output worlds we make available like `Empty_World`, `print1`, `test`...etc.

### Generating samples

If you want to use your trained World-GAN to generate more samples, use `generate_samples.py`.
Make sure you define the path to a pretrained World-GAN and the correct input parameters it was trained with.
An example of the command to run the script:

```
$ python generate_samples.py  --out_ output/wandb/[RUN_NAME]/files --input-dir input/minecraft --input-name [INPUT_WORLD_NAME] --output_dir output/minecraft --output_name [OUTPUT_WORLD_NAME] --num_layer 3 --alpha 100 --niter 4000 --nfc 64
```
The `out_` parameter gives the path to the pretrained World-GAN model 

### Experiments

All methodology and experimental results are explained in our progress report. The commands above is what we used to run our experiments.

## Built With

* Pytorch - Deep Learning Framework
* PyAnvilEditor - a framework for reading and writing nbt files for Minecraft 1.16

## Authors

* **[Josh Moore]** - University of Illinois at Urbana-Champaign
* **[Carl Guo]** - University of Illinois at Urbana-Champaign
* **[Shruthik Musukula]** - University of Illinois at Urbana-Champaign

## Copyright

This code is not endorsed by Mojang and is only intended for research purposes. 

