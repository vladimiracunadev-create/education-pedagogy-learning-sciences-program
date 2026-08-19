#!/usr/bin/env python3
"""Genera el sitio estático que se publica en GitHub Pages.

Convierte todo el Markdown del repositorio a HTML autocontenido en `site/`, con
navegación lateral, buscador de las 216 clases en cliente, tema claro/oscuro y
diagramas mermaid. No requiere dependencias externas: incluye un conversor de
Markdown acotado al subconjunto que este repositorio usa.

Uso:
  python scripts/generar_sitio.py           # genera site/
  python scripts/generar_sitio.py --check   # compila sin escribir en disco
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "site"

TITULO = "Programa de Pedagogía, Docencia y Ciencias del Aprendizaje"
SUBTITULO = "18 partes · 216 clases · de los fundamentos del aprendizaje a la formación de formadores"
REPO = "https://github.com/vladimiracunadev-create/education-pedagogy-learning-sciences-program"

SECCIONES = [
    ("docs", "Documentos transversales"),
    ("curriculum", "Currículo"),
    ("cases", "Casos profesionales"),
    ("projects", "Proyectos integradores"),
    ("assessments", "Evaluación"),
    ("templates", "Plantillas"),
    ("labs", "Laboratorios"),
    ("chile-education-system", "Sistema educativo chileno"),
    ("international-education", "Educación comparada"),
    ("books", "Lecturas"),
    ("papers", "Artículos"),
    ("datasets", "Datos"),
    ("notebooks", "Notebooks"),
    ("virtual-school-lab", "Escuela simulada"),
]

PUBLICADOS = {carpeta for carpeta, _ in SECCIONES}
IGNORADOS = {".git", "node_modules", "site", ".venv", "__pycache__", "scripts", "capacitacion"}


# --------------------------------------------------------------------------- #
# Conversor Markdown mínimo
# --------------------------------------------------------------------------- #

CENTINELA = "\x00{}\x00"

EN_LINEA = [
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)"), r'<img src="\2" alt="\1">'),
    (re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"), r'<a href="\2">\1</a>'),
    (re.compile(r"<((?:https?|mailto):[^>\s]+)>"), r'<a href="\1">\1</a>'),
]


def en_linea(texto: str) -> str:
    fragmentos: list[str] = []

    def guardar(match: re.Match) -> str:
        fragmentos.append(f"<code>{html.escape(match.group(1))}</code>")
        return CENTINELA.format(len(fragmentos) - 1)

    texto = re.sub(r"`([^`]+)`", guardar, texto)
    texto = html.escape(texto, quote=False)
    texto = re.sub(r"&lt;br\s*/?&gt;", "<br>", texto)
    for patron, reemplazo in EN_LINEA:
        texto = patron.sub(reemplazo, texto)
    for indice, fragmento in enumerate(fragmentos):
        texto = texto.replace(CENTINELA.format(indice), fragmento)
    return texto


ENLACE_MD = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)\s]+)\)")


def convertir_enlaces(texto: str, carpeta: Path) -> str:
    """Adapta los enlaces del Markdown a la estructura del sitio."""
    def reescribir(match: re.Match) -> str:
        etiqueta, destino = match.group(1), match.group(2)
        if destino.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        ruta, _, ancla = destino.partition("#")
        sufijo = f"#{ancla}" if ancla else ""
        if ruta.endswith("README.md"):
            return f"[{etiqueta}]({ruta[:-9]}index.html{sufijo})"
        if ruta.endswith(".md"):
            return f"[{etiqueta}]({ruta[:-3]}.html{sufijo})"
        if not ruta:
            return match.group(0)
        objetivo = (carpeta / ruta.rstrip("/")).resolve()
        try:
            relativo = objetivo.relative_to(RAIZ).as_posix()
        except ValueError:
            return match.group(0)
        if objetivo.is_dir():
            if relativo.split("/")[0] in PUBLICADOS:
                return match.group(0)
            return f"[{etiqueta}]({REPO}/tree/main/{relativo})"
        return f"[{etiqueta}]({REPO}/blob/main/{relativo}{sufijo})"

    return ENLACE_MD.sub(reescribir, texto)


def ancla(texto: str) -> str:
    limpio = re.sub(r"[^\w\s-]", "", re.sub(r"<[^>]+>", "", texto)).strip().lower()
    return re.sub(r"[\s_]+", "-", limpio)


def markdown_a_html(fuente: str, carpeta: Path) -> str:
    fuente = convertir_enlaces(fuente, carpeta)
    lineas = fuente.split("\n")
    salida: list[str] = []
    pila: list[str] = []
    indice = 0

    def cerrar(nivel: int = 0) -> None:
        while len(pila) > nivel:
            salida.append(f"</{pila.pop()}>")

    while indice < len(lineas):
        linea = lineas[indice]
        limpia = linea.strip()

        if limpia.startswith("```"):
            cerrar()
            lenguaje = limpia[3:].strip()
            cuerpo: list[str] = []
            indice += 1
            while indice < len(lineas) and not lineas[indice].strip().startswith("```"):
                cuerpo.append(lineas[indice])
                indice += 1
            contenido = html.escape("\n".join(cuerpo))
            if lenguaje == "mermaid":
                salida.append(f'<pre class="mermaid">{contenido}</pre>')
            else:
                clase = f' class="lenguaje-{lenguaje}"' if lenguaje else ""
                salida.append(f"<pre><code{clase}>{contenido}</code></pre>")
            indice += 1
            continue

        if not limpia:
            cerrar()
            indice += 1
            continue

        encabezado = re.match(r"^(#{1,6})\s+(.*)$", limpia)
        if encabezado:
            cerrar()
            nivel = len(encabezado.group(1))
            texto = en_linea(encabezado.group(2))
            salida.append(f'<h{nivel} id="{ancla(encabezado.group(2))}">{texto}</h{nivel}>')
            indice += 1
            continue

        if limpia.startswith("|") and indice + 1 < len(lineas) and \
                re.match(r"^\|[\s:|-]+\|$", lineas[indice + 1].strip()):
            cerrar()
            cabecera = [c.strip() for c in limpia.strip("|").split("|")]
            indice += 2
            filas = []
            while indice < len(lineas) and lineas[indice].strip().startswith("|"):
                filas.append([c.strip() for c in lineas[indice].strip().strip("|").split("|")])
                indice += 1
            encabezados = "".join(f"<th>{en_linea(c)}</th>" for c in cabecera)
            cuerpo_tabla = "".join(
                "<tr>" + "".join(f"<td>{en_linea(c)}</td>" for c in fila) + "</tr>"
                for fila in filas
            )
            salida.append(
                f'<div class="tabla"><table><thead><tr>{encabezados}</tr></thead>'
                f"<tbody>{cuerpo_tabla}</tbody></table></div>"
            )
            continue

        if limpia.startswith(">"):
            cerrar()
            bloque: list[str] = []
            while indice < len(lineas) and lineas[indice].strip().startswith(">"):
                bloque.append(lineas[indice].strip()[1:].strip())
                indice += 1
            alerta = ""
            if bloque and re.match(r"^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]$", bloque[0]):
                tipo = bloque[0][2:-1].lower()
                alerta = f" alerta alerta-{tipo}"
                bloque[0] = {"note": "Nota", "tip": "Sugerencia", "important": "Importante",
                             "warning": "Advertencia", "caution": "Precaución"}[tipo]
            parrafos = "".join(f"<p>{en_linea(b)}</p>" for b in bloque if b)
            salida.append(f'<blockquote class="cita{alerta}">{parrafos}</blockquote>')
            continue

        vineta = re.match(r"^(\s*)([-*])\s+(.*)$", linea)
        numerada = re.match(r"^(\s*)(\d+)\.\s+(.*)$", linea)
        if vineta or numerada:
            coincidencia = vineta or numerada
            etiqueta = "ul" if vineta else "ol"
            nivel = len(coincidencia.group(1)) // 2 + 1
            while len(pila) > nivel:
                salida.append(f"</{pila.pop()}>")
            while len(pila) < nivel:
                salida.append(f"<{etiqueta}>")
                pila.append(etiqueta)
            contenido = coincidencia.group(3)
            tarea = re.match(r"^\[([ xX])\]\s+(.*)$", contenido)
            if tarea:
                marcado = " checked" if tarea.group(1).lower() == "x" else ""
                salida.append(
                    f'<li class="tarea"><input type="checkbox" disabled{marcado}> '
                    f"{en_linea(tarea.group(2))}</li>"
                )
            else:
                salida.append(f"<li>{en_linea(contenido)}</li>")
            indice += 1
            continue

        if limpia.startswith("---") and set(limpia) <= {"-"}:
            cerrar()
            salida.append("<hr>")
            indice += 1
            continue

        if limpia.startswith("<") and limpia.endswith(">") and not limpia.startswith("<http"):
            cerrar()
            salida.append(limpia)
            indice += 1
            continue

        cerrar()
        parrafo = [limpia]
        indice += 1
        while indice < len(lineas) and lineas[indice].strip() and \
                not re.match(r"^(\s*)([-*]|\d+\.)\s+", lineas[indice]) and \
                not lineas[indice].strip().startswith(("#", ">", "|", "```", "---", "<")):
            parrafo.append(lineas[indice].strip())
            indice += 1
        salida.append(f"<p>{en_linea(' '.join(parrafo))}</p>")

    cerrar()
    return "\n".join(salida)


# --------------------------------------------------------------------------- #
# Recursos del sitio
# --------------------------------------------------------------------------- #

ESTILOS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --fondo:#ffffff;--fondo-2:#f5f7fa;--texto:#12181f;--tenue:#5a6572;
  --borde:#dfe4ea;--acento:#0b62d0;--acento-suave:#e8f0fc;--codigo:#f2f4f7;
  --sombra:0 1px 2px rgba(16,24,40,.06),0 8px 24px rgba(16,24,40,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-tema="claro"]){
  --fondo:#0e1116;--fondo-2:#161b22;--texto:#e7edf5;--tenue:#9aa7b6;
  --borde:#242c37;--acento:#5aa2ff;--acento-suave:#132339;--codigo:#161b22;
  --sombra:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35);
}}
:root[data-tema="oscuro"]{
  --fondo:#0e1116;--fondo-2:#161b22;--texto:#e7edf5;--tenue:#9aa7b6;
  --borde:#242c37;--acento:#5aa2ff;--acento-suave:#132339;--codigo:#161b22;
  --sombra:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35);
}
html{scroll-behavior:smooth}
body{margin:0;background:var(--fondo);color:var(--texto);
  font:16px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-text-size-adjust:100%}
a{color:var(--acento);text-decoration:none}
a:hover{text-decoration:underline}
header.superior{position:sticky;top:0;z-index:20;background:var(--fondo);
  border-bottom:1px solid var(--borde);padding:.7rem 1.1rem;
  display:flex;gap:1rem;align-items:center;flex-wrap:wrap}
header.superior .marca{font-weight:700;letter-spacing:-.01em}
header.superior .marca span{color:var(--tenue);font-weight:400;font-size:.85rem;display:block}
header.superior nav{margin-left:auto;display:flex;gap:.9rem;flex-wrap:wrap;font-size:.9rem;align-items:center}
button.tema{background:var(--fondo-2);border:1px solid var(--borde);color:var(--texto);
  border-radius:999px;padding:.3rem .8rem;cursor:pointer;font-size:.85rem}
.envoltura{display:grid;grid-template-columns:300px minmax(0,1fr);gap:2rem;
  max-width:1300px;margin:0 auto;padding:1.6rem 1.1rem 4rem}
aside{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 96px);
  overflow-y:auto;font-size:.9rem;padding-right:.4rem}
aside h2{font-size:.72rem;text-transform:uppercase;letter-spacing:.09em;
  color:var(--tenue);margin:1.3rem 0 .45rem}
aside ul{list-style:none;margin:0;padding:0}
aside li{margin:.12rem 0}
aside a{display:block;padding:.28rem .55rem;border-radius:7px;color:var(--texto)}
aside a:hover{background:var(--fondo-2);text-decoration:none}
main{min-width:0}
main h1{font-size:1.95rem;line-height:1.2;letter-spacing:-.02em;margin:.2rem 0 1rem}
main h2{font-size:1.3rem;margin:2.1rem 0 .7rem;padding-bottom:.3rem;border-bottom:1px solid var(--borde)}
main h3{font-size:1.05rem;margin:1.5rem 0 .5rem}
main p{margin:.75rem 0}
blockquote{margin:1.1rem 0;padding:.7rem 1rem;background:var(--fondo-2);
  border-left:3px solid var(--acento);border-radius:0 8px 8px 0;color:var(--tenue)}
blockquote p{margin:0}
blockquote p+p{margin-top:.4rem}
blockquote.alerta{border-left-width:4px}
blockquote.alerta>p:first-child{color:var(--acento);text-transform:uppercase;
  font-size:.75rem;letter-spacing:.08em;font-weight:700}
blockquote.alerta-warning,blockquote.alerta-caution{border-left-color:#d97706}
blockquote.alerta-warning>p:first-child,blockquote.alerta-caution>p:first-child{color:#d97706}
div[align="center"]{text-align:center}
div[align="center"] h1,div[align="center"] h2{border:none}
div[align="center"] img{display:inline-block;margin:.15rem}
code{background:var(--codigo);padding:.13em .38em;border-radius:5px;
  font:.87em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre{background:var(--codigo);border:1px solid var(--borde);border-radius:10px;
  padding:.9rem 1rem;overflow-x:auto}
pre code{background:none;padding:0}
pre.mermaid{background:var(--fondo-2);border:1px solid var(--borde);border-radius:12px;
  padding:1.1rem;overflow-x:auto;text-align:center;font:.85em ui-monospace,Menlo,Consolas,monospace;
  color:var(--tenue);min-height:3rem}
pre.mermaid[data-processed="true"]{color:inherit;font:inherit}
pre.mermaid svg{max-width:100%;height:auto}
.tabla{overflow-x:auto;margin:1rem 0;border:1px solid var(--borde);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.93rem}
th,td{text-align:left;padding:.55rem .75rem;border-bottom:1px solid var(--borde);vertical-align:top}
th{background:var(--fondo-2);font-weight:600}
tbody tr:last-child td{border-bottom:none}
li.tarea{list-style:none;margin-left:-1.2rem}
li.tarea input{margin-right:.45rem}
hr{border:none;border-top:1px solid var(--borde);margin:2rem 0}
img{max-width:100%;height:auto}
.buscador{width:100%;padding:.5rem .75rem;border:1px solid var(--borde);border-radius:9px;
  background:var(--fondo-2);color:var(--texto);font-size:.9rem}
.resultados{margin-top:.6rem;max-height:52vh;overflow-y:auto}
.resultados ul{list-style:none;padding:0;margin:0}
.resultados li{margin:.15rem 0}
.hero{background:var(--fondo-2);border:1px solid var(--borde);border-radius:14px;
  padding:1.6rem;margin-bottom:1.6rem;box-shadow:var(--sombra)}
.hero h1{margin-top:0}
footer{border-top:1px solid var(--borde);color:var(--tenue);font-size:.85rem;
  padding:1.4rem 1.1rem;text-align:center}
@media (max-width:900px){
  .envoltura{grid-template-columns:1fr;gap:1rem}
  aside{position:static;max-height:none;border-bottom:1px solid var(--borde);padding-bottom:1rem}
}
"""

