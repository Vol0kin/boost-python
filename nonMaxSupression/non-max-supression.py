#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 12:10:17 2019

@author: Vladislav
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageModule
import time

def read_image(file_name, depth):
    """
    Funcion que carga una imagen con la profundidad especificada

    Args:
        file_name: Nombre de la imagen a cargar
        depth: Profundiad (1 color, 0 ByN)
    Return:
        Devuelve una imagen en float64
    """
    # Cargar imagen
    img = cv2.imread(file_name, depth)

    # Transformar imagen a float64
    img = transform_img_float64(img)

    return img


def transform_img_float64(img):
    """
    Funcion que pasa una imagen a float64.

    Args:
        img: Imagen a transformar
    Return:
        Devuelve una imagen en float64
    """

    # Copiar la imagen y convertirla a float64
    transformed = np.copy(img)
    transformed = transformed.astype(np.float64)

    return transformed


def transform_img_uint8(img):
    """
    Funcion que transforma una en float64 a una imagen en uint8 donde cada pixel
    esta en el rango [0, 255]

    Args:
        img: Imagen a transformar
    Return:
        Devuelve la imagen en el rango [0, 255]
    """
    # Copiar la imagen
    trans = np.copy(img)

    # Segun si la imagen es monobanda (2 dimensiones) o tribanda (3 dimensiones)
    # obtener los valores maximos y minimos de GRIS o RGB para cada pixel
    if trans.ndim == 2:
        min_val = np.min(trans)
        max_val = np.max(trans)
    else:
        min_val = np.min(trans, axis=(0, 1))
        max_val = np.max(trans, axis=(0, 1))


    # Normalizar la imagen al rango [0, 1]
    norm = (trans - min_val) / (max_val - min_val)

    # Multiplicar cada pixel por 255
    norm = norm * 255

    # Redondear los valores y convertirlos a uint8
    trans_uint8 = np.round(norm).astype(np.uint8)

    return trans_uint8


def visualize_image(img, title=None):
    """
    Funcion que visualiza una imagen por pantalla.

    Args:
        img: Imagen a visualizar
        title: Titulo de la imagen (por defecto None)
    """
    # Pasar la imagen a uint8
    vis = transform_img_uint8(img)

    # Pasar de una imagen BGR a RGB
    vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

    # Visualizar la imagen
    plt.imshow(vis)
    plt.axis('off')

    if title is not None:
        plt.title(title)

    plt.show()


def apply_kernel(img, kx, ky, border):
    """
    Funcion que aplica un kernel separable sobre una imagen, realizando una
    convolucion

    Args:
        img: Imagen sobre la que aplicar el filtro
        kx: Kernel en el eje X
        ky: Kernel en el eje Y
        border: Tipo de borde
    Return:
        Devuelve una imagen filtrada
    """
    # Hacer el flip a los kernels para aplicarlos como una convolucion
    kx_flip = np.flip(kx)
    ky_flip = np.flip(ky)

    # Realizar la convolucion
    conv_x = cv2.filter2D(img, cv2.CV_64F, kx_flip.T, borderType=border)
    conv = cv2.filter2D(conv_x, cv2.CV_64F, ky_flip, borderType=border)

    return conv


def gaussian_kernel(img, ksize_x, ksize_y, sigma_x, sigma_y, border):
    """
    Funcion que aplica un kernel Gaussiano sobre una imagen.

    Args:
        img: Imagen sobre la que aplicar el kernel
        ksize: Tamaño del kernel
        sigma_x: Sigma sobre el eje X
        sigma_y: Sigma sobre el eje y
        border: Tipo de borde
    Return:
        Devuelve una imagen sobre la que se ha aplicado un kernel Gaussiano
    """
    # Obtener un kernel para cada eje
    kernel_x = cv2.getGaussianKernel(ksize_x, sigma_x)
    kernel_y = cv2.getGaussianKernel(ksize_y, sigma_y)

    # Aplicar kernel Gaussiano
    gauss = apply_kernel(img, kernel_x, kernel_y, border)

    return gauss


def derivative_kernel(img, dx, dy, ksize, border):
    """
    Funcion que aplica un kernel de derivadas a una imagen.

    Args:
        img: Imagen sobre la que aplicar el kernel.
        dx: Numero de derivadas que aplicar sobre el eje X.
        dy: Numero de derivadas que aplicar sobre el eje Y.
        ksize: Tamaño del kernel
        border: Tipo de borde
    Return:
        Devuelve una imagen sobre la que se ha aplicado el filtro de derivadas.
    """
    # Obtener los kernels que aplicar a cada eje (es descomponible porque es
    # el kernel de Sobel)
    kx, ky = cv2.getDerivKernels(dx, dy, ksize, normalize=True)

    # Aplicar los kernels sobre la imagen
    der = apply_kernel(img, kx, ky, border)

    return der


