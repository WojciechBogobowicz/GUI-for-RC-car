# GUI for RC car  
**English version below.**  
GUI zaprojektowane do zdalnie sterowanego samochodzika, który zbudowałem przy pomocy raspberry pi, nakładki oraz silników firmy pololu.  
- GUI wyświetla obraz z kamery
- Samochodzik można kontrolować przy pomocy klawiatury lub joistickiem (zaprojektowanym pod ekrany dotykowe, ale współpracującym też z myszką).
- Na panelu sterowania znajdują się dwa przyciski - do nagrywania filmów i robienia zdjęć.
- Po drugiej stronie w dwóch słupkach zwizualizowana jest prędkość obu kół. Jesli koło kręci się w przód, to w zależności od prędkości, odpowiadający mu słupek zmienia barwę od zielonego do czerwonego, jeśli w tył - od niebieskiego do fioletowego.

Input użytkownika jest konwertowany na dwie wartości od -1 do 1 które odpowiadają prędkościom odpowiednich silników, więc łatwo możesz wykorzystać to GUI w swoim projekcie. W tym celu powinieneś nadpisać funckję _move() z klasy  MotorsController.  

**W projkecie wykorzystano:**  
- Bibliotekę Tkinter do stworzenia grafiki.
- Biblioteki OpenCv oraz PIL do przetwarzania obrazu z kamery wmontowanej w samochodzik.
- Bibliotekę Pynput do obsługi klawiatury oraz bibliotekę threading do robienia tego równolege w czasie działania reszty programu.
- Bibliotekę Unittest do przeprowadzenia testów jednostkowych.

--------------------------------------------------------

**English:**  

This is graphic user interface for remote control car that I build based on rapberry pi and pololu motors and hat.  
- GUI shows video image from the camera.  
- You can control car by keyboard, or joistick (meant for touch screens, but can be used with mouse).  
- There are two buttons - to capture videos and take photos.  
- There are bars that shows car speeds for both wheels. Green to red for forward movements, and blue to violet for backward.  

User input is converted into two values from -1 to 1 coresponding to speeds of two motors, so you can easily adapt it to your project. To do that, you shoud overwrite _move() function from class MotorsController.

**Librares used in project:**  
- Tkinter - to create graphic.
- OpenCv and PIL to process image from camera.
- Pynput to deal with user input from keyboard and threading library, to run it paralel to the rest of the program.
- Unittest to test my own classes from Geometry.py file.