GUION_MERMAID = """
// Los diagramas son el único recurso externo del sitio. Se cargan como módulo con
// versión fijada; si la carga falla —red, bloqueo, uso sin conexión— el bloque queda
// como código legible y el resto de la página funciona igual.
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.esm.min.mjs';

const raiz = document.documentElement;
const oscuro = () => (raiz.getAttribute('data-tema')
  || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'oscuro' : 'claro')) === 'oscuro';

const pintar = async () => {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: oscuro() ? 'dark' : 'default',
    flowchart: { curve: 'basis', useMaxWidth: true },
    fontFamily: 'ui-sans-serif, system-ui, "Segoe UI", Roboto, sans-serif'
  });
  const nodos = document.querySelectorAll('pre.mermaid');
  nodos.forEach(n => {
    if (!n.dataset.fuente) n.dataset.fuente = n.textContent;
    n.innerHTML = n.dataset.fuente;
    n.removeAttribute('data-processed');
  });
  try { await mermaid.run({ nodes: nodos }); } catch (e) { /* queda el código visible */ }
};

pintar();
document.addEventListener('tema-cambiado', pintar);
"""

GUION = """
(function(){
  var raiz=document.documentElement;
  var guardado=null;
  try{guardado=localStorage.getItem('tema');}catch(e){}
  if(guardado){raiz.setAttribute('data-tema',guardado);}
  var boton=document.getElementById('tema');
  if(boton){boton.addEventListener('click',function(){
    var oscuro=window.matchMedia('(prefers-color-scheme: dark)').matches;
    var actual=raiz.getAttribute('data-tema')||(oscuro?'oscuro':'claro');
    var nuevo=actual==='oscuro'?'claro':'oscuro';
    raiz.setAttribute('data-tema',nuevo);
    try{localStorage.setItem('tema',nuevo);}catch(e){}
    document.dispatchEvent(new CustomEvent('tema-cambiado'));
  });}

  var caja=document.getElementById('buscador');
  var lista=document.getElementById('resultados');
  if(!caja||!lista||!window.INDICE)return;
  var base=lista.getAttribute('data-base')||'';
  function pintar(consulta){
    var q=consulta.trim().toLowerCase();
    if(q.length<2){lista.innerHTML='';return;}
    var encontrados=window.INDICE.filter(function(e){
      return e.t.toLowerCase().indexOf(q)>=0||e.p.toLowerCase().indexOf(q)>=0||
             e.c.toLowerCase().indexOf(q)>=0;
    }).slice(0,40);
    if(!encontrados.length){lista.innerHTML='<p style="color:var(--tenue)">Sin resultados.</p>';return;}
    lista.innerHTML='<ul>'+encontrados.map(function(e){
      return '<li><a href="'+base+e.u+'">'+e.n+'. '+e.t+'</a></li>';
    }).join('')+'</ul>';
  }
  caja.addEventListener('input',function(){pintar(caja.value);});
})();
"""


