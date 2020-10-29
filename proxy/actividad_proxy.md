# Actividad en clase: construir un proxy.

Un proxy es cualquier dispositivo intermedio entre un cliente y servidor, comúnmente utilizado para realizar las consultas a nombre del cliente y luego reenviárselas. Así, por ejemplo, pueden leer artículos científicos desde la casa utilizando el proxy del DCC, ya que las bibliotecas científicas son consultadas por la Universidad, quien ya está registrada, y luego el paper es enviado por el proxy hasta su casa.

En nuestro caso partiremos la primera clase con algo simple:

* Construya un servidor http y córralo localmente en el puerto 8888, cuando usted abra el browser con la URI http://localhost:8888 éste debe mostrar un mensaje de bienvenida.
* Modifique su servidor para que al momento de responder le agregue el header X-ElQuePregunta con su email uchile.cl como valor. Cómo puede probar que eso funciona? con el comando curl -I http://localhost:8888 . curl es un cliente http para texto, la opción -I sirve para traer sólo los headers, también les puede servir -L que en caso de alguna redirección la siga y les traiga la información.
* Modifique su servidor para que pueda leer archivos JSON desde entrada estándar o archivo de configuración, con ello le daremos ciertas instrucciones que explicaremos más adelante. Por mientras úselo para dejar en una variable su email uchile y así el servidor queda con usuario parametrizable.

La segunda clase la usaremos para construir el proxy. Nuestro proxy tendrá dos funcionalidades principales:

1. Bloquear tráfico hacia páginas no permitidas (como un control parental), se definirá una página como la URI semi-completa (esto es http://dominio:puerto/path ).
1. Reemplazar contenido inadecuado (reemplazo el string A con el string B)
Para ello

* Modifique su servidor para que sea un proxy que esté entre un cliente y un servidor, pero que no haga nada, esto es: recibe un requerimiento, se lo envía al servidor, recibe la respuesta y se la envía al cliente.
* Modifique su proxy para que al recibir la URI del servidor chequee si la dirección está bloqueada, de ser así devuelva el código de error 403 y el mensaje de error de su preferencia (por ejemplo: “Forbidden”, o “El proxy no te lo permite”, o “You shall not pass”).
* De no haber error reenvíe la consulta a quien corresponda, pero agregando el header X-ElQuePregunta esta vez al request que va al servidor (desde el proxy).
Para probarlo configure http://localhost:8888 como el proxy de su browser favorito (puede seguir estas instrucciones https://es.ccm.net/faq/25993-como-configurar-un-proxy-en-tu-navegador-web ) y pase a la etapa siguiente (Evaluación). Use el siguiente archivo JSON de prueba:

```
{ "user": "--su email--",

"blocked": ["http://www.dcc.uchile.cl/", "http://anakena.dcc.uchile.cl:8989/secret/"],

"forbidden_words": [{"Lorem": "bleuh"}, {"ipsum": "blauh"}, {"amet": "blah"}]

}
```
