# MultiWindowSync-PyQt
  * Windows GUI application developed using `PyQt5`.
  * It demonstrates the synchronization of multiple windows using `pyqtSignal`. <br>
  * Inspired by the [work](https://twitter.com/_nonfigurativ_/status/1727322594570027343) of Bjørn Staal. 

https://github.com/aniketrajnish/MultiWindowSync-PyQt/assets/58925008/e00e10e9-6373-46d8-9669-77466ee8bd90

## Usage
* Clone the repository
  ```
  git clone https://github.com/aniketrajnish/MultiWindowSync-PyQt.git
  ```
* Open Terminal and change directory to the script's folder.
  ```
  cd <path-to-repo>\src
  ```
* Install Dependencies
  ```
  pip install -r requirements.txt
  ```
* Run the main script
  ```
  python MultiWindowTest.py
  ```
* Use your own image/GIF.
  ```
  File -> Open Image/GIF
  ```
* In case you don't wanna go through all of this hassle, I've added an exeutable file in the [Releases Section](https://github.com/aniketrajnish/MultiWindowSync-PyQt/releases/tag/v001) that you can directly try on your machine.
  
## Contributing
Contributions to the project are welcome. Currently working on:
* Expanding the environment to 3D using PyOpenGL.
* Fix the bug where the parent image window always moves the image along with it for ref to other windows even if `Move With Window` is unchecked.

## License
MIT License
