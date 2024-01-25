# Persistence

Aplikace potřebuje obvykle někde uchovávát stav entit. Potřebujeme agregát načítat a ukládat do nějakého úložiště. Proto pro načítání nebo ukládání agregátů jsou připraveny třídy implementující návrhový vzor *Repository*. Protože, každé úložiště má svá specifika jak s ním pracovat, vyplatí se zamyselet nad tím, co mají společného a vytvořit nějakou zastřešující abstrakci či dokonce pro nějaké předpřipravit implementaci.

Tento balík obsahuje rozhraní v podobě protokolů a abtraktních tříd, stejně jako implementaci pro ukládání do paměti, souboru nebo relační databáze SQLite či PosgreSQL.

## Příklady

```python
from basis.persistence.repository import MemoryRepository
from company.domain.model import Person

with MemoryRepository as store:
    store.save(Person(1, "Joe Doe"))
```