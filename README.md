# amazonai
A Python script that can scrape a Amazon product's reviews and put them through HuggingFace's pipeline sentient analysis to generate a final score.
## Example:
```bash
python3 main.py
```
it will ask for an Amazon product ID, you can get it like so:

`www.amazon.com/dp/`**`B0BZPLYYV1`**`/ref=pd_gw_sspa_dk_gateway_5?ie=UTF8&sp_csd=d2lkZ2V`...

The text in bold is the ID.
