<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Create_custom_keyboard_layouts" />

  &#xa0;

  <!-- <a href="https://create_custom_keyboard_layouts.netlify.app">Demo</a> -->
</div>

<h1 align="center">Create_Custom_keyboard_layouts</h1>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Create_custom_keyboard_layouts 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

The project  aims to provide an easy way for users to to  create and customize their own keyboard layouts.
This project is a python code that gets then input keyboard layout settings by using the xmodmap tool. 
The python code then cycles through the input layout settings to get the keycodes and keysym values  associated with each key on the keyboard. 
The python code also includes checking for different modifier settings while cycling through the input keyboard settings.
The final intent of this python code is to generate a text file with 4 8x8 matrices showing the keyboard layouts for the following keyboard modifier types:

      - No Modifier\
      - Shift\
      - AlGr\
      - Shift+AltGr\

## :sparkles: Features ##

:Create various layouts into 8x8 matrices of the current keyboard input settings\


## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have python3 installed and python package codecs for decoding purposes.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/ronyk255/create_custom_keyboard_layouts

# Access
$ cd create_custom_keyboard_layouts

# Install dependencies
$ pip install codecs

# Run the project
$ python3 createCustomKeyBoardLatyouts.py


## Made  by 
<a href="https://github.com/ronyk255}" target="_blank">{{Rony Kuriakose}}</a>

&#xa0;

<a href="#top">Back to top</a>