def pagina(titulo: str, cuerpo: str, base: str, menu: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} · {html.escape(TITULO)}</title>
<meta name="description" content="{html.escape(SUBTITULO)}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='26'>🎓</text></svg>">
<link rel="manifest" href="{base}manifest.webmanifest">
<link rel="stylesheet" href="{base}assets/estilos.css">
</head>
<body>
<header class="superior">
  <div class="marca"><a href="{base}index.html" style="color:inherit">{html.escape(TITULO)}</a>
  <span>{html.escape(SUBTITULO)}</span></div>
  <nav>
    <a href="{base}CURRICULUM.html">Currículo</a>
    <a href="{base}docs/METODOLOGIA.html">Metodología</a>
    <a href="{base}docs/BIBLIOGRAFIA.html">Bibliografía</a>
    <a href="{base}STATUS.html">Estado</a>
    <a href="{REPO}">GitHub</a>
    <button class="tema" id="tema" type="button">Tema</button>
  </nav>
</header>
<div class="envoltura">
<aside>
  <input class="buscador" id="buscador" type="search" placeholder="Buscar entre las 216 clases…" aria-label="Buscar clases">
  <div class="resultados" id="resultados" data-base="{base}"></div>
  {menu}
</aside>
<main>
{cuerpo}
</main>
</div>
<footer>
  Material de formación profesional · no reemplaza un título de pedagogía ni una habilitación legal ·
  <a href="{REPO}">código fuente</a>
