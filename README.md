# top10kindercadeaus.nl

Statische site. Inhoud staat in `data/lists.json`, de site wordt gebouwd met `python3 build.py` naar `docs/`.

- Lijsten aanpassen: bewerk `data/lists.json`, draai `python3 build.py`.
- Affiliate-links aanzetten: vul `BOL_PARTNER_ID` in `build.py` in (linkformaat eerst controleren in het bol-partnerdashboard).
- Bedrijfsgegevens: vul `OWNER` in `build.py` in.
- Hosting: GitHub Pages vanuit de map `docs/` op branch `main`; `docs/CNAME` bevat het domein.