def log_kernel(img, ksize, sigma_x, sigma_y, border):
    """
    Funcion que aplica un kernel LoG (Laplacian of Gaussian) sobre una imagen.

    Args:
        img: Imagen sobre la que aplicar el kernel
        ksize: Tamaño del kernel Gaussiano y Laplaciano
        sigma_x: Valor de sigma en el eje X de la Gaussiana
        sigma_y: Valor de sigma en el eje Y de la Gaussiana
        border: Tipo de borde
    Return:
        Devuelve una imagen sobre la que se ha aplicado un filtro LoG
    """

    # Aplicar filtro Gaussiano
    gauss = gaussian_kernel(img, ksize, ksize, sigma_x, sigma_y, border)
    
    # Obtener los filtros de derivada segunda en cada eje, aplicados sobre
    # el filtro Gaussiano
    dx2 = derivative_kernel(gauss, 2, 0, ksize, border)
    dy2 = derivative_kernel(gauss, 0, 2, ksize, border)
    
    # Combinar los filtros de derivadas y obtener Laplaciana de Gaussiana
    laplace = dx2 + dy2

    return laplace


def non_max_supression(img):
    """
    Funcion que realiza la supresion de no maximos dada una imagen de entrada

    Args:
        img: Imagen sobre la que realizar la supresion de no maximos
    Return:
        Devuelve una nueva imagen sobre la que se han suprimido los maximos
    """
    # Crear imagen inicial para la supresion de maximos (inicializada a 0)
    supressed_img = np.zeros_like(img)

    # Para cada pixel, aplicar una caja 3x3 para determinar el maximo local
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Obtener la region 3x3 (se consideran los bordes para que la caja
            # tenga el tamaño adecuado, sin salirse)
            region = img[max(i-1, 0):i+2, max(j-1, 0):j+2]

            # Obtener el valor actual y el maximo de la region
            current_val = img[i, j]
            max_val = np.max(region)

            # Si el valor actual es igual al maximo, copiarlo en la imagen de supresion
            # de no maximos
            if max_val == current_val:
                supressed_img[i, j] = current_val

    return supressed_img


def laplacian_scale_space(img, ksize, border, N, sigma=1.0, sigma_inc=1.2, boost=False):
    """
    Funcion que construye el espacio de escalas Laplaciano de una imagen dada

    Args:
        img: Imagen de la que extraer el espacio de escalas
        ksize: Tamaño del kernel
        border: Tipo de borde
        N: Numero de escalas
        sigma: Valor inicial del kernel (default 1)
        sigma_inc: Multiplicador que incrementa el sigma (default 1.2)
        boost: Usar o no implementacion de no maximos en Boost.Python
    Return:
        Devuelve una lista con N imagenes, formando el espacio de escalas y los
        valores de sigma utilizados
    """
    # Crear listas que contendran las imagenes y los sigma
    scale_space = []
    sigma_list = []

    total_time = 0

    # Crear las N escalas
    for _ in range(N):
        # Aplicar Laplacian of Gaussian
        level_img = log_kernel(img, ksize, sigma, sigma, border)

        # Normalizar multiplicando por sigma^2
        level_img *= sigma ** 2

        # Elevar al cuadrado la imagen resultante
        level_img = level_img ** 2

        # Suprimir no maximos
        if boost:
            t1 = time.time()
            supressed_level = imageModule.non_max_supression(level_img)
            t2 = time.time()
        else:
            t1 = time.time()
            supressed_level = non_max_supression(level_img)
            t2 = time.time()
        
        time_diff = t2 - t1

        print(f"Time in non-max supression: {time_diff}")
        total_time += time_diff        

        # Guardar imagen y sigma
        scale_space.append(supressed_level)
        sigma_list.append(sigma)

        # Incrementar sigma
        sigma *= sigma_inc
    
    print(f"Total time spent in non-max supression: {total_time}")

    return scale_space, sigma_list


def visualize_laplacian_scale_space(img, sigma, title=None):
    """
    Funcion que permite visualizar una imagen generada en el espacio de escalas
    Laplaciano con circulos en las zonas destacadas

    Args:
        img: Imagen que mostrar
        sigma: Valor de sigma que se ha utilizado para generar la iamgen
        title: Titulo de la imagen (default None)
    """
    # Pasar la imagen a uint8
    vis = transform_img_uint8(img)

    # Obtener los indices de las filas y columnas donde los pixels tienen un valor
    # por encima de la media (es decir, que hayan sido destacados)
    # Las filas y columnas estan invertidas
    idx_col, idx_row = np.where(vis > 128)

    # Pasar de una imagen BGR a RGB
    vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)

    # Pintar un circulo verde por cada punto
    for point in zip(idx_row, idx_col):
        cv2.circle(vis, point, int(np.sqrt(2) * sigma), (0, 255, 0))

    # Visualizar la imagen
    plt.imshow(vis)
    plt.axis('off')

    if title is not None:
        plt.title(title)

    plt.show()

visualize = False

# Cargar la imagen en blanco y negro
cat = read_image('imagenes/cat.bmp', 0)

# Visualizar imagen del gato
if visualize:
    visualize_image(cat, 'Original image')



scale, sigma = laplacian_scale_space(cat, 5, cv2.BORDER_REPLICATE, 100, boost=False)

if visualize:
    for img, sigma  in zip(scale, sigma):
        visualize_image(img, r'Non-max supressed image using $\sigma={}$'.format(sigma))
        visualize_laplacian_scale_space(img, sigma, r'Relevant features using $\sigma={}$'.format(sigma))


scale, sigma = laplacian_scale_space(cat, 5, cv2.BORDER_REPLICATE, 100, boost=True)

if visualize:
    for img, sigma  in zip(scale, sigma):
        visualize_image(img, r'Non-max supressed image using $\sigma={}$'.format(sigma))
        visualize_laplacian_scale_space(img, sigma, r'Relevant features using $\sigma={}$'.format(sigma))
