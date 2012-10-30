CalibreServer
=====

*CalibreServer befindet sich noch in der alpha phase.*

CalibreServer ist der versuch einen python basierenden (reinen) eBook Server für alle Geräte zu entwickeln. Die offzielle Server app bietet wesentlich mehr funktionen, diese Version ist lediglich dazu gedacht die mit Calibre verwalteten Bücher (dynamisch) aufzulisten. Es handelt sich also nur um einen reinen Content Server. Ich betreibe CalibreServer auf einer DS211j, diese war auch der Grund wieso ich mit der entwicklung angefangen habe. Der ofizielle Server läuft nur mit vielen Anpassungen auf der DS.

Features:

* auflistung aller Bücher nach rating
* auflistung aller Bücher nach autor
* durchsuchen von Autor, Titel und Buchbeschreibung
* anzeige der x neusten Bücher
* auflistung nach Tags, Autor, Serie, Rating, Neuste

Geplant:

* opds support für eBook reader wie stanza etc.
* design veränderungen


## Anforderungen

Python 2.7+, bottle, sqlaclhemy

