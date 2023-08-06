# Pitwi

Module for terminal/console user interface.

# Aperçu

## Only Python :

```python
from pitwi import Root, Text

(
    Root(width = 45, height = 8)
    .add(Text('Puf', bg='white', fg='black'))
    .add(Text('Paf'), row=2, column=2)
    .run()
)
```

## Python + XML/CSS :

```xml
<root width="45" height="8">
	<style>
		#pwik {
			bg: white;
			fg: black;
		}
	</style>
	<text id="pwik">Puf</text>
	<text row="2" column="2">Paf</text>
</root>
```

```python
from pitwi import parser

parser.file('NAME_OF_YOUR_FILE.xml').run()
```