<h1> Instrucciones de instalación </h1>
<h2> Requisitos </h2>
<ul>
  <li> Python 3.8 instalado (Específicamente 3.8). </li>
  <li> Un IDE (Pycharm , Vs code , etc ...) con un ambiente virtual. </li>
</ul>

<h2> Instalación </h2>
<ul>
  <li> Descargar el proyecto como .Zip o con "git clone https://github.com/Afelipe72/proyectoTPD.git" desde el Git bash. </li>
  <li> Una vez se haya descargado el proyecto, entrar a la carpeta raiz del proyecto</li>
  <li> Correr el comando "pip install -r requirements.txt" para instalar todas las depedencias. </li>
</ul>

<h2> Notas </h2>
<ul>
  <li> Si la instalación de los requerimientos falla, entrar a "requirements.txt" y eliminar estas 3 lineas:  </li>
  <ul>
    <li> torch==2.0.1+cu117  </li>
    <li> torchaudio==2.0.2+cu117 </li>
    <li> torchvision==0.15.2+cu117 </li>
 </ul>
  <li> Después, escribir el comando en la consola "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118" (Todo lo que está dentro de las comillas) O entrar a https://pytorch.org , y sacar el comando para instalar torch, torchvision y torchaudio. </li>
 </li>
</ul>
