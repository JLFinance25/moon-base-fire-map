"""Inlines site/data.js into site/template.html -> site/index.html (single self-contained file)."""
t=open('site/template.html').read(); d=open('site/data.js').read()
open('site/index.html','w').write(t.replace('<script src="data.js"></script>','<script>'+d+'</script>'))
