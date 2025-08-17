#!/bin/bash
set -e # to stop when anyone failure

echo "📰 Buscando notícias do CNN Brasil..."
scrapy crawl CNNBrasil -s LOG_LEVEL=CRITICAL

echo "📰 Buscando notícias no FIIsNoticias..."
scrapy crawl FIIsNoticias -s LOG_LEVEL=CRITICAL

echo "📰 Buscando notícias do InfoMoney..."
scrapy crawl InfoMoney -s LOG_LEVEL=CRITICAL

echo "📰 Buscando notícias do Money Times..."
scrapy crawl MoneyTimes -s LOG_LEVEL=CRITICAL

echo "💙 Todas as coletas de notícias de veículos concluídas com sucesso!"
