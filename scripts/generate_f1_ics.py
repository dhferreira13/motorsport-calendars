name: Atualizar calendário F1 automaticamente

on:
  workflow_dispatch:
  schedule:
    - cron: "0 6 * * 1"

permissions:
  contents: write

jobs:
  update-calendar:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependências
        run: pip install requests pytz

      - name: Gerar calendário F1 2026
        run: python scripts/generate_f1_ics.py

      - name: Commit e push se houver mudanças
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add f1_2026_brt.ics
          git diff --cached --quiet || git commit -m "Atualiza calendário F1 2026 automaticamente"
          git push



