# Bot de Ofertas MercadoLibre → Telegram + Instagram (+ Twitter manual)

Bot 100% gratuito que revisa MercadoLibre todos los días, detecta bajas reales
de precio, y publica automáticamente en Telegram e Instagram.

---

## Cómo funciona (arquitectura)

```
GitHub Actions (cron diario, gratis)
        │
        ▼
  scraper.py  ──► consulta API pública de MercadoLibre
        │
        ▼
comparador.py ──► compara contra data/precios.json (histórico)
        │           y detecta bajas reales de precio
        ▼
   ┌────┴────┐
   ▼         ▼
Telegram   Instagram
(todas     (solo la
las ofertas) mejor del día)
```

No necesitás servidor propio: todo corre en la nube gratuita de GitHub
Actions, una vez al día, y el historial de precios se guarda como un
archivo JSON dentro del mismo repositorio.

---

## PASO 1 — Crear el bot de Telegram (5 minutos)

1. Abrí Telegram y buscá **@BotFather**.
2. Mandale `/newbot`, seguí las instrucciones y ponele un nombre.
3. Te va a dar un **token** con este formato: `123456789:AAExxxxxxxxxxxxxxxxxxxxxx`.
   Guardalo, es tu `TELEGRAM_BOT_TOKEN`.
4. Creá un **canal** de Telegram (puede ser público o privado).
5. Agregá tu bot como **administrador** del canal.
6. Para obtener el `TELEGRAM_CHAT_ID`:
   - Si el canal es público: usá directamente `@nombre_del_canal` como chat_id.
   - Si es privado: mandá un mensaje cualquiera al canal, y luego visitá
     `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` en el navegador.
     Ahí vas a ver un `"chat":{"id":-1001234567890...}` — ese número
     (con el signo menos incluido) es tu chat_id.

---

## PASO 2 — Crear la app de Instagram (20-30 minutos, es la parte más larga)

1. Tu cuenta de Instagram tiene que ser **Business** o **Creator**
   (Configuración → Cuenta → Cambiar a cuenta profesional. Es gratis).
2. Creá o usá una **Página de Facebook** y vinculala a tu cuenta de Instagram
   desde Configuración de la cuenta de Instagram → Cuenta vinculada.
3. Andá a [developers.facebook.com](https://developers.facebook.com/) →
   **Mis apps** → **Crear app** → tipo "Business".
4. Dentro de la app, agregá el producto **"Instagram Graph API"**.
5. En **Herramientas → Explorador de la API Graph**:
   - Seleccioná tu app.
   - Pedí permisos: `instagram_basic`, `instagram_content_publish`,
     `pages_show_list`, `pages_read_engagement`.
   - Generá un **token de acceso de usuario** (corto plazo).
6. Convertí ese token en uno de **larga duración** (dura ~60 días,
   se puede renovar):
   ```
   GET https://graph.facebook.com/v21.0/oauth/access_token?
       grant_type=fb_exchange_token&
       client_id=<APP_ID>&
       client_secret=<APP_SECRET>&
       fb_exchange_token=<TOKEN_CORTO>
   ```
7. Con ese token, buscá tu **Instagram Business Account ID**:
   ```
   GET https://graph.facebook.com/v21.0/me/accounts?access_token=<TOKEN>
   ```
   Te devuelve tus páginas; con el `id` de la página, pedí:
   ```
   GET https://graph.facebook.com/v21.0/<PAGE_ID>?fields=instagram_business_account&access_token=<TOKEN>
   ```
   Eso te da el `IG_BUSINESS_ID`.

> **Nota:** para uso personal (solo vos publicando en tu propia cuenta) esto
> funciona en modo "Development" sin necesitar la revisión completa de Meta
> (App Review). Solo se pide revisión si querés que *otros usuarios* usen tu
> app. El token de 60 días hay que renovarlo manualmente cada 2 meses
> (o automatizarlo más adelante).

---

## PASO 3 — Twitter/X (la posta)

Desde febrero de 2026, X eliminó el tier gratuito de su API. Las opciones son:

- **Pagar pay-per-use** (~$0.015 por post sin link, ~$0.20 con link). Con 1
  post diario serían pocos dólares al mes — si más adelante querés sumarlo,
  te armo el módulo `publicador_twitter.py`.
- **Manual**: dejá que el bot te mande la alerta a VOS por Telegram (a tu
  chat privado, no al canal público) y publicás manualmente en 10 segundos.

Por ahora el flujo no incluye Twitter automático; arrancamos con Telegram +
Instagram, que son gratis de verdad.

---

## PASO 4 — Subir el proyecto a GitHub

1. Creá un repositorio nuevo en GitHub (puede ser privado).
2. Subí todos los archivos de este proyecto:
   ```bash
   git init
   git add .
   git commit -m "Bot de ofertas inicial"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

---

## PASO 5 — Configurar los secrets en GitHub

En tu repo: **Settings → Secrets and variables → Actions → New repository secret**.

Agregá estos 4 secrets:

| Nombre | Valor |
|---|---|
| `TELEGRAM_BOT_TOKEN` | El token que te dio BotFather |
| `TELEGRAM_CHAT_ID` | El ID o @usuario de tu canal |
| `IG_ACCESS_TOKEN` | El token de larga duración de Meta |
| `IG_BUSINESS_ID` | El ID de tu cuenta de Instagram Business |

---

## PASO 6 — Probar el workflow

1. Andá a la pestaña **Actions** de tu repo.
2. Seleccioná el workflow **"Bot de ofertas diario"**.
3. Click en **"Run workflow"** para probarlo manualmente (no hace falta
   esperar al cron).
4. Revisá los logs. Si todo salió bien, deberías ver los mensajes llegando
   a tu canal de Telegram.
5. Una vez que confirmes que funciona, el cron (`0 12 * * *`, todos los días
   a las 12:00 UTC) lo va a correr solo, sin que hagas nada más.

---

## Personalización

- **Cambiar qué productos buscar**: editá la lista `KEYWORDS` en `main.py`.
- **Cambiar el país**: editá `SITE_ID` en `scraper.py` (MLA=Argentina,
  MLM=México, MLB=Brasil, MCO=Colombia, MLC=Chile, MPE=Perú).
- **Cambiar el umbral de "oferta real"**: editá `UMBRAL_BAJA_PORCENTAJE` en
  `comparador.py` (por defecto 5%).
- **Cambiar el horario**: editá el `cron` en `.github/workflows/daily.yml`
  (está en UTC, restale/sumale horas según tu zona horaria).
- **Activar Instagram**: descomentá las líneas correspondientes en
  `main.py` una vez que tengas el `IG_ACCESS_TOKEN` configurado.

---

## Estructura de archivos

```
ml-ofertas-bot/
├── scraper.py              # Busca productos en MercadoLibre
├── comparador.py            # Detecta bajas de precio reales
├── notificador_telegram.py  # Publica en Telegram
├── publicador_instagram.py  # Publica en Instagram
├── main.py                  # Orquesta todo el flujo
├── requirements.txt         # Dependencias de Python
├── data/
│   └── precios.json         # Histórico de precios (se genera solo)
└── .github/workflows/
    └── daily.yml             # Cron diario gratis en GitHub Actions
```
