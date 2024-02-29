# Firmware 6_1
# Madre : Firmware6_0
# Para  : solutions.fusepong.com ()
# ----- No modificar las primeras 3 lineas -----
# (modificar solo para nuevos o cambios de firmware)
#-------------------------------------------------------------
# administracions de lokers
# reproduccion de audios


## Configuración

Se debe crear o adicionar al archivo /etc/mpd.conf la siguiente configuracion

```bash
audio_output {
    type "alsa"
    name "Fuse sound device"
    device "hw:1,0"  
    format "44100:16:2"           
    mixer_device "default"           
    mixer_control "PCM"    
    mixer_index "0" 
}
```

