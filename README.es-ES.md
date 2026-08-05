

# Neural Render - Complemento para Blender

## Descripción
Neural Render es un complemento para Blender que integra modelos de IA de Replicate en tu flujo de trabajo. Te permite procesar imágenes renderizadas con IA, mejorando su calidad y resolución, o generando nuevas imágenes basadas en tus renders directamente desde Blender.

## Características
- Escalar y mejorar imágenes renderizadas usando IA (Clarity Upscaler)
- Generar nuevas imágenes basadas en tus renders usando Control Net
- Parámetros personalizables para el procesamiento con IA
- Integración fluida con el pipeline de renderizado de Blender
- Soporte para varios modelos de Stable Diffusion y tipos de control
- Opciones para mosaico (tiling), reducción de escala y modelos LoRA personalizados

## Instalación
1. Descarga el archivo ZIP del complemento
2. En Blender, ve a Editar > Preferencias > Complementos
3. Haz clic en "Instalar" y selecciona el archivo ZIP descargado
4. Habilita el complemento "Render: Neural Render"

## Uso
1. Configura tu clave API de Replicate en las preferencias del complemento
2. Ve al panel de Propiedades > pestaña Render > sección Neural Render
3. Elige el modelo de IA que deseas usar (Clarity Upscaler o Control Net)
4. Ajusta los parámetros de procesamiento de IA según sea necesario
5. Haz clic en el botón "Neural Render" para procesar tu render con IA

## Requisitos
- Blender 4.2.0 o superior
- Conexión a internet activa
- Cuenta de Replicate
- Clave API de Replicate

## Cómo comenzar con Replicate
1. Visita el sitio web de Replicate: https://replicate.com
2. Regístrate para crear una cuenta si aún no tienes una
3. Una vez iniciado sesión, ve a la configuración de tu cuenta
4. Busca la sección de tokens API y genera un nuevo token API
5. Copia este token API y guárdalo de forma segura - lo necesitarás para el complemento

Recuerda nunca compartir tu token API públicamente. Siempre puedes generar un nuevo token si es necesario.

## Configuración
- API Key: Ingresa tu clave API de Replicate en las preferencias del complemento
- AI Model: Elige entre Clarity Upscaler y Control Net
- Model-specific parameters: Ajusta según el modelo seleccionado

### Parámetros de Clarity Upscaler
- Positive Prompt: Describe lo que deseas mejorar en la imagen
- Negative Prompt: Describe lo que deseas evitar en la imagen
- Seed: Establece una semilla para resultados reproducibles
- Steps: Número de pasos de inferencia
- Scheduler: Elige el algoritmo de programador de IA
- Scale Factor: Establece el factor de ampliación
- Other parameters: Ajusta creatividad, parecido, mosaico, etc.

### Parámetros de Control Net
- Prompt: Describe la imagen que deseas generar
- Negative Prompt: Describe lo que deseas evitar en la imagen
- Seed: Establece una semilla para resultados reproducibles
- Steps: Número de pasos de inferencia
- Control Type: Elige entre canny, soft edge, o depth
- Guidance Scale: Ajusta la influencia del prompt
- Control Strength: Establece la fuerza del control

## Soporte
Para reportar problemas, solicitar funciones o contribuir, visita el repositorio de GitHub.

## Recomendaciones y Precauciones de Uso

### PRECAUCIÓN
El uso de este complemento con la API de Replicate puede generar costos. Los usuarios son responsables de su uso y de cualquier cargo asociado. Gestiona cuidadosamente tu configuración para evitar un alto consumo y costos.

### Recomendaciones de Uso
- Puedes renderizar en muy baja calidad sin reducir la escala para mayor velocidad y menor costo.
- Usa la reducción de escala cuando renderices imágenes de más de 1024 píxeles.
- Para mantener los detalles al reducir la escala, puedes renderizar hasta cualquier resolución (2-6k), pero es muy importante usar la reducción de escala para conservar los detalles mientras ahorras consumo y costos.
- Si usas un factor de escala mayor a 2, asegúrate de que tus imágenes renderizadas tengan baja resolución.