</footer>
<script src="{base}assets/indice.js"></script>
<script src="{base}assets/sitio.js"></script>
<script type="module" src="{base}assets/diagramas.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Construcción
# --------------------------------------------------------------------------- #

def recolectar() -> list[Path]:
    documentos = list(RAIZ.glob("*.md"))
    for carpeta, _ in SECCIONES:
        if (RAIZ / carpeta).exists():
            documentos += sorted((RAIZ / carpeta).rglob("*.md"))
    return [p for p in documentos
            if not any(parte in IGNORADOS for parte in p.relative_to(RAIZ).parts)]


def construir_menu(curriculo: list[dict], base: str) -> str:
    docs = "".join(
        f'<li><a href="{base}docs/{p.stem}.html">'
        f'{p.stem.replace("_", " ").capitalize()}</a></li>'
        for p in sorted((RAIZ / "docs").glob("*.md"))
    )
    partes = ""
    vistas = []
    for clase in curriculo:
        if clase["part"] in vistas:
            continue
        vistas.append(clase["part"])
        partes += (f'<li><a href="{base}curriculum/{clase["part_slug"]}/index.html">'
                   f'{clase["part"]:02d}. {html.escape(clase["part_title"])}</a></li>')
    otras = "".join(
        f'<li><a href="{base}{carpeta}/index.html">{nombre}</a></li>'
        for carpeta, nombre in SECCIONES
        if carpeta not in {"docs", "curriculum"} and (RAIZ / carpeta).exists()
    )
    return f"""
<h2>Programa</h2>
<ul>
  <li><a href="{base}index.html">Inicio</a></li>
  <li><a href="{base}CURRICULUM.html">Currículo completo</a></li>
  <li><a href="{base}SYLLABUS.html">Programa detallado</a></li>
  <li><a href="{base}ROADMAP.html">Ruta de dominio</a></li>
  <li><a href="{base}STATUS.html">Estado verificable</a></li>
  <li><a href="{base}FILE_INDEX.html">Índice de archivos</a></li>
</ul>
<h2>Documentos</h2>
<ul>{docs}</ul>
<h2>Las 18 partes</h2>
<ul>{partes}</ul>
<h2>Material de apoyo</h2>
<ul>{otras}</ul>
"""