### Consejos Útiles
- Cambia la seed para diversificar tu generación.
- Valores más bajos de creativity y resemblance solo escalarán/mejorarán tu render. Para resultados creativos, intenta aumentar estos números y no dudes en experimentar.

### Consejo de Instalación
Si encuentras problemas con dependencias faltantes al instalar el complemento, puedes instalar manualmente los paquetes requeridos. Aquí te mostramos cómo:

#### Método 1 (Funciona en Mac, puede funcionar en algunas configuraciones de Windows):

1. Abre el Editor de Scripts de Blender
2. Crea un nuevo archivo de texto
3. Pega y ejecuta el siguiente código Python:

```python
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'replicate'])
```

4. Reinicia Blender
5. Intenta habilitar el complemento Neural Render nuevamente

#### Método 2 (Alternativa para usuarios de Windows):

Si el Método 1 no funciona en tu sistema Windows, sigue estos pasos:

1. Localiza la carpeta de instalación de Blender. Normalmente se encuentra en:
   `C:\Program Files\Blender Foundation\Blender 4.2`

2. Abre el Explorador de Archivos de Windows y navega a esta carpeta

3. En la barra de direcciones superior, escribe `cmd` y presiona Enter. Esto abrirá una ventana del Símbolo del Sistema en la carpeta de Blender

4. En el Símbolo del Sistema, escribe el siguiente comando y presiona Enter:
   ```
   4.2\python\bin\python.exe -m pip install replicate
   ```

5. Espera a que la instalación se complete. Deberías ver un mensaje de éxito

6. Cierra el Símbolo del Sistema y reinicia Blender

7. Intenta habilitar el complemento Neural Render nuevamente

Estos métodos deberían instalar el paquete necesario 'replicate' en el entorno Python de Blender. Si sigues experimentando problemas, consulta nuestro repositorio de GitHub para obtener las soluciones de problemas más actualizadas.

## Descripción de los Parámetros

- Positive Prompt: Describe lo que deseas mejorar o agregar a la imagen.
- Negative Prompt: Describe lo que deseas evitar o eliminar de la imagen.
- Seed: Establece una semilla para resultados reproducibles (0 significa aleatorio).
- Steps: Número de pasos de inferencia (valores más altos pueden producir mejor calidad pero tardan más).
- Scheduler: Elige el algoritmo de programador de IA para el proceso de difusión.
- Scale Factor: Establece el factor de ampliación para la imagen.
- Dynamic: Ajusta el efecto HDR, prueba valores de 3 a 9.
- Creativity: Controla el nivel de interpretación creativa, prueba valores de 0.3 a 0.9.
- Resemblance: Determina qué tan parecido es el resultado a la entrada, prueba valores de 0.3 a 1.6.
- Tiling Width/Height: Afecta la fractalidad de la imagen, valores más bajos resultan en mayor fractalidad.
- SD Model: Elige el checkpoint del modelo Stable Diffusion.
- Downscaling: Activa para reducir la escala de la imagen antes de ampliarla (recomendado para imágenes grandes).
- Downscaling Resolution: Establece la resolución para la reducción de escala.
- LoRA Links: Agrega enlaces a archivos LoRA para un ajuste fino adicional.
- Custom SD Model: Proporciona un enlace a un modelo Stable Diffusion personalizado.
- Sharpen: Aplica nitidez a la imagen después de la ampliación.
- Mask: Proporciona una URL de imagen de máscara para preservar áreas específicas durante la ampliación.
- Hand Fix: Usa Clarity para corregir las manos en la imagen.
- Pattern: Activa para ampliar patrones con mosaico sin costuras.
- Output Format: Elige el formato para las imágenes de salida (WebP, JPEG, o PNG).

## Licencia

Este proyecto está licenciado bajo la Licencia Pública General GNU v3.0 o posterior (GPL-3.0-or-later) - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Créditos
- Desarrollado por Alex Nix
- Impulsado por Replicate y el modelo Clarity Upscaler
- Construido para Blender, la suite de creación 3D gratuita y de código abierto
- Modelo Flux Control Net por xlabs-ai
- Modelo Control Net por jagilley
- Cursor AI para todo lo demás

## Aviso Legal
Este complemento requiere una cuenta activa de Replicate y el uso de la API puede generar costos. Consulta la tarifa de Replicate para más información.