def indice_busqueda(curriculo: list[dict]) -> str:
    catalogo = json.loads((RAIZ / "catalog.json").read_text(encoding="utf-8"))["catalogo"]
    conceptos = {c["n"]: " · ".join(c["conceptos"]) for c in catalogo}
    entradas = [{
        "n": f"{c['global_class']:03d}",
        "t": c["title"],
        "p": c["part_title"],
        "c": conceptos.get(c["global_class"], ""),
        "u": f"curriculum/{c['part_slug']}/{c['slug']}/index.html",
    } for c in curriculo]
    return json.dumps(entradas, ensure_ascii=False, separators=(",", ":"))


def verificar_enlaces() -> dict[str, int]:
    rotos: dict[str, int] = {}
    for archivo in SALIDA.rglob("*.html"):
        texto = archivo.read_text(encoding="utf-8")
        for destino in re.findall(r'(?:href|src)="([^"]+)"', texto):
            if destino.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            objetivo = (archivo.parent / destino.partition("#")[0]).resolve()
            if objetivo.is_dir():
                objetivo = objetivo / "index.html"
            if not objetivo.exists():
                rotos[destino] = rotos.get(destino, 0) + 1
    return rotos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compila sin escribir en disco")
    args = parser.parse_args()

    curriculo = json.loads((RAIZ / "manifests" / "curriculum.json").read_text(encoding="utf-8"))
    documentos = recolectar()
    paginas: list[tuple[Path, str]] = []

    for documento in documentos:
        relativo = documento.relative_to(RAIZ)
        if documento.name == "README.md":
            destino = SALIDA / relativo.parent / "index.html"
        else:
            destino = SALIDA / relativo.with_suffix(".html")
        profundidad = len(destino.relative_to(SALIDA).parts) - 1
        base = "../" * profundidad
        fuente = documento.read_text(encoding="utf-8")
        titulo_match = re.search(r"^#\s+(.*)$", fuente, re.M)
        titulo = re.sub(r"<[^>]+>", "", titulo_match.group(1)) if titulo_match else documento.stem
        cuerpo = markdown_a_html(fuente, documento.parent)
        if destino == SALIDA / "index.html":
            cuerpo = f'<div class="hero">{cuerpo}</div>'
        paginas.append((destino, pagina(titulo, cuerpo, base, construir_menu(curriculo, base))))

    if args.check:
        total = sum(len(contenido) for _, contenido in paginas)
        print(f"OK: {len(paginas)} páginas compilan ({total // 1024} KB).")
        return 0

    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir(parents=True)
    (SALIDA / ".nojekyll").write_text("", encoding="utf-8")

    activos = SALIDA / "assets"
    activos.mkdir()
    (activos / "estilos.css").write_text(ESTILOS.strip() + "\n", encoding="utf-8")
    (activos / "sitio.js").write_text(GUION.strip() + "\n", encoding="utf-8")
    (activos / "diagramas.js").write_text(GUION_MERMAID.strip() + "\n", encoding="utf-8")
    (activos / "indice.js").write_text(
        f"window.INDICE={indice_busqueda(curriculo)};\n", encoding="utf-8")

    for destino, contenido in paginas:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(contenido, encoding="utf-8", newline="\n")

    # Índices de carpetas que no tienen README propio.
    for carpeta, nombre in SECCIONES:
        indice = SALIDA / carpeta / "index.html"
        if indice.exists() or not (SALIDA / carpeta).exists():
            continue
        enlaces = "".join(
            f'<li><a href="{p.relative_to(SALIDA / carpeta).as_posix()}">{p.stem}</a></li>'
            for p in sorted((SALIDA / carpeta).rglob("*.html"))
        )
        indice.write_text(
            pagina(nombre, f"<h1>{nombre}</h1><ul>{enlaces}</ul>", "../",
                   construir_menu(curriculo, "../")),
            encoding="utf-8")

    (SALIDA / "404.html").write_text(
        pagina("Página no encontrada",
               "<h1>404 · Página no encontrada</h1><p>El documento que buscas no existe en este "
               'sitio. Vuelve al <a href="index.html">inicio</a> o usa el buscador de clases.</p>',
               "", construir_menu(curriculo, "")),
        encoding="utf-8")
    (SALIDA / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n", encoding="utf-8")
    (SALIDA / "manifest.webmanifest").write_text(json.dumps({
        "name": TITULO, "short_name": "Pedagogía", "start_url": ".",
        "display": "standalone", "background_color": "#ffffff", "theme_color": "#0b62d0",
        "description": SUBTITULO,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    urls = "".join(
        f"<url><loc>{REPO.replace('https://github.com/vladimiracunadev-create/', 'https://vladimiracunadev-create.github.io/')}"
        f"/{p.relative_to(SALIDA).as_posix()}</loc></url>"
        for p in sorted(SALIDA.rglob("*.html"))
    )
    (SALIDA / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8")

    rotos = verificar_enlaces()
    if rotos:
        print(f"FALLÓ: {len(rotos)} destino(s) internos rotos en el sitio generado:")
        for destino, veces in sorted(rotos.items(), key=lambda x: -x[1])[:20]:
            print(f"  {veces}x  {destino}")
        return 1

    total = len(list(SALIDA.rglob("*.html")))
    print(f"OK: sitio generado en site/ con {total} páginas y sin enlaces internos rotos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
